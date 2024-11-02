import pygame
import random

import constants
from constants import FRAME_RATE


class AnimationSequence:
    def __init__(self, name: str, time: float, image_sequence: list[pygame.Surface]):
        # check params type
        if type(name) is not str:
            raise TypeError("'name' has to be string")

        if type(time) is not float:
            raise TypeError("'time' has to be float")

        if type(image_sequence) is not list:
            raise TypeError("'image_sequence' has to be list")

        if not all(isinstance(seq, pygame.Surface) for seq in image_sequence):
            raise TypeError("each of 'image_sequence' has to be string")

        # init fields
        self.name = name
        self.time = time
        self.sequence = image_sequence


class Animation:
    def __init__(self, a_current: str, a_next: str, sequences: list[AnimationSequence]):
        super().__init__()

        # check params type
        if type(a_current) is not str:
            raise TypeError("'a_current' has to be string")

        if type(a_next) is not str:
            raise TypeError("'a_next' has to be string")

        if type(sequences) is not list:
            raise TypeError("'sequences' has to be list")

        if not all(isinstance(seq, AnimationSequence) for seq in sequences):
            raise TypeError("each of 'sequences' has to be AnimationSequence")


        # check for duplicate animation names
        self._anim_seq_names = [seq.name for seq in sequences]
        if len(self._anim_seq_names) != len(set(self._anim_seq_names)):
            dup_names = set([dup for dup in self._anim_seq_names if self._anim_seq_names.count(dup) > 1])
            raise ValueError(f"Duplicate animation names: {dup_names}")

        # initialize params
        self._anim_seq_names = set(self._anim_seq_names)
        self.images = {sequence.name: sequence for sequence in sequences}
        self.animation = a_current
        self.next_animation = a_next
        self.index = 0
        self.index_max = len(self.images[self.animation].sequence)
        self.frame = random.uniform(0, int(FRAME_RATE * self.images[self.animation].time))

    def update(self):
        self.frame = self.frame + 1

        if (self.index + 1) == self.index_max:
            self.state(self.next_animation, self.next_animation)
        else:
            # next animation frame
            self.index = int((self.frame / (constants.FRAME_RATE * self.images[self.animation].time) * (self.index_max - 1)))

    def get_image(self):
        return self.images[self.animation].sequence[self.index]

    def state(self, animation: str, next_animation: str):
        if animation not in self._anim_seq_names:
            raise ValueError(f"State {animation} is not in animations: {self._anim_seq_names}")

        if next_animation not in self._anim_seq_names:
            raise ValueError(f"Next state {next_animation} is not in animations: {self._anim_seq_names}")

        self.animation = animation
        self.next_animation = next_animation
        self.index = 0
        self.index_max = len(self.images[self.animation].sequence)
        self.frame = 0

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, animation: Animation):
        super().__init__()
        self._animation = animation
        self.image = self._animation.get_image()
        self.rect = self.image.get_rect()

    def update(self):
        self._animation.update()
        self.image = self._animation.get_image()

    def animation(self, animation: str, switch_to: str):
        self._animation.state(animation, switch_to)

