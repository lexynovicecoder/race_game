import pygame
import time
import math
from functions import scale_image


GRASS = scale_image(pygame.image.load("grass1.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("track.png"), 0.9)

FINISH = pygame.image.load("finish.png")
TRACK_BOARDER = scale_image(pygame.image.load("track-border.png"), 0.9)

RED_CAR = pygame.image.load("myredcar.jpg")
BLUE_CAR = pygame.image.load('mybluecar.jpg')

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
# getting width and height of track in order to use it to set the width and height of window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Game")

FPS = 60  # setting frame rate
run = True
clock = pygame.time.Clock()
# trying to set the speed of the game so that the speed would be similar on anyone's computer
while run:
    clock.tick(FPS)  # this ensures that loop doesn't run more than 60 frames per second

    WIN.blit(GRASS, (0, 0)) # this means drawing grass image in the window by specifying its coordinates
    WIN.blit(TRACK, (0, 0))
    WIN.blit(FINISH, (0, 0))

    pygame.display.update()  # this command is essential to ensure that anything u 'draw' in pygame is updated in the
    # display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
