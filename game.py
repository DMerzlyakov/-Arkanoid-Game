import pygame as pg
from pygame import Surface
from pygame.font import Font
from pygame.time import Clock
from pygame.event import Event
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

    _paddle: Paddle = None  # объект платформы
    _ball: Ball = None  # объект шарика
    _blocks: Group = None  # группа объектов блоков
    _score: Score = None  # объект счета

    _running: bool = None  # глобальный игровой цикл

    def __init__(self, width: int, height: int, fps: int):
        pg.init()
        pg.font.init()
        self._display = pg.display.set_mode((width, height))
        pg.display.set_caption("Arkanoid")

        self._clock = Clock()
        self._fps = fps

        self._init_objects()

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

        self._score = Score(FONT, int(self._display.get_width() / 3), SCORE_COLOR)

    def on_event(self, event: Event):
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
            elif event.key == pg.K_SPACE and self._game_over:  # рестарт игры по клавише Space
                pg.display.flip()
                self._init_objects()
                self._game_over = False
                self._start_game = False
                self._pause = True

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

        if self._pause:
            pass
        if self._game_over:
            pass

    def on_render(self):
        """
        Отрисовывает все игровые объекты
        """
        width, height = self._display.get_width(), self._display.get_height()

        # Старт
        if not self._start_game:
            background = pg.Surface((width, height))
            background.fill(BG_COLOR)
            background_rect = background.get_rect(center=(width / 2, height / 2))

            font_color = (255, 255, 255)
            text = Font(FONT, int(height / 12))
            start = text.render(START_TEXT, True, font_color)
            start_rect = start.get_rect(center=background_rect.center)

            text = Font(FONT, int(height / 12))
            score = text.render(f"ARKANOID    2  0  7  8", True, (234, 236, 35))
            score_rect = score.get_rect(center=(background_rect.centerx, background_rect.centery - 200))

            text = Font(FONT, int(height / 20))
            note = text.render("Notes:", True, font_color)
            note_rect = note.get_rect(center=(background_rect.centerx, background_rect.centery + 150))

            text = Font(FONT, int(height / 50))
            note1 = text.render("    ".join("- use the mouse to control the paddle".split()),
                                True, font_color)
            note1_rect = note1.get_rect(
                midleft=(score_rect.left, note_rect.centery + note_rect.height + text.get_height()))

            note2 = text.render("    ".join("- press ENTER to pause the game".split()),
                                True, font_color)
            note2_rect = note2.get_rect(midleft=(note1_rect.left, note1_rect.centery + 2 * note1_rect.height))

            self._display.blit(background, background_rect)
            self._display.blit(score, score_rect)
            self._display.blit(start, start_rect)
            self._display.blit(note, note_rect)
            self._display.blit(note1, note1_rect)
            self._display.blit(note2, note2_rect)

        # Игра
        if not self._pause and not self._game_over:
            self._display.fill(BG_COLOR)
            self._score.draw(self._display)
            self._paddle.draw(self._display)
            self._ball.draw(self._display)
            self._blocks.draw(self._display)

        # Пауза
        if self._pause and self._start_game and not self._game_over:
            background = pg.Surface((width - 50, height - 50))
            background.fill((55, 55, 55))
            background.set_alpha(5)
            background_rect = background.get_rect(center=(width / 2, height / 2))

            font_color = (255, 255, 255)
            text = Font(FONT, int(height / 6))
            pause = text.render(PAUSE_TEXT, True, (88, 51, 255))
            pause_rect = pause.get_rect(center=background_rect.center)
            
            text = Font(FONT, int(height / 12))
            score = text.render(f"Your score:   {self._score.counter}", True, font_color)
            score_rect = score.get_rect(center=(background_rect.centerx, background_rect.centery - 200))

            text = Font(FONT, int(height / 20))
            note = text.render("Notes:", True, font_color)
            note_rect = note.get_rect(center=(background_rect.centerx, background_rect.centery + 150))

            text = Font(FONT, int(height / 50))
            note1 = text.render("    ".join("- use the mouse to control the paddle".split()),
                                True, font_color)
            note1_rect = note1.get_rect(midleft=(score_rect.left, note_rect.centery + note_rect.height + text.get_height()))

            note2 = text.render("    ".join("- press ENTER to unpause the game".split()),
                                True, font_color)
            note2_rect = note2.get_rect(midleft=(note1_rect.left, note1_rect.centery + 2 * note1_rect.height))

            self._display.blit(background, background_rect)
            self._display.blit(score, score_rect)
            self._display.blit(pause, pause_rect)
            self._display.blit(note, note_rect)
            self._display.blit(note1, note1_rect)
            self._display.blit(note2, note2_rect)

        # Конец игры
        if self._game_over and self._running:
            background = pg.Surface((width, height))
            background.fill(BG_COLOR)
            background_rect = background.get_rect(center=(width / 2, height / 2))

            font_color = (255, 255, 255)
            text = Font(FONT, int(height / 6))
            end = text.render(END_TEXT, True, (252, 57, 31))
            end_rect = end.get_rect(center=background_rect.center)

            text = Font(FONT, int(height / 12))
            score = text.render(f"Your score:   {self._score.counter}", True, font_color)
            score_rect = score.get_rect(center=(background_rect.centerx, background_rect.centery - 200))

            text = Font(FONT, int(height / 20))
            note = text.render("Notes:", True, font_color)
            note_rect = note.get_rect(center=(background_rect.centerx, background_rect.centery + 150))

            text = Font(FONT, int(height / 50))
            note1 = text.render("    ".join("- use the mouse to control the paddle".split()),
                                True, font_color)
            note1_rect = note1.get_rect(
                midleft=(score_rect.left, note_rect.centery + note_rect.height + text.get_height()))

            note2 = text.render("    ".join("- press SPACE to restart the game".split()),
                                True, font_color)
            note2_rect = note2.get_rect(midleft=(note1_rect.left, note1_rect.centery + 2 * note1_rect.height))

            self._display.blit(background, background_rect)
            self._display.blit(score, score_rect)
            self._display.blit(end, end_rect)
            self._display.blit(note, note_rect)
            self._display.blit(note1, note1_rect)
            self._display.blit(note2, note2_rect)

        pg.display.flip()
        self._clock.tick(self._fps)

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
