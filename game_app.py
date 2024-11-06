import pygame

import constants

from engine import open_gl
from engine.cursors import GameCursors
from game.air_defence import AirDefence
from game.background import AnimatedBackGround
from game.crab import Crab
from game.ufo import Ufo


if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Атака НЛО")

    # Set up the screen
    og_game = open_gl.OpenGLGame(
        width=constants.WIDTH,
        height=constants.HEIGHT,
        vertex_shader_path=constants.VERT_SHADER_PATH,
        fragment_shader=constants.FRAG_SHADER_PATH,
    )
    print("OpenGL initiated")

    # Set up the clock
    clock = pygame.time.Clock()

    # Font for displaying FPS
    debug_font = pygame.font.Font(None, 36)
    game_font = pygame.font.SysFont(None, 36)

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    ufo_sprites = pygame.sprite.Group()

    # Create the crab and add it to all_sprites group
    all_sprites.add(AnimatedBackGround())
    print("Background added")

    # Generate ufo
    for i in range(constants.UFOS_NUMBER):
        random_ufo = Ufo()
        all_sprites.add(random_ufo)
        ufo_sprites.add(random_ufo)
    print("Ufos added")

    # Create the crab and add it to all_sprites group
    all_sprites.add(Crab())
    print("Crab added")

    # Air defence
    air_defence = AirDefence()
    print("Air defence added")

    # Create cursor
    cursors = GameCursors()
    pygame.mouse.set_visible(False)

    running = True
    frame_idx = 0
    ufo_counter = 0
    while running:
        og_game.init_texture(tex=0, time=int((frame_idx / (constants.FRAME_RATE / 12))))

        frame_idx += 1

        # Update the game objects
        all_sprites.update()

        # Draw everything on the screen
        all_sprites.draw(og_game.display)

        # get all events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        mx, my = pygame.mouse.get_pos()

        # air_defence
        is_shooting = air_defence.defend(og_game.display, events, mx, my)

        # get a list of all sprites that are under the mouse cursor
        ufos_shot = len(
            [
                ufo.hit()
                for ufo in ufo_sprites
                if not ufo.is_hit and is_shooting and ufo.rect.collidepoint((mx, my))
            ]
        )
        ufo_counter += ufos_shot

        # draw cursor
        cur_image, cx, cy = cursors.get("aim")
        og_game.display.blit(cur_image, (mx + cx, my + cy))

        # Calculate and print the fps
        fps = clock.get_fps()

        # print information
        mouse = game_font.render(f"Mouse: {mx}, {my}", True, (50, 200, 50))
        og_game.display.blit(mouse, (10, 10))
        fps_text = debug_font.render(f"FPS: {fps:.2f}", True, (50, 200, 50))
        og_game.display.blit(fps_text, (10, 46))
        mouse = debug_font.render(f"Збито НЛО: {ufo_counter}", True, (0xEA, 0xA1, 0x2C))
        og_game.display.blit(mouse, (10, 82))

        # Flip the display
        pygame.display.flip()
        og_game.cleanup()
        clock.tick(constants.FRAME_RATE)

    # Quit Pygame
    pygame.quit()
