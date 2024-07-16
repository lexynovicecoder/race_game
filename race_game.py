import pygame
import time
import math

GRASS = pygame.image.load("grass1.jpg")
TRACK = pygame.image.load("track.png")

FINISH = pygame.image.load("finish.png")
TRACK_BOARDER = pygame.image.load("track-border.png")

RED_CAR = pygame.image.load("myredcar.jpg")
BLUE_CAR = pygame.image.load('mybluecar.jpg')

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
# getting width and height of track in order to use it to set the width and height of window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Game")

# creating while loop to run the window continuously
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break # writing condition to close window when the close button on the window box is clicked
pygame.quit()
