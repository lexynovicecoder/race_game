import pygame
import time
import math
from functions import *

GRASS = scale_image(pygame.image.load("grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("track2.png"), 0.8)

FINISH = pygame.image.load("finish.png")
TRACK_BOARDER = scale_image(pygame.image.load("track2border.png"), 0.8)

RED_CAR = scale_image(pygame.image.load("redcar.png"), 0.17)
BLUE_CAR = scale_image(pygame.image.load('bluecar.png'), 0.17)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
# getting width and height of track in order to use it to set the width and height of window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Game")

FPS = 60  # setting frame rate
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]


# making list that contains some images and their positions, so it can be used in the draw function


class AbstractCar:  # super class to be used by both player car and computer car
    def __init__(self, max_vel, rotation_vel):  # vel meaning velocity
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0  # zero because at the start your car isn't moving at all
        self.rotation_vel = rotation_vel
        self.angle = 0  # car starts at zero degrees
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    # this method increases the car angle when left is True(turning left)
    # and decreases the angle when right is True(turning right)

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        # this method says that if the car's velocity becomes greater than the maximum velocity it should move with
        # the maximum velocity but if not it should keep accelerating
        self.move()

    def move(self):
        radians = math.radians(self.angle)  # this is a special way used to calculate angles in computers
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration, 0)
        # this is so because if the velocity happens to become negative we don't want to move backwards hence it
         # automatically sets to zero
        self.move()


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (732.5, 322)


player_car = PlayerCar(4, 4)


def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)
    # function created to blit images on the screen
    player_car.draw(win)
    pygame.display.update()  # this command is essential to ensure that anything u 'draw' in pygame is updated in the
    # display


run = True
clock = pygame.time.Clock()
# trying to set the speed of the game so that the speed would be similar on anyone's computer

while run:
    clock.tick(FPS)  # this ensures that loop doesn't run more than 60 frames per second

    draw(WIN, images, player_car)  # calling draw function

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        player_car.move_forward()
    if not keys[pygame.K_UP]:
        player_car.reduce_speed()

pygame.quit()
