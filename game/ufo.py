import math

import random
import engine

import constants
from engine import assets
from engine.animated_sprite import AnimationSequence


class UfoAnimation(engine.animated_sprite.Animation):
    def __init__(self):
        super().__init__(
            "idle",
            "idle",
            [
                AnimationSequence(
                    "idle",
                    1.0,
                    [
                        assets.load_image("resources/ufo/ufo_new.png"),
                    ],
                ),
                AnimationSequence(
                    "hit",
                    1.0,
                    [
                        assets.load_image("resources/ufo/ufo_hit_1.png"),
                        assets.load_image("resources/ufo/ufo_hit_2.png"),
                        assets.load_image("resources/ufo/ufo_hit_3.png"),
                        assets.load_image("resources/ufo/ufo_hit_4.png"),
                        assets.load_image("resources/ufo/ufo_hit_5.png"),
                        assets.load_image("resources/ufo/ufo_hit_6.png"),
                        assets.load_image("resources/ufo/ufo_hit_7.png"),
                        assets.load_image("resources/ufo/ufo_hit_8.png"),
                        assets.load_image("resources/ufo/ufo_hit_9.png"),
                        assets.load_image("resources/ufo/ufo_hit_10.png"),
                    ],
                ),
            ],
        )


class UfoTrajectoryAroundCity:
    def __init__(self):
        self.l = random.uniform(50, 100)
        self.a = self.l / 2
        self.x = constants.WIDTH + random.uniform(0, constants.WIDTH)
        self.y = random.uniform(0, constants.HEIGHT * 0.40) + 80
        self.x_mod = -random.uniform(1, 5)
        self.y_mod = math.sin(self.x / self.l) * self.a

    def update(self):
        self.x = self.x + self.x_mod
        self.y = self.y
        self.y_mod = math.sin(self.x / self.l) * self.a

    def init(self):
        self.x = constants.WIDTH + random.uniform(0, constants.WIDTH)
        self.y = random.uniform(0, constants.HEIGHT * 0.40) + 80
        self.l = random.uniform(50, 100)
        self.a = self.l / 2
        self.x_mod = -random.uniform(1, 5)
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
            self.reset()

    def hit(self):
        super().animation("hit", lock_animation=True, callback=lambda: self.reset())

    def reset(self):
        self.trajectory.init()
        super().animation("idle", "idle")
        self.rect = self.image.get_rect()
        self.rect.x = self.trajectory.get_x()
        self.rect.y = self.trajectory.get_y()
