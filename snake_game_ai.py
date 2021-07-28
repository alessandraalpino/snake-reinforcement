import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial',25)

#reset

#reward

#play(action) -> direction

# game_iteration

# _is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point','x,y')


# rgb colors
# values between 0 and 255
# colors to use in the game
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2= (0,100,255)
BLACK = (0,0,0)

# set block size
BLOCK_SIZE = 20
SPEED = 20

class SnakeGameAI:
    # set display size
    def __init__(self,w=640,h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
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
        self.frame_iteration = 0


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


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #2.move
        self._move(action) #update the head, we don't use append because we need it in the beggining
        self.snake.insert(0, self.head)

        #3. check if game over
        reward = 0
        game_over = False
        # collision or if the snake does not do anything
        if self._is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        #4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            #remove the last element of the snake
            self.snake.pop()

        #5. update ui and clock
        self._update_ui()
        #control how fast the frame update
        self.clock.tick(SPEED)

        #6. turn game over and score

        return reward, game_over, self.score

    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        #hists boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        #hists itself
        # [1:] because the head is always in the snake, so we exclude the first element
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1, pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display,BLUE2, pygame.Rect(pt.x+4,pt.y+4,12,12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        # 0,0 means upper left
        self.display.blit(text, [0,0])
        # without this command we don't see the changes of score
        pygame.display.flip()

    def _move(self, action):
        # [straight,right,left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn  r -> d -> l -> u
        else: # [0,0,1]
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # left turn  r -> u -> l -> d

        self.direction = new_dir


        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x,y)



