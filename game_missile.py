import pygame, random
from pygame.rect import Rect

from game_base_sprite import BaseSprite
from game_physics import Direction

class Missile(BaseSprite):
    def __init__(self, graphic, player) -> None:
        super().__init__()

        self.image = pygame.image.load(graphic)
        rand = random.randint(1, 5)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * rand, self.image.get_height() * rand))
        self.rect = self.image.get_rect()
        self.id_num = "missile"
        self.lifespan = 30 * 6
        self.fired_by = player
        self.velocity.set_bounce(True)
        self.force.lifespan = 10

    def set_missile_launch(self, pos, direction = Direction.NONE, direction2 = Direction.NONE):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.force.apply_force(25, direction)
        self.force.apply_force(25, direction2)

    def update(self, *args, **kwargs) -> None:
        self.lifespan -= 1
        super().update(*args, **kwargs)

        if self.lifespan <= 0:
            self.kill()