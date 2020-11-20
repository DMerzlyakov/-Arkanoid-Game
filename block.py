import pygame as pg
from pygame.sprite import Group
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


def add_row_blocks(blocks: Group) -> None:
    space = 5
    block_list = blocks.sprites()

    if block_list:
        width = block_list[0].rect.width
        height = block_list[0].rect.height

        for block in block_list:
            block.rect.centery += space + height
    else:
        width = 50
        height = 15

    count = WIDTH // (width + 2 * space)
    delta = (WIDTH - count * (width + space)) // 2

    for i in range(count):
        x = delta + (i * (space + width) + width / 2 + space)
        blocks.add(Block(x, space * 2, width, height))
