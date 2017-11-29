import random
import sys
import pygame
from pygame.locals import QUIT

GRAVITY = 0.1
STATE_WIDTH = 7
STATE_HEIGHT = 7
BOX_SIZE = 32
SCREEN_WIDTH = STATE_WIDTH * BOX_SIZE
SCREEN_HEIGHT = STATE_HEIGHT * BOX_SIZE
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT + BOX_SIZE)
BALL_RADIUS = 2
BACKGROUND_COLOR = (85, 66, 54)
BALL_COLOR = ()


def i2xy(i):
    x = i // STATE_WIDTH
    y = i % STATE_HEIGHT
    return (x, y)


def xy2i(x, y):
    return x * STATE_WIDTH + y


class Ball():
    def __init__(self, x=SCREEN_WIDTH / 2, y=0, theta=90):
        self.x = x
        self.y = y
        self.theta = theta

    def update(self):
        self.move()

    def move(self):
        return

    def reflect(self):
        return

    def on_collision(self, obj):
        return

    def judge_collision(self, obj):
        return


class Box():
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def on_collision(self, obj):
        return


class Player():
    def __init__(self):
        return

    def set_theta(self, board, theta):
        return


class Board():
    def __init__(self, difficulty=0):
        self.boxes = []

    def new_row(self, difficulty=0):
        return [random.choice([difficulty, 2 * difficulty, None])
                for _ in range(STATE_WIDTH)]

    def set_state(self, difficulty):
        self.boxes = [None for _ in range(STATE_HEIGHT * (STATE_WIDTH - 1))]

    def update(self):
        self.boxes = self.new_row() + self.state[:-1]


class Game():
    def __init__(self, ballnum=1, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT + BOX_SIZE, theta=90):
        self.board = Board()
        self.balls = [Ball(x=x, y=y, theta=theta) for _ in range(ballnum)]

    def update(self):
        for ball in self.balls:
            ball.update()
            for box in self.board.boxes:
                if ball.judge_collision(box):
                    ball.on_collision()
                    box.on_collision()

    def play_gui(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('balls')

        while True:
            self.screen.fill(BACKGROUND_COLOR)

            for ball in self.balls:
                pygame.draw.circle(self.screen, (255, 255, 0),
                                   (ball.x, ball.y), BALL_RADIUS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()


def __main__():
    game = Game()
    game.play_gui()
    return


if __name__ == '__main__':
    __main__()
