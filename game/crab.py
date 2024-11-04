import pygame
import constants
import engine

from engine import assets
from engine.animated_sprite import AnimationSequence


class CrabAnimation(engine.animated_sprite.Animation):
    def __init__(self):
        super().__init__(
            "idle",
            "idle",
            [
                AnimationSequence(
                    "idle",
                    1.0,
                    [
                        assets.load_image("resources/crab_idle_pixel/idle-1.png"),
                        assets.load_image("resources/crab_idle_pixel/idle-2.png"),
                        assets.load_image("resources/crab_idle_pixel/idle-3.png"),
                        assets.load_image("resources/crab_idle_pixel/idle-4.png"),
                        assets.load_image("resources/crab_idle_pixel/idle-5.png"),
                    ],
                ),
                AnimationSequence(
                    "jump",
                    0.25,
                    [
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000000.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000001.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000002.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000003.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000004.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000005.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000006.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000007.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000008.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000009.png"
                        ),
                        assets.load_image(
                            "resources/crab_jump_pixel/ss-0000000010.png"
                        ),
                    ],
                ),
            ],
        )


class Crab(engine.animated_sprite.AnimatedSprite):
    def __init__(self):
        super().__init__(CrabAnimation())

        self.rect.topleft = (
            (constants.WIDTH - self.rect.width) / 2,
            constants.HEIGHT - self.rect.height,
        )
        self.jump_power = -10
        self.gravity = 0.8
        self.jumping = False
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        # self.animation.update()
        super().update()
        self.image = self._animation.get_image()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE]:
            self.jump()

        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y
        if self.rect.y > constants.HEIGHT - self.rect.height - 100:
            self.rect.y = constants.HEIGHT - self.rect.height - 100

    def jump(self):
        self.velocity.y = self.jump_power
        super().animation("jump", "idle")

    def land(self):
        self.velocity.y = 0
        super().animation("jump", "idle")
