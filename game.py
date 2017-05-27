# -*- coding: utf-8 -*-
# @Last Modified    : 5/17/2017 1:25 PM
# @Author  : Snow
# @email   : liuxx@nlp.nju.edu.cn
# @Description:

import pygame
from pygame.locals import *
import sys

BLACK = (0, 0, 0)
White = (255, 255, 255)

SCREEN_SIZE = [320, 400]
BAR_SIZE = [20, 5]
BALL_SIZE = [15, 15]
MOVE_SIZE = 2


class Game(object):
    def __init__(self):
        pygame.init()   # init import module
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('First Simple Game')
        # init first position
        self.ball_pos_x = SCREEN_SIZE[0]//2 - BALL_SIZE[0]//2
        self.ball_pos_y = SCREEN_SIZE[1]//2 - BALL_SIZE[1]//2
        # init ball move direction
        self.ball_dir_x = -1  # -1 = left, 1 = right
        self.ball_dir_y = -1  # -1 = up, 1 = down
        self.ball_pos = pygame.Rect(self.ball_pos_x, self.ball_pos_y, BALL_SIZE[0], BALL_SIZE[1])

        self.score = 0
        self.bar_pos_x = SCREEN_SIZE[0]//2 - BAR_SIZE[0]//2
        self.bar_pos = pygame.Rect(self.bar_pos_x, SCREEN_SIZE[1]-BAR_SIZE[1], BAR_SIZE[0], BAR_SIZE[1])

    def bar_move_left(self):
        self.bar_pos_x -= MOVE_SIZE

    def bar_move_right(self):
        self.bar_pos_x += MOVE_SIZE

    def run(self):
        pygame.mouse.set_visible(True)
        bar_move_left = False
        bar_move_right = False
        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # left key down, move left, left key up, stop move to left
                elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
                    bar_move_left = True
                elif event.type == pygame.KEYUP and event.key == K_LEFT:
                    bar_move_left = False
                elif event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                    bar_move_right = True
                elif event.type == pygame.KEYUP and event.key == K_RIGHT:
                    bar_move_right = False

            if bar_move_left is True and bar_move_right is False:
                self.bar_move_left()
            elif bar_move_right is True and bar_move_left is False:
                self.bar_move_right()

            self.screen.fill(BLACK)
            self.bar_pos.left = self.bar_pos_x
            pygame.draw.rect(self.screen, White, self.bar_pos)

            # block will move every time step
            self.ball_pos.left += self.ball_dir_x * 2
            self.ball_pos.bottom += self.ball_dir_y * 3
            pygame.draw.rect(self.screen, White, self.ball_pos)

            if self.ball_pos.top <= 0 or self.ball_pos.bottom >= (SCREEN_SIZE[1] - BAR_SIZE[1] + 1):
                self.ball_dir_y *= -1

            if self.ball_pos.left <= 0 or self.ball_pos.right >= (SCREEN_SIZE[0]):
                self.ball_dir_x *= -1

            if self.bar_pos.top <= self.ball_pos.bottom and (
                    self.bar_pos.left < self.ball_pos.right and self.bar_pos.right > self.ball_pos.left):
                self.score += 1
                print("Score: ", self.score, end='\r')
            elif self.bar_pos.top <= self.ball_pos.bottom and (
                    self.bar_pos.left > self.ball_pos.right or self.bar_pos.right < self.ball_pos.left):
                print("Game Over, Score is: ", self.score)
                return self.score

            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()






