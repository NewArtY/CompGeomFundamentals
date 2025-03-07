import numpy as np
import pygame
from pygame.gfxdraw import pixel, line, arc

from geometry.base import BaseGeoModel


class Point(BaseGeoModel):
    def __init__(self, coors: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (0, 0, 0)):
        super().__init__(coors=coors, color=color)

    def render(self, surface: pygame.Surface):
        pixel(surface, *BaseGeoModel.get_new_coors(self.coors, surface.get_height(), surface.get_width()), self.color)


class Polyline(BaseGeoModel):
    def __init__(self, coors: tuple[tuple, ...] = ((0, 0), (1, 1)),
                 color: tuple[int, int, int] = (0, 0, 0)):
        super().__init__(coors=coors, color=color)

    @staticmethod
    def __generalized_mod(coors: tuple[tuple]):
        """Метод предварительной обработки координат для ломанной линии"""

        coors = np.array(coors, dtype=np.float64)
        ones_array = np.ones((coors.shape[0], 1), dtype=int)
        return np.hstack((coors, ones_array))

    def render(self, surface: pygame.Surface):
        height, width = surface.get_height(), surface.get_width()
        for d1, d2 in zip(self.coors[:-1], self.coors[1:]):
            line(surface, *BaseGeoModel.get_new_coors(d1, height, width),
                 *BaseGeoModel.get_new_coors(d2, height, width), self.color)


class Arc(BaseGeoModel):
    def __init__(self, coors: tuple[int, int] = (0, 0), r: int = 10, start_angle: int = 0, end_angle: int = 180,
                 color: tuple[int, int, int] = (255, 255, 255)):
        super().__init__(coors=coors, color=color)
        self.r = r
        self.start_angle = start_angle
        self.end_angle = end_angle

    def render(self, surface: pygame.Surface):
        height, width = surface.get_height(), surface.get_width()
        arc(surface, *BaseGeoModel.get_new_coors(self.coors, height, width),
            self.r, 360 - self.end_angle, 360 - self.start_angle, self.color)
