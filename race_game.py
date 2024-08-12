import pygame
import time
import math
from functions import *

GRASS = scale_image(pygame.image.load("grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("track2.png"), 0.8)

FINISH = pygame.image.load("finish.png")
FINISH_POS = (732.5, 395)
FINISH_MASK = pygame.mask.from_surface(FINISH)
TRACK_BORDER = scale_image(pygame.image.load("track2border.png"), 0.8)

TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
# getting the mask of the track border to help in detecting pixel perfect collision

RED_CAR = scale_image(pygame.image.load("redcar.png"), 0.17)
BLUE_CAR = scale_image(pygame.image.load('bluecar.png'), 0.17)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
# getting width and height of track in order to use it to set the width and height of window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Game")

images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH,(FINISH_POS)), (TRACK_BORDER, (0, 0))]


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

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        # we are halfing the negative velocity because when reversing a car you can't go as fast as when moving forward
        self.move()

    def collide(self, mask, x = 0, y = 0):
       car_mask = pygame.mask.from_surface(self.img)
       offset = (int(self.x - x), int(self.y - y))
       poi = mask.overlap(car_mask, offset)
       return poi

    def move(self):
        radians = math.radians(self.angle)  # this is a special way used to calculate angles in computers
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

PATH = [(794, 323), (794, 323), (785, 273), (760, 236), (703, 176), (671, 150), (622, 117), (549, 92), (498, 80), (439, 78), (392, 79), (305, 92), (268, 94), (213, 108), (188, 124), (194, 151), (234, 182), (293, 207), (316, 223), (332, 254), (309, 304), (256, 321), (216, 328), (178, 354), (148, 385), (152, 420), (215, 445), (268, 453), (332, 460), (397, 476), (401, 524), (385, 570), (358, 606), (300, 653), (261, 697), (225, 745), (240, 799), (285, 849), (342, 845), (384, 823), (424, 794), (489, 798), (538, 817), (603, 837), (668, 823), (696, 782), (705, 721), (740, 679), (779, 646), (809, 593), (818, 540), (808, 485), (798, 405)]



class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (732.5, 340)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration, 0)
        # this is so because if the velocity happens to become negative we don't want to move backwards hence it
         # automatically sets to zero
        self.move()

    def bounce(self):
        self.vel = -self.vel# reverse velocity so if the car hits it moving forward it goes back and vice versa
        self.move()


player_car = PlayerCar(8, 8)


class ComputerCar(AbstractCar):
    IMG = BLUE_CAR
    START_POS = (773, 340)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel) # inheriting the constructor and initializing the attributes needed
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        if y_diff == 0:
            desired_radian_angle = math.pi / 2  # this is done so that a zero division error won't be
            # raised when the difference returns zero and sets the angle to 90 degrees
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)
        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(
                *target):  # the asterisk passes the x and y coordinates as two different arguments to the function
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return
        self.calculate_angle()
        self.update_path_point()
        super().move()


computer_car = ComputerCar(3, 3,  PATH)

def move_player(player_car):
    moved = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()



def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)
    # function created to blit images on the screen
    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()  # this command is essential to ensure that anything u 'draw' in pygame is updated in the
    # display


FPS = 70  # setting frame rate

run = True
clock = pygame.time.Clock()
# trying to set the speed of the game so that the speed would be similar on anyone's computer

while run:
    clock.tick(FPS)  # this ensures that loop doesn't run more than 60 frames per second

    draw(WIN, images, player_car, computer_car)  # calling draw function

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    computer_car.move()

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    finish_poi = player_car.collide(FINISH_MASK, *FINISH_POS)
    if finish_poi != None:
        if finish_poi[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            print("finish")



pygame.quit()
