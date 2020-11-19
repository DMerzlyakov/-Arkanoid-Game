import pygame as pg
import math

from settings import WIDTH, HEIGHT


class Ball(pg.sprite.Sprite):

    def __init__(self, x, y, radius, color, *groups):
        super(Ball, self).__init__(*groups)
        self.color = color
        self.speedx = self.speedy = 0
        self.acc = 0.01  # TODO: шарик ускоряется с каждым столкновением

        self.image = pg.Surface((radius, radius), pg.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

    def collide(self, paddle, blocks):
        collision = False

        # с границами окна
        if self.rect.x + self.rect.width >= WIDTH or self.rect.x <= 0:
            self.speedx *= -1
            collision = True

        if self.rect.y <= 0 or self.rect.y + self.rect.height >= HEIGHT:
            self.speedy *= -1
            collision = True

        # с доской
        if pg.sprite.collide_rect(self, paddle):
            collision = True
            self.speedy *= -1

        # с блоком
        for block in blocks:
            if pg.sprite.collide_rect(self, block):
                collision = True
                block.kill()
                self.speedy *= -1

        if collision and abs(self.speedx) < 15:
            self.speedx += math.copysign(1, self.speedx) * self.acc
            self.speedy += math.copysign(1, self.speedy) * self.acc

    def update(self, paddle, blocks):
        self.collide(paddle, blocks)
        self.rect.centerx += self.speedx
        self.rect.centery += self.speedy

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
