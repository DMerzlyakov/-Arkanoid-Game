import pygame as pg
import random

from settings import WIDTH


class Block(pg.sprite.Sprite):
    colors = [(249, 237, 105), (240, 138, 93), (184, 59, 94), (106, 44, 112)]

    def __init__(self, x, y, width, height, heath=None, effect=None, *groups):
        super(Block, self).__init__(*groups)
        self.effect = effect
        self.health = heath or random.randint(1, len(self.colors))
        self.color = self.colors[self.health - 1]

        self.image = pg.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, y))

    def kill(self):
        self.health -= 1
        if self.health == 0:
            super(Block, self).kill()

    def update(self):
        self.color = self.colors[self.health - 1]
        self.image.fill(self.color)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def create_blocks(width=40, height=15, space=5, rows=6):
    blocks = []
    count = WIDTH // (width + space)
    delta = (WIDTH - count * (width + space)) // 2
    for i in range(rows):
        for j in range(count):
            x = delta + (j * (space + width) + width / 2 + space)
            y = space + (i * (space + height) + height / 2 + space)
            blocks.append(Block(x, y, width, height))

    return blocks
