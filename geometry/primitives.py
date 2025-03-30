import numpy as np
import pygame
from pygame.gfxdraw import pixel, line, arc

from core.config import BACKGROUND
from geometry.base import BaseGeoModel


class Point(BaseGeoModel):
    def __init__(self, coors: tuple[int, int] = (0, 0),
                 color: tuple[int, int, int] = (0, 0, 0),
                 layer: str = BACKGROUND):
        super().__init__(coors=coors, color=color, layer=layer)

    def render(self, surface: pygame.Surface):
        pixel(surface, *self.get_new_coors(self.coors, surface.get_height(), surface.get_width()), self.color)


class Polyline(BaseGeoModel):
    def __init__(self, coors: tuple[tuple, ...] = ((0, 0), (1, 1)),
                 color: tuple[int, int, int] = (0, 0, 0),
                 layer: str = BACKGROUND):
        super().__init__(coors=coors, color=color, layer=layer)

    def _generalized_mod(self, coors: tuple[tuple]):
        """Обобщённые координаты для ломанной линии"""
        coors = np.array(coors, dtype=np.float64)
        ones_array = np.ones((coors.shape[0], 1), dtype=int)
        return np.hstack((coors, ones_array))

    @property
    def _center(self):
        return np.mean(self.coors, axis=0)[:2]

    def rotate(self, alpha):
        c = self._center
        self.rotate_by_dot(alpha, c)

    def scale(self, k):
        c = self._center
        self.scale_by_dot(c, k)

    def render(self, surface: pygame.Surface):
        height, width = surface.get_height(), surface.get_width()
        for d1, d2 in zip(self.coors[:-1], self.coors[1:]):
            line(surface, *self.get_new_coors(d1, height, width),
                 *self.get_new_coors(d2, height, width), self.color)


class Polygon(Polyline):
    def __init__(self, coors: tuple[tuple, ...] = ((0, 0), (1, 1)),
                 color: tuple[int, int, int] = (0, 0, 0),
                 layer: str = BACKGROUND):
        coors += (coors[0], )
        super().__init__(coors, color, layer)

    @property
    def _center(self):
        return np.mean(self.coors[:-1], axis=0)[:2]


class Arc(BaseGeoModel):
    def __init__(self, coors: tuple[int, int] = (0, 0),
                 r: int = 10, start_angle: int = 0, end_angle: int = 180,
                 color: tuple[int, int, int] = (255, 255, 255),
                 layer: str = BACKGROUND):
        super().__init__(coors=coors, color=color, layer=layer)
        self.r = r
        self.start_angle = start_angle
        self.end_angle = end_angle

    def render(self, surface: pygame.Surface):
        height, width = surface.get_height(), surface.get_width()
        arc(surface, *self.get_new_coors(self.coors, height, width),
            self.r, 360 - self.end_angle, 360 - self.start_angle, self.color)
