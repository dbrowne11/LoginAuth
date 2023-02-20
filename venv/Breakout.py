import pygame, sys
from random import randint, choice
from math import cos, sin, floor, pi, sqrt
if not pygame.get_init():
    pygame.init()

clock = pygame.time.Clock()
FPS = 30
WIDTH = 640
HEIGHT = 480
#screen = pygame.display.set_mode((WIDTH,HEIGHT))
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

RESTART = -1
GAME_OVER = 0
PLAYING = 1
LEVELCOMPLETE = 2

state = PLAYING

class Ball():
    def __init__(self, paddle):
        self.pos = [randint(15, WIDTH), (HEIGHT // 2) + randint(-20, 20)]
        self.velocity = [6, 8]
        self.hitbox = pygame.draw.rect(screen, red, (0, 0, 10, 10), 1)
        self.paddle = paddle

    def move(self, blocks):
        # get x and y value
        x = self.pos[0]
        y = self.pos[1]
        self.hitbox.center = (x, y)

        # collisions with walls
        if (x <= 5):            # left 
            self.velocity[0] = -self.velocity[0]
        elif (x >= 635):        # right
           self.velocity[0] = -self.velocity[0]
        elif y <= 5:            # top
            if(self.velocity[1] < 0):
                self.velocity[1] = -self.velocity[1]
            print(self.velocity[1])
        # Check for paddle contact
        elif y >= 455:
            self.hitPaddle()
            if y > 475:
                return False
        hitBlock = self.hitBlocks(blocks)
        if hitBlock is not None:
            print(hitBlock.top, hitBlock.height, y)
            # Blocks can be hit on the sides or top/bottom, if hit top/bottom flip y velo, else flip x velo
            if (y >= hitBlock.top and y <= hitBlock.top + hitBlock.height):
                print("hit side")
                self.velocity[0] = -self.velocity[0]
            else:
                self.velocity[1] = -self.velocity[1]


        #print(dx, dy)
        # store new x and y
        self.pos[0] = floor(x + self.velocity[0])
        self.pos[1] = floor(y + self.velocity[1])
        return True

    def draw(self):
        pygame.draw.circle(screen, red, (self.pos[0], self.pos[1]), 5)


    def update(self, blocks):
        self.draw()
        return self.move(blocks)

    def hitPaddle(self):
        reflectShifter = -2
        for segment in self.paddle.paddle:
            if self.hitbox.colliderect(segment):
                self.velocity[0] = self.velocity[0] + reflectShifter
                self.velocity[1] = -abs(self.velocity[1] - reflectShifter)
                return True
            reflectShifter += 1

        return False

    def hitBlocks(self, blocks):
        block = self.hitbox.collidelist(blocks.blocks)
        if block != -1:
            blocks.colors.pop(block)
            block = blocks.blocks.pop(block)
            return block
        return None


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
        self.colors = []

    def GenerateBlocks(self, level):
        numBlocks = 16 * level
        x, y = 0, 32
        for i in range(numBlocks):
            self.blocks.append(pygame.draw.rect(screen, choice(blockColors),(x, y, 40, 16)))
            self.colors.append(blockColors[i % len(blockColors)])
            if x <= 600:
                x += 40
            else:
                x = 0
                y += 16

    def Draw(self):
        for color, segment in zip(self.colors, self.blocks):
            pygame.draw.rect(screen, color, segment)

def run(screen):
    globals()['screen'] = screen
    paddle = Paddle()
    ball = Ball(paddle)
    blocks = Blocks()
    state = PLAYING
    level = 1
    while True:
        lives = 3
        blocks.GenerateBlocks(level)
        while state == PLAYING:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(black)
            if not ball.update(blocks):
                lives -= 1
                if lives <= 0:
                    state = GAME_OVER
                else:                           #create new ball
                    del ball
                    ball = Ball(paddle)
            paddle.update()
            blocks.Draw()

            if (len(blocks.blocks) == 0):
                state = LEVELCOMPLETE

            font = pygame.font.SysFont('arial', 16)
            text = font.render('Lives: ' + str(lives), True, green, black)
            textRect = text.get_rect()
            textRect.center = (48, 16)
            screen.blit(text, textRect)

            pygame.display.update()

        while state == LEVELCOMPLETE:
            #print level complete
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(f"Level {level} Complete", True, red, black)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2 - 64)
            screen.blit(text, textRect)
            #print space to continue
            text2 = font.render('Press Space to advance', True, blue, black)
            text2Rect = text2.get_rect()
            text2Rect.center = (WIDTH // 2, HEIGHT // 2 + 32)
            screen.blit(text2, text2Rect)
            #print main menu
            text3 = font.render('Press Escape to return to menu', True, blue, black)
            text3Rect = text3.get_rect()
            text3Rect.center = (WIDTH // 2, HEIGHT // 2 + 80)
            screen.blit(text3, text3Rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        state = PLAYING
                        level += 1
                        lives = 3 
                        del ball
                        ball = Ball(paddle)
                    if event.key == pygame.K_ESCAPE:
                        return
            pygame.display.update()

        while state == GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        level = 1
                        blocks.GenerateBlocks(level)
                        lives=3
                        del ball
                        ball = Ball(paddle)
                        state=PLAYING
                    if event.key == pygame.K_ESCAPE:
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
