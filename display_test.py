import pygame
from pygame.locals import *
pygame.init()
WIDTH = 1280
HEIGHT = 1080
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
img = pygame.image.load("myimage.jpg")
while True:
        events = pygame.event.get()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        windowSurface.blit(img, (0, 0)) #Replace (0, 0) with desired coordinates
        pygame.display.flip()
