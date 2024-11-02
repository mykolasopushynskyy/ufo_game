import pygame
import random

def load_image(image_file: str):
    return pygame.image.load(image_file).convert_alpha()

def scale_image_by(image_to_scale, scale_factor: tuple, flip_rnd=False):
    factor, random_factor = scale_factor

    scaled_image = pygame.transform.scale_by(image_to_scale, factor * (1 + random_factor * random.uniform(-1, 1)))

    if flip_rnd:
        scaled_image = pygame.transform.flip(scaled_image, bool(random.getrandbits(1)), False)

    return scaled_image

def scale_image(image_to_scale, scale_factor: tuple):
    scaled_image = pygame.transform.scale(image_to_scale, scale_factor)
    return scaled_image
