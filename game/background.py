import constants
import engine

from engine import utils
from engine.animated_sprite import AnimationSequence


class BackgroundAnimation(engine.animated_sprite.Animation):
    def __init__(self):
        scale_factor = (constants.WIDTH, constants.HEIGHT)
        super().__init__(
            "idle",
            "idle",
            [
                AnimationSequence(
                    "idle",
                    1.0,
                    [
                        utils.load_image(
                            "resources/back_pixel/back_iteration_1.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_2.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_3.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_4.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_5.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_6.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_7.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_8.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_9.png", scale_factor
                        ),
                        utils.load_image(
                            "resources/back_pixel/back_iteration_10.png", scale_factor
                        ),
                    ],
                )
            ],
        )


class AnimatedBackGround(engine.animated_sprite.AnimatedSprite):
    def __init__(self):
        super().__init__(BackgroundAnimation())
        self.rect.topleft = (0, 0)
