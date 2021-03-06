import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial',25)


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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        #2.move
        self._move(self.direction) #update the head, we don't use append because we need it in the beggining
        self.snake.insert(0, self.head)

        #3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        #4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            #remove the last element of the snake
            self.snake.pop()

        #5. update ui and clock
        self._update_ui()
        #control how fast the frame update
        self.clock.tick(SPEED)

        #6. turn game over and score

        return game_over, self.score

    def _is_collision(self):
        #hists boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        #hists itself
        # [1:] because the head is always in the snake, so we exclude the first element
        if self.head in self.snake[1:]:
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

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x,y)



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


