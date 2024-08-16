import pygame
pygame.font.init()

def scale_image(img, factor):
# function to adjust size of images
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)
    # transforms size of image according to the scale


def blit_rotate_center(win, image, top_left, angle):
    # this rotates the image using its topleft corner but using only this can cause distortions in the image
    rotated_image = pygame.transform.rotate(image, angle)
    # this ensures the image only rotates in the center
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def blit_text_center(win, font, text):
    render = font.render(text, 1, (255, 255, 255))
    win.blit(render, (win.get_width()/2 - render.get_width()/2 , win.get_height()/2 - render.get_height()/2))