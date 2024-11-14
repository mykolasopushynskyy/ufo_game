from array import array

import moderngl
import pygame

from engine import assets

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


class OpenGLGame:
    def __init__(
        self, width: int, height: int, vertex_shader_path: str, fragment_shader: str
    ):
        # Set up the screen
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
        screen = pygame.display.set_mode(
            (width, height), pygame.OPENGL | pygame.DOUBLEBUF
        )
        self.display = pygame.Surface((width, height))

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = self.ctx.SRC_ALPHA, self.ctx.ONE_MINUS_SRC_ALPHA

        self.program = self.ctx.program(
            vertex_shader=assets.read_file_as_string(vertex_shader_path),
            fragment_shader=assets.read_file_as_string(fragment_shader),
        )
        self.render_object = self.ctx.vertex_array(
            self.program,
            [(self.ctx.buffer(data=QUAD_BUFFER), "2f 2f", "vert", "texcoord")],
        )
        self.frame_tex = None

    def init_texture(self, **kwargs):
        self.frame_tex = self.ctx.texture(self.display.get_size(), 4)
        self.frame_tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.frame_tex.swizzle = "BGRA"
        self.frame_tex.write(self.display.get_view("1"))
        self.frame_tex.use(0)

        for k, v in kwargs.items():
            self.program[k] = v

        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

    def cleanup(self):
        self.frame_tex.release()
