import math
import random

import constants
import engine
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
                    0.5,
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
    def __init__(self, w: int, h: int):
        self.w = w
        self.h = h

        self.choice = random.choice([-1, 1])
        self.x_mod = self.choice * random.uniform(1, 5)
        self.x = -(
            self.choice - 1
        ) / 2 * constants.WIDTH - self.choice * random.uniform(self.w, constants.WIDTH)

        self.l = random.uniform(50, 100)
        self.a = self.l / 2 if random.uniform(0, 100) > 80 else 0
        self.y = random.uniform(0, constants.HEIGHT * 0.40) + 80
        self.y_mod = math.sin(self.x / self.l) * self.a

    def update(self):
        self.x = self.x + self.x_mod
        self.y = self.y
        self.y_mod = math.sin(self.x / self.l) * self.a

    def reset(self):
        self.choice = random.choice([-1, 1])
        self.x_mod = self.choice * random.uniform(1, 5)
        self.x = -(
            self.choice - 1
        ) / 2 * constants.WIDTH - self.choice * random.uniform(self.w, constants.WIDTH)

        self.l = random.uniform(50, 100)
        self.a = self.l / 2 if random.uniform(0, 100) > 20 else 0
        self.y = random.uniform(0, constants.HEIGHT * 0.40) + 80
        self.y_mod = math.sin(self.x / self.l) * self.a

    def get_x(self):
        return self.x + self.x_mod

    def get_y(self):
        return self.y + self.y_mod

    def is_outside(self):
        return self.get_x() < -self.w or self.get_x() > constants.WIDTH + self.w


class Ufo(engine.animated_sprite.AnimatedSprite):
    def __init__(self):
        super().__init__(UfoAnimation())

        self.rect = self.image.get_rect()
        self.trajectory = UfoTrajectoryAroundCity(self.rect.w, self.rect.h)
        self.rect.x = self.trajectory.get_x()
        self.rect.y = self.trajectory.get_y()
        self.is_hit = False

    def update(self):
        super().update()
        self.trajectory.update()

        self.rect.x = self.trajectory.get_x()
        self.rect.y = self.trajectory.get_y()

        if self.trajectory.is_outside():
            self.reset()

    def hit(self):
        super().animation("hit", lock_animation=True, callback=lambda: self.reset())
        if not self.is_hit:
            self.trajectory.x_mod = self.trajectory.x_mod / 2
            self.is_hit = True

    def reset(self):
        self.trajectory.reset()
        self.is_hit = False
        super().animation("idle", "idle")
        self.rect = self.image.get_rect()
        self.rect.x = self.trajectory.get_x()
        self.rect.y = self.trajectory.get_y()
