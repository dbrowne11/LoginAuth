import pygame, sys
from random import randint

class Snake():
    """
    Class containing everything for the snake
    """
    def __init__(self, dir=None):
        self.segments = list()
        self.dirs = list()
        self.bodyLen = 0

    def Move(self, dir=None):
        """
        Logic to move the snake
        :param dir: Can be called with a direction (left, right up down) to turn the snake.  These directions are defined within this file
        :return: True if a collision has occured, False otherwise
        """
        if dir is None:
            dir = self.dirs[0]
            if dir == 0:
                return
        if dir == left and self.dirs[0] == right or dir == right and self.dirs[0] == left:
            return True
        elif dir == up and self.dirs[0] == down or dir == down and self.dirs[0] == up:
            return True
        self.dirs.insert(0, dir)
        self.dirs.pop(-1)
        for i, rect in enumerate(self.segments):
            rect.move_ip(self.dirs[i])
        return self.Collision()

    def InitializeSnake(self):
        """
        Initializes the snakes body and sets up beginning state
        :return: None
        """
        body0 = pygame.draw.rect(screen, purple, (320, 240, TILE_SIZE, TILE_SIZE))  # initialize at center
        self.segments.append(body0)
        self.dirs.append(0)

    def Draw(self):
        """
        Draws the snake
        :return: None
        """
        for segment in self.segments:
            pygame.draw.rect(screen, purple, segment)

    def Eat(self):
        """
        Grows the snake after eating a 'fruit', adds the snakes new segments and updates neccessary data
        :return: None
        """
        dir = self.dirs[-1]
        x, y, trash1, trash2 = self.segments[-1]
        x -= dir[0]
        y -= dir[1]
        add = pygame.draw.rect(screen, purple, (x, y, TILE_SIZE, TILE_SIZE))
        self.segments.append(add)
        self.dirs.append(dir)

    def Collision(self):
        """
        Checks if the snake has collided with anything
        :return: True if a collision has occured, false otherwise
        """
        head = self.segments[0]
        if head[0] < 0 or head[0] > 635:
            return True
        elif head[1] < 0 or head[1] > 475:
            return True
        elif head.collidelist(self.segments[1::]) != -1:
            return True
        else:
            return False

    def Score(self):
        """
        Keeps track of and prints score
        :return: None
        """
        font = pygame.font.SysFont('arial', 16)
        text = font.render(str(len(self.segments) - 1), True, yellow, black)
        textRect = text.get_rect()
        textRect.center = (16, 16)
        screen.blit(text, textRect)


# Functions
def GenerateFood():
    """
    Generates food, determining its random position
    :return: tuple containing food's x and y coords
    """
    x = randint(1, 62)
    y = randint(1, 46)
    pygame.draw.circle(screen, cyan, (x * 10, y * 10), 5)
    return (x * 10, y * 10)


def DrawFood(pos):
    """
    draws food at a given position
    :param pos: tuple containing x, y pos
    :return: None
    """
    pygame.draw.circle(screen, cyan, pos, 5)

PLAYING = 1
GAME_OVER = 0
RESTART = -1
black = (0, 0, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
orange = (255, 100, 10)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
purple = (160, 32, 240)
gray = (190, 190, 190)

# Directions
left = (-10, 0)
right = (10, 0)
up = (0, -10)
down = (0, 10)

clock = pygame.time.Clock()
FPS = 30
WIDTH = 640
HEIGHT = 480
TILE_SIZE = 10
def run(screen):
    """
    Runs the game snake
    :param screen: Pygame window to run snake on
    :return: None
    """
    # Set up Window
    globals()['screen'] = screen
    pygame.display.set_caption('Snake')

    gameState = PLAYING
    food = False
    initialized = False
    while True:
        while gameState == PLAYING:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        end = player.Move(left)
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        end = player.Move(right)
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        end = player.Move(up)
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        end = player.Move(down)

            screen.fill(black)
            if initialized == False:
                player = Snake()
                player.InitializeSnake()
                initialized = True
            if food == False:
                foodPos = GenerateFood()
                food = True
            player.Draw()
            end = player.Move()
            DrawFood(foodPos)
            player.Score()
            if end:
                gameState = GAME_OVER
            if player.segments[0].collidepoint((foodPos[0] - 5, foodPos[1])) or \
                    player.segments[0].collidepoint((foodPos[0] + 5, foodPos[1])) or \
                    player.segments[0].collidepoint((foodPos[0], foodPos[1] + 5)) or \
                    player.segments[0].collidepoint((foodPos[0], foodPos[1] - 5)):
                player.Eat()
                food = False

            pygame.display.update()


        while gameState == GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameState = RESTART
                    if event.key == pygame.K_ESCAPE:
                        del player
                        initialized = False
                        food = False
                        return
            #print game over
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('Game Over', True, red, black)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2 - 64)
            screen.blit(text, textRect)
            #print space to restart
            text2 = font.render('Press Space to Restart', True, blue, black)
            text2Rect = text2.get_rect()
            text2Rect.center = (WIDTH // 2, HEIGHT // 2 + 32)
            screen.blit(text2, text2Rect)
            #print main menu
            text3 = font.render('Press Escape to return to menu', True, blue, black)
            text3Rect = text3.get_rect()
            text3Rect.center = (WIDTH // 2, HEIGHT // 2 + 80)
            screen.blit(text3, text3Rect)

            pygame.display.update()

            while gameState == RESTART:
                print('restarting')
                del player
                initialized = False
                food = False
                gameState = PLAYING
