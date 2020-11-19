import pygame as pg
import random

from settings import WIDTH


class Block(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, color, effect, *groups):
        super(Block, self).__init__(*groups)
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.effect = effect  # TODO: бонусы, которые могут выпасть при разрушении блока
        self.health = 1

    def update(self):
        """
        TODO: реализовать смену цвета для блоков с жизнями
        """
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def create_blocks(width=40, height=15, space=5, rows=7):
    blocks = []
    count = WIDTH // (width + space)
    delta = (WIDTH - count * (width + space)) // 2
    for i in range(rows):
        # color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        color = random.choice(list(pg.color.THECOLORS.values()))
        for j in range(count):
            x = delta + (j * (space + width) + width / 2 + space)
            y = space + (i * (space + height) + height / 2 + space)
            blocks.append(Block(x, y, width, height, color, False))

    return blocks
