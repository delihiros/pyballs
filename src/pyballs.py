import pygame
import random
import math
import sys

BLOCK_SIZE = 32
BLOCK_ROW = 7
SCREEN_HEIGHT = BLOCK_SIZE * 9
SCREEN_WIDTH = BLOCK_SIZE * BLOCK_ROW
BALL_RADIUS = 4
BALL_COLOR = (251, 176, 52)
BLOCK_COLOR = (0, 164, 228)
BACKGROUND_COLOR = (106, 115, 123)
PERIOD = 30
DISPLAY_UPDATE = 1000
GRAVITY = 0.01

pygame.init()
sysfont = pygame.font.Font(
    "/System/Library/Fonts/AquaKana.ttc", int(BLOCK_SIZE/2))


# TODO
class Player():
    def __init__(self):
        return

    def play(self, game):
        game


class Ball():
    def __init__(self, x=SCREEN_WIDTH, y=SCREEN_HEIGHT, dx=0, dy=0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self, blocks):
        old_x = self.x
        old_y = self.y
        self.x += self.dx
        self.y += self.dy

        # collided to wall
        # collided to right or left
        if self.x < 0 or SCREEN_WIDTH <= self.x:
            self.dx = -self.dx
            self.dy += GRAVITY
            self.x += self.dx
        # collided to bottom
        if SCREEN_HEIGHT <= self.y:
            return None
        if self.y < 0:
            self.dy = -self.dy
            self.y += self.dy

        # collided to blocks
        new_blocks = []
        for block in blocks:
            number = block.number
            if number > 0 and self.collided_to_block(block):
                # collided to bottom
                if old_y >= block.y + BLOCK_SIZE \
                        and block.y + BLOCK_SIZE > self.y:
                    number -= 1
                    self.dy = -self.dy
                    self.y += self.dy
                # collided to top
                if old_y < block.y and self.y >= block.y:
                    number -= 1
                    self.dy = -self.dy
                    self.y += self.dy
                # collided to right
                if old_x > block.x + BLOCK_SIZE and \
                        self.x <= block.x + BLOCK_SIZE:
                    number -= 1
                    self.dx = -self.dx + GRAVITY
                    self.x += self.dx
                # collided to left
                if old_x < block.x and self.x >= block.x:
                    number -= 1
                    self.dx = -self.dx
                    self.x += self.dx + GRAVITY
            if number > 0:
                new_blocks.append(
                    Block(number=number, x=block.x, y=block.y))

        return new_blocks

    def collided_to_block(self, block):
        return block.x <= self.x and self.x <= block.x + BLOCK_SIZE \
            and block.y <= self.y and self.y <= block.y + BLOCK_SIZE

    def draw(self, screen):
        pygame.draw.circle(screen, BALL_COLOR,
                           (int(self.x), int(self.y)), BALL_RADIUS)

    def __repr__(self):
        return "<Ball " + ','.join(
            [str(x) for x in [self.x, self.y, self.dx, self.dy]]) + ">"


class Block():
    def __init__(self, number=1, x=0, y=0, add_ball=False):
        self.number = number
        self.x = x
        self.y = y
        self.add_ball = add_ball

    def draw(self, screen):
        if self.add_ball:
            pygame.draw.circle(screen, BLOCK_COLOR,
                               (int(self.x), int(self.y), BALL_RADIUS))
            # number_text = sysfont.render(str(self.number), True, (0, 0, 0))
            # screen.blit(number_text, (int(self.x), int(self.y)))
        else:
            pygame.draw.rect(screen, BLOCK_COLOR, pygame.Rect(
                self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))
            number_text = sysfont.render(str(self.number), True, (0, 0, 0))
            screen.blit(number_text, (int(self.x), int(self.y)))

    def __repr__(self):
        return "<Block " + ','.join(
            [str(x) for x in [self.number, self.x, self.y]]) + ">"


class Game():
    def __init__(self, ball_nums=1,
                 ball_x=SCREEN_WIDTH / 2, ball_y=SCREEN_HEIGHT,
                 difficulty=1):
        self.ball_nums = ball_nums
        self.difficulty = difficulty
        self.blocks = []
        self.set_balls(ball_nums, ball_x, ball_y)

    def set_balls(self, ball_nums, ball_x, ball_y):
        self.balls = [Ball(x=ball_x, y=ball_y) for _ in range(ball_nums)]

    def generate_blocks(self):
        blocks = []
        for idx in range(BLOCK_ROW):
            # if random.random() > 1 / (self.difficulty + 1):
            if random.random() > 1/2:
                if random.random() > 0.5:
                    blocks.append(Block(number=self.difficulty * 2,
                                        x=idx * BLOCK_SIZE, y=BLOCK_SIZE))
                else:
                    blocks.append(Block(number=self.difficulty,
                                        x=idx * BLOCK_SIZE, y=BLOCK_SIZE))
        if len(blocks) == 0:
            blocks = [Block(number=self.difficulty, x=0, y=BLOCK_SIZE)]
        return blocks

    def shifted_block(self, block):
        return Block(number=block.number, x=block.x, y=block.y + BLOCK_SIZE)

    def new_blocks(self, blocks):
        new_blocks = []
        for block in blocks:
            new_blocks.append(self.shifted_block(block))
        new_blocks.extend(self.generate_blocks())
        return new_blocks

    def is_gameover(self):
        for block in self.blocks:
            if block.y == BLOCK_ROW * BLOCK_SIZE:
                return True
        return False

    def play(self, dx=0, dy=-1):
        self.blocks = self.new_blocks(self.blocks)
        self.balls = [Ball(x=ball.x, y=ball.y, dx=dx, dy=dy)
                      for ball in self.balls]
        # until game over

    def play_animation(self, dx=0, dy=-1):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('pyballs')

        self.play(dx=dx, dy=dy)
        ball_ready = self.balls
        self.balls = [ball_ready[0]]
        ball_ready = ball_ready[1:]

        idx = 0
        display_count = 0
        while True:
            display_count += 1
            idx += 1
            self.screen.fill(BACKGROUND_COLOR)
            if len(ball_ready) > 0 and idx > PERIOD:
                idx = 0
                self.balls.append(ball_ready[0])
                ball_ready = ball_ready[1:]

            for block in self.blocks:
                block.draw(self.screen)
            for ball in self.balls:
                ball.draw(self.screen)

            if display_count == DISPLAY_UPDATE:
                pygame.display.update()
                display_count = 0

            old_balls = self.balls
            self.balls = []
            for ball in old_balls:
                result = ball.update(self.blocks)
                if result is not None:
                    self.blocks = result
                    self.balls.append(ball)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if len(self.balls) == 0:
                return
                # pygame.quit()
                # sys.exit()


def __main__():
    current_ball_nums = 2
    game = Game(ball_nums=current_ball_nums)
    while not game.is_gameover():
        print(current_ball_nums)
        rad = math.radians(10)  # degree should be 0 < x < 180
        dx = math.cos(rad)
        dy = -math.sin(rad)
        game.set_balls(current_ball_nums, SCREEN_WIDTH / 2, SCREEN_HEIGHT)
        game.play_animation(dx=dx, dy=dy)
        game.difficulty += 1
        current_ball_nums += 1

    pygame.quit()
    sys.exit()

    return


if __name__ == '__main__':
    __main__()
