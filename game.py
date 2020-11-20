import pygame as pg
from paddle import Paddle
from ball import Ball
from block import Block, create_blocks

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
        self._counter = 0

        self._running = True

    def _init_objects(self):
        paddle_width = self._display.get_width() // 5
        paddle_height = 15
        paddle_x = self._display.get_width() / 2
        paddle_y = self._display.get_height() - 2 * paddle_height
        paddle_color = (232, 69, 69)
        self._paddle = Paddle(paddle_x, paddle_y, paddle_width, paddle_height, paddle_color)

        ball_radius = 15
        ball_color = (43, 46, 74)
        self._ball = Ball(self._paddle.rect.centerx,
                          self._paddle.rect.top - ball_radius / pow(2, 1/2),
                          ball_radius,
                          ball_color)

        self._blocks = pg.sprite.Group(*create_blocks())
        self._score = 0  # TODO: объект

    def on_game(self):
        self._paddle.update()
        paddle_collision, block_collision, game_over = self._ball.update(self._paddle, self._blocks)
        self._blocks.update()
        self._score += block_collision  # TODO: метод update

        self._counter += paddle_collision
        self._game_over = game_over

    def on_pause(self):
        pass

    def on_game_over(self):
        pass

    def on_event(self, event):
        if event.type == pg.QUIT:
            self._running = False

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_RETURN and self._pause:
                self._ball.speed = self._start_speed
                self._pause = False

    def on_loop(self):
        if not self._pause:
            self.on_game()

        if self._pause:
            self.on_pause()

        if self._game_over:
            self.on_game_over()

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
