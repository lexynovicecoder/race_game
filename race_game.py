import pygame
import time
import math
from functions import scale_image, draw

GRASS = scale_image(pygame.image.load("grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("track2.png"), 0.8)

FINISH = pygame.image.load("finish.png")
TRACK_BOARDER = scale_image(pygame.image.load("track2border.png"), 0.8)

RED_CAR = scale_image(pygame.image.load("redcar.png"), 0.25)
BLUE_CAR = scale_image(pygame.image.load('bluecar.png'), 0.25)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
# getting width and height of track in order to use it to set the width and height of window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Game")

FPS = 60  # setting frame rate
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]


# making list that contains some images and their positions, so it can be used in the draw function

class AbstractCar:  # super class to be used by both player car and computer car
    def __init__(self, max_vel, rotation_vel):  # vel meaning velocity
        self.max_vel = max_vel
        self.vel = 0  # zero because at the start your car isn't moving at all
        self.rotation_vel = rotation_vel
        self.angle = 0  # car starts at zero degrees
    def rotate(self, left=False, right=False):
        if left:
            self.angle -= self.rotation_vel
        elif right:
            self.angle += self.rotation_vel
    # this method decreases the car angle when left is True(turning left)
    # and increases the angle when right is True(turning right)


run = True
clock = pygame.time.Clock()
# trying to set the speed of the game so that the speed would be similar on anyone's computer
while run:
    clock.tick(FPS)  # this ensures that loop doesn't run more than 60 frames per second

    draw(WIN, images)  # calling draw function

    pygame.display.update()  # this command is essential to ensure that anything u 'draw' in pygame is updated in the
    # display
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()
