import pygame as pg

from settings import WIDTH


class Paddle(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, color, *groups):
        super(Paddle, self).__init__(*groups)
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.centerx = pg.mouse.get_pos()[0]

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x + self.rect.width >= WIDTH:
            self.rect.x = WIDTH - self.rect.width

    def draw(self, surface):
        surface.blit(self.image, self.rect)
