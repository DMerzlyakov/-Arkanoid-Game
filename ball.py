import pygame as pg
from pygame.sprite import Sprite, Group

from settings import WIDTH


class Ball(Sprite):

    def __init__(self, x, y, radius, color, *groups):
        super(Ball, self).__init__(*groups)
        self.color = color
        self.speed = 0
        self.dx = 1
        self.dy = -1
        self.acc = 0.015

        self.image = pg.Surface((2 * radius, 2 * radius))
        self.rect = self.image.get_rect(center=(x, y))

    def _collide_with(self, sprite: Sprite):
        if self.dx > 0:  # left
            delta_x = abs(self.rect.right - sprite.rect.left)
        else:  # right
            delta_x = abs(self.rect.left - sprite.rect.right)

        if self.dy > 0:  # top
            delta_y = abs(self.rect.bottom - sprite.rect.top)
        else:  # bottom
            delta_y = abs(self.rect.top - sprite.rect.bottom)

        if abs(delta_x - delta_y) < 8:  # edges
            self.dx, self.dy = -self.dx, -self.dy
        elif delta_x > delta_y:  # top, bottom
            self.dy = -self.dy
        elif delta_y > delta_x:  # left, right
            self.dx = -self.dx

    def _collide(self, paddle: Sprite, blocks: Group) -> tuple[int, int, bool]:
        paddle_collision = 0
        block_collision = 0
        dropped = False

        # with screen edges (пока остановился на такой логике)
        if self.rect.left <= 0:  # left
            self.dx = abs(self.dx)
        elif self.rect.right >= WIDTH:  # right
            self.dx = -abs(self.dx)

        if self.rect.top <= 0:  # top
            self.dy = abs(self.dy)
        elif self.rect.top >= paddle.rect.top:  # bottom, game over
            dropped = True

        # with paddle
        if pg.sprite.collide_rect(self, paddle):
            paddle_collision += 1
            self._collide_with(paddle)

        # with blocks
        blocks = pg.sprite.spritecollide(self, blocks, dokill=True)
        for block in blocks:
            block_collision += 1
            self._collide_with(block)

        # speed increase
        if paddle_collision and self.speed < 15:
            self.speed += self.acc

        return paddle_collision, block_collision, dropped

    def update(self, paddle: Sprite, blocks: Group) -> tuple[int, int, bool]:
        paddle_collision, block_collision, dropped = self._collide(paddle, blocks)
        self.rect.centerx += self.speed * self.dx
        self.rect.centery += self.speed * self.dy
        return paddle_collision, block_collision, dropped

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.rect.centerx, self.rect.centery), self.rect.height / 2)
        # screen.blit(self.image, self.rect)
