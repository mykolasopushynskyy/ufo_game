import math

import random
import engine
import utils

import constants
from engine.animated_sprite import AnimationSequence

class UfoAnimation(engine.animated_sprite.Animation):
    def __init__(self):
        super().__init__(
            'idle', 'idle',
            [
                AnimationSequence('idle', 1.0, [
                    utils.load_image('resources/ufo/pixel/ufo_0-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_1-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_2-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_3-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_4-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_5-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_6-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_7-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_8-pixel.png'),
                    utils.load_image('resources/ufo/pixel/ufo_9-pixel.png'),
                ])
            ]
        )

class UfoTrajectoryAroundCity:
    def __init__(self):
        self.l = random.uniform(50, 100)
        self.a = self.l / 5
        self.x = constants.WIDTH + random.uniform(0, constants.WIDTH)
        self.y = random.uniform(0, constants.HEIGHT * 0.40) + 80
        self.x_mod = -random.uniform(1, 10)
        self.y_mod = math.sin(self.x / self.l) * self.a

    def update(self):
        self.x = self.x + self.x_mod
        self.y = self.y
        self.y_mod = math.sin(self.x / self.l) * self.a

    def init(self):
        self.x = constants.WIDTH + random.uniform(0, constants.WIDTH)
        self.y = random.uniform(0, constants.HEIGHT * 0.40) + 80
        self.l = random.uniform(50, 100)
        self.a = self.l / 5
        self.x_mod = -random.uniform(1, 10)
        self.y_mod = math.sin(self.x / self.l) * self.a

    def get_x(self):
        return self.x + self.x_mod

    def get_y(self):
        return self.y + self.y_mod

class Ufo(engine.animated_sprite.AnimatedSprite):
    def __init__(self):
        super().__init__(UfoAnimation())

        self.trajectory = UfoTrajectoryAroundCity()
        self.rect = self.image.get_rect()
        self.rect.x = self.trajectory.get_x()
        self.rect.y = self.trajectory.get_y()

    def update(self):
        super().update()
        self.trajectory.update()

        self.rect.x = self.trajectory.get_x()
        self.rect.y = self.trajectory.get_y()

        if self.rect.x < -self.rect.width:
            self.trajectory.init()
            self.rect = self.image.get_rect()
            self.rect.x = self.trajectory.get_x()
            self.rect.y = self.trajectory.get_y()
