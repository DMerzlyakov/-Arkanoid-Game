import pygame as pg
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group
import random

from settings import WIDTH, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SPRITES


class Block(Sprite):
    sprites: list[str] = BLOCK_SPRITES

    # effect = None
    health: int = None
    sprite: str = None
    image: Surface = None
    rect: Rect = None

    def __init__(self, x: float, y: float, width: int, height: int,
                 heath: int = None, effect=None, *groups: Group):
        super(Block, self).__init__(*groups)
        self.effect = effect
        self.health = heath or random.randint(1, len(self.sprites))
        self.sprite = self.sprites[self.health - 1]

        self.image = pg.transform.scale(pg.image.load(self.sprite), (width, height)).convert()
        self.rect = self.image.get_rect(center=(x, y))

    def kill(self):
        self.health -= 1
        if self.health == 0:
            super(Block, self).kill()

    def update(self):
        pass
        self.sprite = self.sprites[self.health - 1]
        self.image = pg.transform.scale(pg.image.load(self.sprite), (self.rect.width, self.rect.height)).convert()
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def add_row_blocks(blocks: Group):
    space = 10
    block_list = blocks.sprites()

    if block_list:
        width = block_list[0].rect.width
        height = block_list[0].rect.height

        for block in block_list:
            block.rect.centery += space + height
    else:
        width = BLOCK_WIDTH
        height = BLOCK_HEIGHT

    count = WIDTH // (width + space)
    delta = (WIDTH - count * (width + space)) // 2

    for i in range(count):
        x = delta + (i * (space + width) + width / 2 + space)
        blocks.add(Block(x, space * 2, width, height))
