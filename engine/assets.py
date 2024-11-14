import os

import pygame

import constants

_images = {}
_sounds = {}


def load_image(image_file: str, scale_factor: tuple = None):
    if image_file in _images:
        image = _images[image_file]
    else:
        image_file = os.path.join(constants.PROJECT_PATH, image_file)
        image = pygame.image.load(image_file).convert_alpha()

    if scale_factor is not None:
        image = pygame.transform.scale(image, scale_factor)

    _images[image_file] = image
    return image


def load_sound(sound: str):
    if sound in _sounds:
        return _sounds[sound]

    sound = os.path.join(constants.PROJECT_PATH, sound)
    loaded_sound = pygame.mixer.Sound(sound)
    _sounds[sound] = loaded_sound
    return loaded_sound


def read_file_as_string(file_path):
    file_path = os.path.join(constants.PROJECT_PATH, file_path)
    with open(file_path, "r") as file:
        content = file.read()
    return content


def get_abs_path(relative_path: str):
    return os.path.join(constants.PROJECT_PATH, relative_path)
