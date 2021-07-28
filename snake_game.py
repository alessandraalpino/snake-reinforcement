import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point','x,y')

# set block size
BLOCK_SIZE = 20

class SnakeGame:
    # set display size
    def __init__(self,w=640,h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT
        # put snake in the center of the display
        self.head = Point(self.w/2, self.h/2)
        # creating the initial snake with the head plus 2 blocks for the body
        self.snake = [self.head,
                        Point(self.head.x-BLOCK_SIZE,self.head.y),
                        Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]

        # set initial score to 0 and no food
        self.score = 0
        self.food = None
        # place food in the display
        self._place_food()

    def _place_food(self):
        # food will be a random point inside the display size
        # self.w - BLOCK_SIZE -> to ensure that the point will be inside the display
        # we use // BLOCK_SIZE to garantee that the max value will be multiple of BLOCK_SIZE
        # (self.w - BLOCK_SIZE) // BLOCK_SIZE ) this represents the amount of blocks that fit the display
        # * BLOCK_SIZE is to get the final value in pixels
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE ) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE ) * BLOCK_SIZE
        self.food = Point(x,y)
        # check if food is inside the snake
        if self.food in self.snake:
            self.place_food()


    def play_step(self):
        # 1. collect user input

        #2.move

        #3. check if game over

        #4. place new food or just move

        #5. update ui and check

        #6. turn game over and score
        game_over = False
        return game_over, self.score



if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

        # break if game over
    print(f'Final Score: {score}')

    pygame.quit()


