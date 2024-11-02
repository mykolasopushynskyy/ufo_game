import os

import pygame
import random
import constants


def load_image(image_file: str, scale_factor: tuple = None):
    image_file = os.path.join(constants.PROJECT_PATH, image_file)

    loaded_image = pygame.image.load(image_file).convert_alpha()
    if scale_factor is None:
        return loaded_image

    return pygame.transform.scale(loaded_image, scale_factor)


def scale_image_by(image_to_scale, scale_factor: tuple, flip_rnd=False):
    factor, random_factor = scale_factor

    scaled_image = pygame.transform.scale_by(
        image_to_scale, factor * (1 + random_factor * random.uniform(-1, 1))
    )

    if flip_rnd:
        scaled_image = pygame.transform.flip(
            scaled_image, bool(random.getrandbits(1)), False
        )

    return scaled_image


def scale_image(image_to_scale, scale_factor: tuple):
    scaled_image = pygame.transform.scale(image_to_scale, scale_factor)
    return scaled_image
