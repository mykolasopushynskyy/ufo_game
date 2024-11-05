import math
import random

import pygame


class AirDefence:
    def __init__(self):
        super().__init__()

        self.frame_idx = 0
        self.mouse_pressed = False
        self.cx = 725
        self.cy = 655
        self.r = 50

        self.beam_r, self.beam_g, self.beam_b = 225, 75, 30
        self.r_a, self.g_a, self.b_a = 25, 25, 0
        self.beam_color = (self.beam_r, self.beam_g, self.beam_b)
        self.mx, self.my = pygame.mouse.get_pos()

        self.laser_x1 = (
            self.cx
            + self.r
            * (self.mx - self.cx)
            / ((self.mx - self.cx) ** 2 + (self.my - self.cy) ** 2) ** 0.5
        )
        self.laser_y1 = (
            self.cy
            + self.r
            * (self.my - self.cy)
            / ((self.mx - self.cx) ** 2 + (self.my - self.cy) ** 2) ** 0.5
        )

    def defend(self, surface, pygame_events, mx, my):
        self.frame_idx += 1
        # draw laser with period
        # air defence cords 725, 655
        self.mx, self.my = mx, my

        # get all events
        for event in pygame_events:
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True

        if (
            self.mouse_pressed
            and self.my < self.cy + self.r
            and ((self.mx - self.cx) ** 2 + (self.my - self.cy) ** 2) ** 0.5 > self.r
        ):

            self.laser_x1 = (
                self.cx
                + self.r
                * (self.mx - self.cx)
                / ((self.mx - self.cx) ** 2 + (self.my - self.cy) ** 2) ** 0.5
            )
            self.laser_y1 = (
                self.cy
                + self.r
                * (self.my - self.cy)
                / ((self.mx - self.cx) ** 2 + (self.my - self.cy) ** 2) ** 0.5
            )

            # beam color and amplitudes
            self.beam_color = (
                int(self.beam_r + self.r_a * math.sin(self.frame_idx)),
                int(self.beam_g + self.g_a * math.sin(self.frame_idx)),
                int(self.beam_b + self.b_a * math.sin(self.frame_idx)),
            )

            pygame.draw.line(
                surface,
                self.beam_color,
                (self.laser_x1 + random.uniform(-3, 3), self.laser_y1 + random.uniform(-3, 3)),
                (self.mx + random.uniform(-1, 1), self.my + random.uniform(-2, 2)),
                3,
            )
            return True

        return False
