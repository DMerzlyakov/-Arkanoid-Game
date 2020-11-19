import pygame as pg
from paddle import Paddle
from ball import Ball
from block import Block, create_blocks

from settings import WIDTH, HEIGHT, FPS


class Game:
    def __init__(self, width, height, fps):
        pg.init()
        self.size = self.width, self.height = width, height
        self._display = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Arkanoid")

        self._clock = pg.time.Clock()
        self._fps = fps

        self._paddle = Paddle(100, 550, 100, 20, (255, 0, 255))
        self._ball = Ball(100, 480, 10, (255, 255, 0))
        self._blocks = pg.sprite.Group(*create_blocks())

        self._pause = True
        self._speed = 2

        self._running = True

    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_RETURN and self._pause:
                self._ball.speedx = self._ball.speedy = self._speed
                self._pause = False

    def on_loop(self):
        self._paddle.update()
        self._ball.update(self._paddle, self._blocks)

    def on_render(self):
        self._display.fill((255, 255, 255))

        self._paddle.draw(self._display)
        self._ball.draw(self._display)
        self._blocks.draw(self._display)

        pg.display.update()
        self._clock.tick(self._fps)

    def on_cleanup(self):
        pg.quit()

    def on_execute(self):
        while self._running:
            for event in pg.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == '__main__':
    game = Game(WIDTH, HEIGHT, FPS)
    game.on_execute()
