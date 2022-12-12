import sys, pygame, random
from pygame.sprite import Sprite, Group

import json

from game_player import Player
from game_character import Character

with open ('settings.json', 'r') as f:
    settings = json.load(f)

if settings.get("debug"):
    settings = {}

gfx = [
    "tank_small_blue",
    "tank_small_green",
    "tank_small_pink",
    "tank_small_yellow"
]

class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        pygame.display.set_caption("Tanks But No Tanks!")

        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')
        self.kaboom_sound = pygame.mixer.Sound('sounds/kaboom.wav')

        self.clock = pygame.time.Clock()
        
        self.size = width, height = settings.get('resolution_x', 320), settings.get('resolution_y', 240)
        self.flags = pygame.RESIZABLE
        self.screen = pygame.display.set_mode(self.size, flags=self.flags)
        self.background_color = 15, 15, 15

        self.sprites = Group()
        self.characters = Group()
        self.missiles = Group()

        self.players = []
        self.joysticks = {}

        self._collect_players()

    def add_sprite_to_game(self, sprite):
        x, y = self.size
        sprite.rect.x = random.randint(0, x - sprite.rect.width)
        sprite.rect.y = random.randint(0, y - sprite.rect.height)
        self.sprites.add(sprite)

    def _collect_players(self):
        for x in range(pygame.joystick.get_count()):
            player = Player(pygame.joystick.Joystick(x))
            self.players.append(player)
            self.joysticks[x] = player
            player.set_character(Character(f"gfx/{random.choice(gfx)}.png", player))
            self.add_sprite_to_game(player.character)
            self.characters.add(player.character)

    def _refresh(self):
        self.size = pygame.display.get_window_size()
        self.screen.fill(self.background_color)
        self.sprites.update(container=self.size)
        self._collision()
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def _collision(self):
        hit = pygame.sprite.groupcollide(self.characters, self.missiles, False, True)

        for key, val in hit.items():
            for m in val:
                if random.randint(1, 5) == 5:
                    pygame.mixer.Sound.play(self.kaboom_sound)
                    key.player.alive = False
                    key.kill()
                else:
                    pygame.mixer.Sound.play(self.hit_sound)


    def _handle_event(self, event):
        match event.type:
            case pygame.QUIT:
                sys.exit()
            case pygame.WINDOWSIZECHANGED:
                self.size = (event.x, event.y)
            case pygame.JOYBUTTONDOWN:
                joystick = event.joy
                player = self.joysticks.get(joystick)

                if player:
                    player.button_down(event.button, self)

            case pygame.JOYAXISMOTION:
                joystick = event.joy
                player = self.joysticks.get(joystick)

                if player:
                    player.axis_motion(event)
            case _:
                pass

    def run(self):
        while True:
            for event in pygame.event.get():
                self._handle_event(event)
                
            self._refresh()
            self.clock.tick(30)


game = Game()
game.run()