from pygame.sprite import Sprite

from game_physics import Velocity, Force

class BaseSprite(Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.velocity = Velocity()
        self.force = Force()
        
    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)

        self.velocity.apply_forces([self.force])
        self.rect = self.velocity.translate_rect(self.rect)

        if kwargs.get('container'):
            self._contain(kwargs.get('container'))

    def _contain(self, container_xy):
        x, y = container_xy
        restrict_x, restrict_y = False, False

        if self.rect.left < 0:
            self.rect.x = 0
            restrict_x = True

        if self.rect.top < 0:
            self.rect.y = 0
            restrict_y = True

        if self.rect.right > x:
            self.rect.x = x - self.rect.width
            restrict_x = True

        if self.rect.bottom > y:
            self.rect.y = y - self.rect.height
            restrict_y = True

        if self.velocity.bounce:
            if restrict_y:
                self.velocity.apply_bounce("y")
                self.force.apply_bounce("y")
            elif restrict_x:
                self.velocity.apply_bounce("x")
                self.force.apply_bounce("x")
