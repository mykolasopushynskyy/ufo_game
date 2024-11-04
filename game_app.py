import pygame
from array import array

import constants
import moderngl

from engine import assets
from engine.cursors import GameCursors
from game.air_defence import AirDefence
from game.background import AnimatedBackGround
from game.crab import Crab
from game.ufo import Ufo

# IMPORTANT don't touch or change values
QUAD_BUFFER = array(
    "f",
    [
        -1.0,
        1.0,
        0.0,
        0.0,  # top left
        1.0,
        1.0,
        1.0,
        0.0,  # top right
        -1.0,
        -1.0,
        0.0,
        1.0,  # bot top left
        1.0,
        -1.0,
        1.0,
        1.0,  # bot top right
    ],
)

if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Атака НЛО")

    # Set up the screen
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
    )
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
    screen = pygame.display.set_mode(
        (constants.WIDTH, constants.HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF
    )
    display = pygame.Surface((constants.WIDTH, constants.HEIGHT))
    print("Screen initiated")

    # Use OpenGL
    ctx = moderngl.create_context()
    vert_shader = assets.read_file_as_string(constants.VERT_SHADER_PATH)
    frag_shader = assets.read_file_as_string(constants.FRAG_SHADER_PATH)
    program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
    quad_buffer = ctx.buffer(data=QUAD_BUFFER)
    render_object = ctx.vertex_array(
        program, [(quad_buffer, "2f 2f", "vert", "texcoord")]
    )

    def surf_to_texture(surf):
        texture = ctx.texture(surf.get_size(), 4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = "BGRA"
        texture.write(surf.get_view("1"))
        return texture

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

        frame_tex = surf_to_texture(display)
        frame_tex.use(0)
        program["tex"] = 0
        program["time"] = int((frame_idx / (constants.FRAME_RATE / 12)))
        frame_idx += 1
        render_object.render(mode=moderngl.TRIANGLE_STRIP)

        # Update the game objects
        all_sprites.update()

        # Draw everything on the screen
        all_sprites.draw(display)

        # get all events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        mx, my = pygame.mouse.get_pos()

        # air_defence
        is_shooting = air_defence.update(display, events, mx, my)

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
        display.blit(cur_image, (mx + cx, my + cy))

        # Calculate and print the fps
        fps = clock.get_fps()

        # print information
        mouse = game_font.render(f"Mouse: {mx}, {my}", True, (50, 200, 50))
        display.blit(mouse, (10, 10))
        fps_text = debug_font.render(f"FPS: {fps:.2f}", True, (50, 200, 50))
        display.blit(fps_text, (10, 46))
        mouse = debug_font.render(f"Збито НЛО: {ufo_counter}", True, (0xEA, 0xA1, 0x2C))
        display.blit(mouse, (10, 82))

        # Flip the display
        pygame.display.flip()
        frame_tex.release()
        clock.tick(constants.FRAME_RATE)

    # Quit Pygame
    pygame.quit()
