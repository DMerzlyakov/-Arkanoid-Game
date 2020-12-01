import pygame as pg
from pygame import Surface
from pygame.font import Font
from pygame.time import Clock
from pygame.event import EventType
from pygame.sprite import Group

from paddle import Paddle
from ball import Ball
from block import add_row_blocks
from score import Score

from settings import *


class Game:
    _display: Surface = None  # игровое окно
    _clock: Clock = None  # объект, отвечающий за частоту обновления окна
    _fps: int = None  # кол-во кадров в секунду

    _start_game: bool = None  # Игра только запустилась или нет
    _pause: bool = None  # игра на паузе или нет
    _game_over: bool = None  # игра закончилась или нет
    _start_speed: float = None  # начальная скорость шарика
    _limit: int = None  # кол-во столкновений шарика с платформой, после которого происходит добавление ряда блоков
    _complexity: float = None  # сложность игры, чем меньше, тем чаще добавляются ряды блоков
    _counter: int = None  # счетчик столкновений шарика с платформой
    _game_win: bool = None

    _paddle: Paddle = None  # объект платформы
    _ball: Ball = None  # объект шарика
    _blocks: Group = None  # группа объектов блоков
    _score: Score = None  # объект счета

    _running: bool = None  # глобальный игровой цикл

    def __init__(self, width: int, height: int, fps: int):
        pg.init()
        self._display = pg.display.set_mode((width, height))
        pg.display.set_caption("Arkanoid")

        self._clock = Clock()
        self._fps = fps

        self._init_objects()

        self._game_win = False
        self._start_game = False
        self._pause = True
        self._game_over = False
        self._start_speed = 8
        self._limit = sum([block.health for block in self._blocks.sprites()])
        self._complexity = 0.5
        self._counter = 0

        self._running = True

    def _init_objects(self):
        """
        Инициализирует все игровые объекты
        """
        paddle_width = self._display.get_width() // 5
        paddle_height = PADDLE_HEIGHT
        paddle_x = self._display.get_width() / 2
        paddle_y = self._display.get_height() - 2 * paddle_height
        paddle_color = PADDLE_COLOR
        self._paddle = Paddle(paddle_x,
                              paddle_y,
                              paddle_width,
                              paddle_height,
                              paddle_color)

        ball_radius = BALL_RADIUS
        ball_color = BALL_COLOR
        self._ball = Ball(self._paddle.rect.centerx,
                          self._paddle.rect.top - ball_radius,
                          ball_radius,
                          ball_color)

        self._blocks = Group()
        [add_row_blocks(self._blocks) for _ in range(4)]  # инициализируем четыре ряда блоков

        self._score = Score(SCORE_FONT, int(self._display.get_width() / 3), SCORE_COLOR)

    def on_event(self, event: EventType):
        """
        Обрабатывает пользовательский ввод
        """
        if event.type == pg.QUIT:
            self._running = False

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_RETURN and self._pause:  # снять паузу по клавише Enter
                self._ball.speed = self._start_speed
                self._pause = False
                self._start_game = True
            elif event.key == pg.K_RETURN and not self._pause:  # поставить паузу по клавише Enter
                self._pause = True
            # elif event.key == pg.K_SPACE and self._game_over:  # Подумать над рестартом игры
            #     pass

    def on_loop(self):
        """
        Обновляет состояния игровых объектов
        """
        if not self._pause and not self._game_over:
            self._paddle.update()
            paddle_collision, block_collision, self._game_over = self._ball.update(self._paddle, self._blocks)
            self._blocks.update()
            self._score.update(block_collision)

            # добавляем новый ряд блоков
            self._counter += paddle_collision
            if self._counter > self._limit * self._complexity or len(self._blocks.sprites()) < 4:
                add_row_blocks(self._blocks)
                self._limit = sum([block.health for block in self._blocks.sprites()])
                self._counter = 0
                if self._complexity > 0.1:
                    self._complexity -= 0.1
                elif self._complexity > 0.04:
                    self._complexity -= 0.02

            if len(self._blocks) == 0:
                self._game_win = True
        if self._pause:
            pass
        if self._game_over:
            pass

    def on_render(self):
        """
        Отрисовывает все игровые объекты
        """
        if not self._start_game:
            pg.font.init()
            text = Font(START_FONT, int(self._display.get_width() / 7))
            image = text.render(START_TEXT, True, (255, 255, 255))
            rect = image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self._display.blit(image, rect)
            pg.display.flip()

        if not self._pause and not self._game_over:
            self._display.fill((3, 3, 3))

            self._score.draw(self._display)
            self._paddle.draw(self._display)
            self._ball.draw(self._display)
            self._blocks.draw(self._display)

            pg.display.flip()
            self._clock.tick(self._fps)

        if self._pause and self._start_game and not self._game_over:
            image = pg.transform.scale(pg.image.load("sprites/pause.png"), (800, 600)).convert()
            image.set_alpha(5)
            rect = image.get_rect(center=(400, 300))
            self._display.blit(image, rect)
            pg.display.flip()
            self._clock.tick(self._fps)

        if self._game_over and self._running:
            self._display.fill((3, 3, 3))
            pg.font.init()
            text = Font(END_FONT, int(self._display.get_width() / 4))
            image = text.render(LOSE_TEXT, True, (255, 255, 255))
            rect = image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            # text_2 = Font("fonts/19783.ttf", int(self._display.get_width() / 10))
            # image_2 = text_2.render("Press Space to new game", True, (97, 97, 97))
            # rect_2 = image_2.get_rect(center=(WIDTH / 2, HEIGHT*2 / 3))
            self._display.blit(image, rect)
            # self._display.blit(image_2, rect_2)
            self._clock.tick(self._fps)
            pg.display.flip()

        if self._game_win and self._running:
            self._display.fill((3, 3, 3))
            pg.font.init()
            text = Font(END_FONT, int(self._display.get_width() / 4))
            image = text.render(WIN_TEXT, True, (255, 255, 255))
            rect = image.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            self._display.blit(image, rect)
            self._clock.tick(self._fps)
            pg.display.flip()

    def on_cleanup(self):
        """
        Завершает работу игры
        """
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
