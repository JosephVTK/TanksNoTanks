from game_missile import Missile
from game_utils import get_center_of_rect
from game_physics import Force, Direction
from game_character import Character

import pygame, random

gfx = [
    "tank_small_blue",
    "tank_small_green",
    "tank_small_pink",
    "tank_small_yellow"
]

class Controller:
    AXIS_LEFT_STICK_X = 0
    AXIS_LEFT_STICK_Y = 1

    AXIS_RIGHT_STICK_X = 3
    AXIS_RIGHT_STICK_Y = 4

    AXIS_LEFT_TRIGGER = 2
    AXIS_RIGHT_TRIGGER = 5

    LEFT_STICK = [AXIS_LEFT_STICK_X, AXIS_LEFT_STICK_Y]
    RIGHT_STICK = [AXIS_RIGHT_STICK_X, AXIS_RIGHT_STICK_Y]

    AXIS_NAMES = {
        AXIS_LEFT_STICK_X : "Left Stick X",
        AXIS_LEFT_STICK_Y : "Left Stick Y",
        AXIS_RIGHT_STICK_X : "Right Stick X",
        AXIS_RIGHT_STICK_Y : "Right Stick Y",
        AXIS_LEFT_TRIGGER : "Left Trigger",
        AXIS_RIGHT_TRIGGER : "Right Trigger",
    }

    def __init__(self, joystick) -> None:
        self.joystick = joystick
        self.button_state = {}
        self.axis_state = {
            self.AXIS_LEFT_STICK_X : 0,
            self.AXIS_LEFT_STICK_Y : 0,
            self.AXIS_RIGHT_STICK_X : 0,
            self.AXIS_RIGHT_STICK_Y : 0,
            self.AXIS_LEFT_TRIGGER : -1,
            self.AXIS_RIGHT_TRIGGER : -1,
        }

    def process_event(self, event):
        match (event.type):
            case pygame.JOYAXISMOTION:
                self._axis_event(event)

    def get_analog_position(self, analog_stick):
        if analog_stick == self.LEFT_STICK:
            x_axis, y_axis = self._get_axis(self.AXIS_LEFT_STICK_X), self._get_axis(self.AXIS_LEFT_STICK_Y)
            x, y = self._get_direction(self.AXIS_LEFT_STICK_X, x_axis), self._get_direction(self.AXIS_LEFT_STICK_Y, y_axis)

        if analog_stick == self.RIGHT_STICK:
            x_axis, y_axis = self._get_axis(self.AXIS_RIGHT_STICK_X), self._get_axis(self.AXIS_RIGHT_STICK_Y)
            x, y = self._get_direction(self.AXIS_RIGHT_STICK_X, x_axis), self._get_direction(self.AXIS_RIGHT_STICK_Y, y_axis)

        return x, y

    def _axis_event(self, event):
        if abs(event.value) <= 0.5:
            self._set_axis(event.axis, 0)
            return

        self._set_axis(event.axis, event.value)

    def _clear_all_axis(self):
        for axis in self.axis_state.keys():
            self.axis_state[axis] = 0

    def _set_axis(self, axis, value):
        self.axis_state[axis] = round(value, 2)

    def _get_axis(self, axis):
        axis = self.axis_state.get(axis)
        if axis == None:
            self.axis_state[axis] = 0
            return 0
        return axis

    def _get_stick(self, stick):
        return self._get_axis(stick[0]), self._get_axis(stick[1])

    def _get_direction(self, axis, value):
        if axis in [self.AXIS_LEFT_STICK_X, self.AXIS_RIGHT_STICK_X]:
            if value > 0:
                return Direction.RIGHT
            elif value < 0:
                return Direction.LEFT
            else:
                return Direction.NONE

        if axis in [self.AXIS_LEFT_STICK_Y, self.AXIS_RIGHT_STICK_Y]:
            if value > 0:
                return Direction.DOWN
            elif value < 0:
                return Direction.UP
            else:
                return Direction.NONE

class Player:
    def __init__(self, joystick) -> None:
        self.controller = Controller(joystick)
        self.character = None
        self.laser_sound = pygame.mixer.Sound('sounds/laser.wav')
        self.alive = True
        self.missiles = pygame.sprite.Group()

    def set_character(self, character):
        self.character = character

    def button_down(self, button, game):
        if button == 0 or button == 5:
            x_dir, y_dir = self.controller.get_analog_position(Controller.RIGHT_STICK)

            if self.alive is False:
                return

            if x_dir == Direction.NONE and y_dir == Direction.NONE:
                return

            missile = Missile("gfx/missile_5_5.png", self)
            pygame.mixer.Sound.play(self.laser_sound)

            player_rect = self.character.rect
            x = player_rect.x + (player_rect.width / 2)
            y = player_rect.y + (player_rect.height / 2)

            if y_dir == Direction.UP:
                y -= player_rect.height
            if y_dir == Direction.DOWN:
                y += player_rect.height
            if x_dir == Direction.LEFT:
                x -= player_rect.width
            if x_dir == Direction.RIGHT:
                x += player_rect.width

            missile.set_missile_launch((x,y), x_dir, y_dir)

            self.missiles.add(missile)
            game.missiles.add(missile)
            game.sprites.add(missile)
        elif button == 7:
            if self.alive is True:
                return

            self.set_character(Character(f"gfx/{random.choice(gfx)}.png", self))
            game.add_sprite_to_game(self.character)
            game.characters.add(self.character)
            self.alive = True

    def axis_motion(self, event):
        self.controller.process_event(event)
        self._controller_effect()

    def hat_motion(self, value):
        pass

    def key_down(self, key):
        pass

    def _controller_effect(self):
        x_dir, y_dir = self.controller.get_analog_position(Controller.LEFT_STICK)

        if x_dir == Direction.LEFT:
            self.character.force.set_force(5, Direction.LEFT)
            self.character.force.set_force(0, Direction.RIGHT)
        elif x_dir == Direction.RIGHT:
            self.character.force.set_force(5, Direction.RIGHT)
            self.character.force.set_force(0, Direction.LEFT)
        else:
            self.character.force.set_force(0, Direction.RIGHT)
            self.character.force.set_force(0, Direction.LEFT)           

        if y_dir == Direction.UP:
            self.character.force.set_force(5, Direction.UP)
            self.character.force.set_force(0, Direction.DOWN)
        elif y_dir == Direction.DOWN:
            self.character.force.set_force(5, Direction.DOWN)
            self.character.force.set_force(0, Direction.UP)
        else:
            self.character.force.set_force(0, Direction.DOWN)
            self.character.force.set_force(0, Direction.UP)

        trigger = self.controller._get_axis(Controller.AXIS_LEFT_TRIGGER)
        self.character.velocity.set_friction(max(trigger, .1))

        trigger = self.controller._get_axis(Controller.AXIS_RIGHT_TRIGGER)
        for missile in self.missiles.sprites():
            new_friction = max(trigger, 0)
            missile.velocity.set_friction(new_friction)