import pygame as pg

from paddle import Paddle
from ball import Ball
from block import Block, add_row_blocks
from score import Score

from settings import WIDTH, HEIGHT, FPS


class Game:
    def __init__(self, width, height, fps):
        pg.init()
        self._display = pg.display.set_mode((width, height))
        pg.display.set_caption("Arkanoid")

        self._clock = pg.time.Clock()
        self._fps = fps

        self._init_objects()

        self._pause = True
        self._game_over = False
        self._start_speed = 2.1
        self._limit = sum([block.health for block in self._blocks.sprites()])
        self._complexity = 0.8
        self._counter = 0

        self._running = True

    def _init_objects(self):
        paddle_width = self._display.get_width() // 5
        paddle_height = 15
        paddle_x = self._display.get_width() / 2
        paddle_y = self._display.get_height() - 2 * paddle_height
        paddle_color = (232, 69, 69)
        self._paddle = Paddle(paddle_x,
                              paddle_y,
                              paddle_width,
                              paddle_height,
                              paddle_color)

        ball_radius = 8
        ball_color = (43, 46, 74)
        self._ball = Ball(self._paddle.rect.centerx,
                          self._paddle.rect.top - ball_radius,
                          ball_radius,
                          ball_color)

        self._blocks = pg.sprite.Group()
        [add_row_blocks(self._blocks) for _ in range(5)]

        self._score = Score('Comic Sans MS', int(self._display.get_width() / 1.2), (245, 245, 245))

    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_RETURN and self._pause:
                self._ball.speed = self._start_speed
                self._pause = False

    def on_loop(self):
        if not self._pause:
            self._paddle.update()
            paddle_collision, block_collision, self._game_over = self._ball.update(self._paddle, self._blocks)
            self._blocks.update()
            self._score.update(block_collision)

            self._counter += paddle_collision
            if self._counter > self._limit * self._complexity:
                add_row_blocks(self._blocks)
                self._limit = sum([block.health for block in self._blocks.sprites()])
                self._complexity -= 0.05
                self._counter = 0

        if self._pause:
            pass

        if self._game_over:
            pass

    def on_render(self):
        if not self._pause:
            self._display.fill((255, 255, 255))

            self._score.draw(self._display)
            self._paddle.draw(self._display)
            self._ball.draw(self._display)
            self._blocks.draw(self._display)

            pg.display.flip()
            self._clock.tick(self._fps)

        if self._pause:
            pass

        if self._game_over:
            pass

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
