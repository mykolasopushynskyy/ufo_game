import constants
import engine

from engine import assets
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
                        assets.load_image(
                            "resources/background/background.png", scale_factor
                        )
                    ],
                )
            ],
        )


class AnimatedBackGround(engine.animated_sprite.AnimatedSprite):
    def __init__(self):
        super().__init__(BackgroundAnimation())
        self.rect.topleft = (0, 0)

    def update(self):
        pass
