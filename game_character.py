import pygame
from game_base_sprite import BaseSprite

class Character(BaseSprite):
    def __init__(self, graphic, player) -> None:
        super().__init__()

        self.image = pygame.image.load(graphic)
        self.rect = self.image.get_rect()
        self.id_num = "character"
        self.player = player
        self.velocity.set_bounce(True)
        self.velocity.set_friction(.1)