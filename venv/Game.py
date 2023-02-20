import pygame, sys
from random import randint
import Snake
def play():
    pygame.init()

    # Colors
    black = (0,0,0)
    cyan = (0,255,255)
    blue = (0,0,255)
    orange = (255,100,10)
    red = (255,0,0)
    yellow = (255,255,0)
    green = (0,255,0)
    purple = (160,32,240)
    gray = (190, 190, 190)

    # Set up Window
    clock = pygame.time.Clock()
    FPS = 30
    WIDTH = 640
    HEIGHT = 480
    TILE_SIZE = 10
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Games')

    # Game States
    MENU = 0
    gameState = MENU


    while True:
        while gameState == MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    if(text2Rect.collidepoint(mousePos)):
                        Snake.run(screen)
                    if(text3Rect.collidepoint(mousePos)):
                        Breakout.run()

            screen.fill(black)
            font = pygame.font.SysFont('lucidasans', 32)
            text = font.render('Choose a Game', True, green, black)
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 5)
            screen.blit(text, textRect)

            font2 = pygame.font.SysFont('lucidasans', 32)
            text2 = font2.render('Snake', True, green, black)
            text2Rect = text2.get_rect()
            text2Rect.center = (WIDTH //2, HEIGHT // 5 + 48)
            screen.blit(text2, text2Rect)

            font3 = pygame.font.SysFont('lucidasans', 32)
            text3 = font3.render('Breakout', True, green, black)
            text3Rect = text3.get_rect()
            text3Rect.center = (WIDTH // 2, HEIGHT // 5 + 96)
            screen.blit(text3, text3Rect)

            pygame.display.update()


