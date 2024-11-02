import engine.animated_sprite
import pygame
import constants
from constants import WIDTH, HEIGHT
from engine import utils
from engine.animated_sprite import AnimationSequence
from ufo import UfoAnimation, Ufo


class BackgroundAnimation(engine.animated_sprite.Animation):
    def __init__(self):
        super().__init__(
            'idle', 'idle',
            [
                AnimationSequence('idle', 1.0, [
                    utils.load_image('resources/back_pixel/back_iteration_1.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_2.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_3.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_4.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_5.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_6.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_7.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_8.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_9.png', (WIDTH, HEIGHT)),
                    utils.load_image('resources/back_pixel/back_iteration_10.png', (WIDTH, HEIGHT)),
                ])
            ]
        )

class AnimatedBackGroud(engine.animated_sprite.AnimatedSprite):
    def __init__(self):
        super().__init__(BackgroundAnimation())
        self.rect.topleft = (0, 0)


class CrabAnimation(engine.animated_sprite.Animation):
    def __init__(self):
        super().__init__(
            'idle', 'idle',
            [
                AnimationSequence('idle', 1.0, [
                    utils.load_image('resources/crab_idle_pixel/idle-1.png'),
                    utils.load_image('resources/crab_idle_pixel/idle-2.png'),
                    utils.load_image('resources/crab_idle_pixel/idle-3.png'),
                    utils.load_image('resources/crab_idle_pixel/idle-4.png'),
                    utils.load_image('resources/crab_idle_pixel/idle-5.png'),
                ]),
                AnimationSequence('jump', 0.25, [
                    utils.load_image('resources/crab_jump_pixel/ss-0000000000.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000001.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000002.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000003.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000004.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000005.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000006.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000007.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000008.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000009.png'),
                    utils.load_image('resources/crab_jump_pixel/ss-0000000010.png'),
                ])
            ]
        )

class Crab(engine.animated_sprite.AnimatedSprite):
    def __init__(self):
        super().__init__(CrabAnimation())

        self.rect.topleft = ((constants.WIDTH - self.rect.width) / 2, constants.HEIGHT - self.rect.height)
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
        super().animation('jump', 'idle')

    def land(self):
        self.velocity.y = 0
        super().animation('jump', 'idle')

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Font for displaying FPS
    font = pygame.font.Font(None, 36)

    # Set up the screen
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Ufo Attack")
    print("Screen initiated")

    # Set up the clock
    clock = pygame.time.Clock()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    ufo_sprites = pygame.sprite.Group()

    # Create the crab and add it to all_sprites group
    all_sprites.add(AnimatedBackGroud())
    print("Background added")

    # Generate ufo
    for i in range(500):
        random_ufo = Ufo()
        all_sprites.add(random_ufo)
        ufo_sprites.add(random_ufo)
    print("Ufos added")

    # Create the crab and add it to all_sprites group
    crab = Crab()
    all_sprites.add(crab)
    print("Crab added")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the game objects
        all_sprites.update()

        # # Check for collisions
        # if pygame.sprite.spritecollide(crab, obstacles, False):
        #     print("Game Over!")
        #     # running = False

        # Draw everything on the screen
        all_sprites.draw(screen)

        # Calculate and print the fps
        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {fps:.2f}", True, (50, 200, 50))
        screen.blit(fps_text, (10, 10))

        # Flip the display
        pygame.display.flip()
        clock.tick(constants.FRAME_RATE)

    # Quit Pygame
    pygame.quit()
