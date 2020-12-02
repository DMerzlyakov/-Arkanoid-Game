import pygame as pg
from pygame import Surface, Rect
from pygame.sprite import Sprite, Group

from settings import WIDTH, BALL_SPRITE


class Ball(Sprite):
    """
    Создает объект шарика
    """
    sprite: str = BALL_SPRITE

    color: (int, int, int) = None  # цвет
    speed: float = None  # скорость движения
    dx: int = None  # направление скорости по x
    dy: int = None  # направление скорости по y
    acc: float = None  # ускорение
    image: Surface = None  # поверхность, на которой отрисован шарик
    rect: Rect = None  # объект с размерами и координатами поверхности

    def __init__(self, x: float, y: float, radius: float, color: (int, int, int), *groups: Group):
        super(Ball, self).__init__(*groups)
        self.color = color
        self.speed = 0
        self.dx = 1
        self.dy = -1
        self.acc = 0.02
        self.image = pg.transform.scale(pg.image.load(self.sprite), (int(2 * radius), int(2 * radius))).convert()
        self.rect = self.image.get_rect(center=(x, y))

    def _collide_with(self, sprite: Sprite):
        """
        Изменяет направление движения шарика
        после столкновения
        """
        if self.dx > 0:  # правым ребром
            delta_x = abs(self.rect.right - sprite.rect.left)
        else:  # левым ребром
            delta_x = abs(self.rect.left - sprite.rect.right)

        if self.dy > 0:  # нижним ребром
            delta_y = abs(self.rect.bottom - sprite.rect.top)
        else:  # верхним ребром
            delta_y = abs(self.rect.top - sprite.rect.bottom)

        if abs(delta_x - delta_y) < 8:  # края
            self.dx, self.dy = -self.dx, -self.dy
        elif delta_x > delta_y:  # верх, низ
            self.dy = -self.dy
        elif delta_y > delta_x:  # лево, право
            self.dx = -self.dx

    def _collide(self, paddle: Sprite, blocks: Group) -> (int, int, bool):
        """
        Обрабатывает столкновения шарика
        """
        paddle_collision = 0  # кол-во столкновений с платформой (1 или 0)
        block_collision = 0  # кол-во столкновений с блоками
        dropped = False  # выход за границы игрового поля

        # с краями экрана
        if self.rect.left <= 0:  # левый
            self.dx = abs(self.dx)
        elif self.rect.right >= WIDTH:  # правый
            self.dx = -abs(self.dx)

        if self.rect.top <= 0:  # верхний
            self.dy = abs(self.dy)
        elif self.rect.top >= paddle.rect.top:  # нижний, окончание игры
            dropped = True

        # с платформой
        if pg.sprite.collide_rect(self, paddle):
            paddle_collision += 1
            self._collide_with(paddle)

        # с блоками
        blocks = pg.sprite.spritecollide(self, blocks, dokill=True)
        for block in blocks:
            block_collision += 1
            self._collide_with(block)

        # увеличение скорости
        if paddle_collision and self.speed < 15:
            self.speed += self.acc
            self.acc += 0.0025

        return paddle_collision, block_collision, dropped

    def update(self, paddle: Sprite, blocks: Group) -> tuple[int, int, bool]:
        paddle_collision, block_collision, dropped = self._collide(paddle, blocks)
        self.rect.centerx += self.speed * self.dx
        self.rect.centery += self.speed * self.dy
        return paddle_collision, block_collision, dropped

    def draw(self, surface: Surface):
        # пока используется круг для изоображения шарика
        surface.blit(self.image, self.rect)
