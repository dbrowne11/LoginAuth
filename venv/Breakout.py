import pygame, sys
from random import randint, choice
from math import cos, sin, floor, pi, sqrt
if not pygame.get_init():
    pygame.init()

clock = pygame.time.Clock()
FPS = 30
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Breakout')

black = (0, 0, 0)
cyan = (0, 255, 255)
blue = (0, 0, 255)
orange = (255, 100, 10)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
purple = (160, 32, 240)
gray = (190, 190, 190)
blockColors = [cyan, blue, orange, red, yellow, green, purple]

RESET = -1
GAME_OVER = 0
PLAYING = 1
state = PLAYING

class Ball():
    def __init__(self, paddle):
        self.pos = [randint(15, WIDTH), (HEIGHT // 2) + randint(-20, 20)]
        self.velocity = [4, 5]
        self.hitbox = pygame.draw.rect(screen, red, (0, 0, 10, 10), 1)
        self.paddle = paddle
    def move(self):
        # get x and y value
        x = self.pos[0]
        y = self.pos[1]
        self.hitbox.center = (x, y)
        # collisions with walls
        if (x <= 5):
            self.velocity[0] = -self.velocity[0]
        elif (x >= 635):
           self.velocity[0] = -self.velocity[0]
        elif y <= 5:
            if(self.velocity[1] < 0):
                self.velocity[1] = -self.velocity[1]
            print(self.velocity[1])
        elif y >= 455:
            self.hitPaddle()
            if y > 475:
                return False
        #print(dx, dy)
        # store new x and y
        self.pos[0] = floor(x + self.velocity[0])
        self.pos[1] = floor(y + self.velocity[1])
        return True

    def draw(self):
        pygame.draw.circle(screen, red, (self.pos[0], self.pos[1]), 5)


    def update(self):
        self.draw()
        return self.move()

    def hitPaddle(self):
        reflectShifter = -2
        for segment in self.paddle.paddle:
            if self.hitbox.colliderect(segment):
                self.velocity[0] = self.velocity[0] + reflectShifter
                self.velocity[1] = -abs(self.velocity[1] - reflectShifter)
                return True
            reflectShifter += 1

        return False

    # def hitBlocks(self, blocks):
        # block = self.hitbox.collidelist(blocks.)

class Paddle():
    def __init__(self):
        l2 = pygame.draw.rect(screen, gray, (300, 460, 12, 8))
        l1 = pygame.draw.rect(screen, gray, (310, 460, 12, 8))
        c = pygame.draw.rect(screen, gray, (320, 460, 12, 8))
        r1 = pygame.draw.rect(screen, gray, (330, 460, 12, 8))
        r2 = pygame.draw.rect(screen, gray, (340, 460, 12, 8))
        self.paddle = [l2, l2, c, r1, r2]

    def move(self):
        mousePosX, mousePosY = pygame.mouse.get_pos()
        x = mousePosX - 30
        for i, rect in enumerate(self.paddle):
            rect.center = (x, rect.center[1])
            x += 12

    def draw (self):
        for segment in self.paddle:
            pygame.draw.rect(screen, gray, segment)

    def update(self):
        self.move()
        self.draw()

class Blocks():
    def __init__(self):
        self.level = 1
        self.blocks = []
    def GenerateBlocks(self):
        numBlocks = 16 * self.level
        x, y = 0, 32
        for i in range(numBlocks):
            self.blocks.append(pygame.draw.rect(screen, choice(blockColors),(x, y, 40, 16)))
            if x <= 600:
                x += 40
            else:
                x = 0
                y += 16


    def Draw(self):
        for i, segment in enumerate(self.blocks):
            pygame.draw.rect(screen, blockColors[i % len(blockColors)], segment)

def run():
    paddle = Paddle()
    ball = Ball(paddle)
    blocks = Blocks()
    state = PLAYING
    while True:
        lives = 3
        blocks.GenerateBlocks()
        while state == PLAYING:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(black)
            if not ball.update():
                lives -= 1
                if lives <= 0:
                    state = GAME_OVER
                else:                           #create new ball
                    del ball
                    ball = Ball(paddle)
            paddle.update()
            blocks.Draw()
            font = pygame.font.SysFont('arial', 16)
            text = font.render('Lives: ' + str(lives), True, green, black)
            textRect = text.get_rect()
            textRect.center = (48, 16)
            screen.blit(text, textRect)

            pygame.display.update()
        while state == GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

run()