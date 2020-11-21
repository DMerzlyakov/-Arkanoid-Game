import pygame as pg
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group
import random

from settings import WIDTH, BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SPRITES


class Block(Sprite):
    """
    Создает объект блока
    """
    sprites: list[str] = BLOCK_SPRITES  # спрайты для блоков с различным количеством hp

    # effect = None
    health: int = None  # hp блока
    sprite: str = None  # путь к спрайту
    image: Surface = None  # поверхность, на которой отрисован блок
    rect: Rect = None  # объект с размерами и координатами поверхности

    def __init__(self, x: float, y: float, width: int, height: int,
                 heath: int = None, effect=None, *groups: Group):

        super(Block, self).__init__(*groups)
        self.effect = effect
        self.health = heath or random.randint(1, len(self.sprites))
        self.sprite = self.sprites[self.health - 1]

        self.image = pg.transform.scale(pg.image.load(self.sprite), (width, height)).convert()
        self.rect = self.image.get_rect(center=(x, y))

    def kill(self):
        """
        Переопределенный метод класса Sprite
        Уменьшает hp блока на 1 пункт. Если hp=0 удаляет объект из всех групп
        """
        self.health -= 1
        if self.health == 0:
            super(Block, self).kill()

    def update(self):
        self.sprite = self.sprites[self.health - 1]
        self.image = pg.transform.scale(pg.image.load(self.sprite), (self.rect.width, self.rect.height)).convert()
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def add_row_blocks(blocks: Group):
    """
    Создает вверху поля ряд заполненный блоками
    """
    space = 10  # расстояние между блоками
    block_list = blocks.sprites()  # список всех, находящихся на экране блоков

    if block_list:  # если есть блоки, то сдвигаем все ряды на 1 вниз
        width = block_list[0].rect.width
        height = block_list[0].rect.height

        for block in block_list:
            block.rect.centery += space + height
    else:
        width = BLOCK_WIDTH
        height = BLOCK_HEIGHT

    count = WIDTH // (width + space)  # кол-во блоков в ряду
    delta = (WIDTH - count * (width + space)) // 2  # расстояние для центрирования ряда

    for i in range(count):
        x = delta + (i * (space + width) + width / 2 + space)
        blocks.add(Block(x, space * 2, width, height))
