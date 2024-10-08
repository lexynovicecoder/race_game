import pygame
import time
import math
from functions import *
pygame.font.init()

GRASS = scale_image(pygame.image.load("grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("newtrack.png"), 2)

FINISH = pygame.image.load("finish.png")
FINISH_POS = (805, 500)
FINISH_MASK = pygame.mask.from_surface(FINISH)
TRACK_BORDER = scale_image(pygame.image.load("newtrackborder.png"), 2)

TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
# getting the mask of the track border to help in detecting pixel perfect collision

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

RED_CAR = scale_image(pygame.image.load("redcar.png"), 0.15)
BLUE_CAR = scale_image(pygame.image.load('bluecar.png'), 0.17)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
# getting width and height of track in order to use it to set the width and height of window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Game")

images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH,(FINISH_POS)), (TRACK_BORDER, (0, 0))]


# making list that contains some images and their positions, so it can be used in the draw function
class GameInfo:
    LEVELS = 10
    def __init__(self, level=1):
        self.level = level
        self.started = False # to determine if the level has started
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS # checking if the game is finished

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        else:
            return round(time.time() - self.level_start_time)

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
        self.move()
        # we are halfing the negative velocity because when reversing a car you can't go as fast as when moving forward

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

PATH = [(872, 310), (845, 247), (770, 209), (607, 195), (505, 125), (404, 191), (205, 209), (132, 289), (199, 367), (507, 365), (607, 413), (602, 506), (471, 538), (297, 537), (180, 548), (135, 628), (193, 696), (357, 701), (724, 695), (840, 662), (858, 514)]



class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (825, 440)

    def reduce_speed(self):
        self.vel = max((self.vel - self.acceleration) / 2, 0)
        # this is so because if the velocity happens to become negative we don't want to move backwards hence it
         # automatically sets to zero
        self.move()

    def bounce(self):
        self.vel = -self.vel# reverse velocity so if the car hits it moving forward it goes back and vice versa
        self.move()


player_car = PlayerCar(8, 8)


class ComputerCar(AbstractCar):
    IMG = BLUE_CAR
    START_POS = (853, 440)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel) # inheriting the constructor and initializing the attributes needed
        self.path = path
        self.current_point = 0
        self.vel = max_vel


    def draw(self, win):
        super().draw(win)


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

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0

computer_car = ComputerCar(3, 4.5, PATH)

def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    computer_finish_poi = computer_car.collide(FINISH_MASK, *FINISH_POS)
    if computer_finish_poi is not None:
        blit_text_center(WIN, MAIN_FONT, "You lost!")
        pygame.display.update()
        pygame.time.wait(3000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi = player_car.collide(FINISH_MASK, *FINISH_POS)
    if player_finish_poi is not None:
        if player_finish_poi[1] == 0:
            player_car.bounce()
        else:
            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)



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



def draw(win, images, player_car, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)
    # function created to blit images on the screen
    level_text = MAIN_FONT.render(f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))


    vel_text = MAIN_FONT.render(f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()  # this command is essential to ensure that anything u 'draw' in pygame is updated in the
    # display


FPS = 70  # setting frame rate

run = True
clock = pygame.time.Clock()
# trying to set the speed of the game so that the speed would be similar on anyone's computer
game_info = GameInfo()

while run:
    clock.tick(FPS)  # this ensures that loop doesn't run more than 60 frames per second

    draw(WIN, images, player_car, computer_car, game_info)  # calling draw function
    pygame.display.update()

    while not game_info.started:
        blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                game_info.start_level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    computer_car.move()
    move_player(player_car)
    handle_collision(player_car,computer_car,game_info)

    if game_info.game_finished():
        blit_text_center(WIN, MAIN_FONT, "You won the game!")
        pygame.display.update()
        pygame.time.wait(3000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

pygame.quit()
