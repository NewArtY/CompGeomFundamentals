import numpy as np
import pygame
from pygame.gfxdraw import pixel, line, arc

from core.config import BACKGROUND
from geometry.base import BaseGeoModel
from geometry.utils import distance


class Point(BaseGeoModel):
    def __init__(self, coors: tuple[int, int] = (0, 0),
                 color: tuple[int, int, int] = (0, 0, 0),
                 layer: str = BACKGROUND):
        super().__init__(coors=coors, color=color, layer=layer)

    def render(self, surface: pygame.Surface):
        pixel(surface, *self.get_new_coors(self.coors), self.color)

    @property
    def _center(self):
        return self.coors[:2]


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
        for d1, d2 in zip(self.coors[:-1], self.coors[1:]):
            line(surface, *self.get_new_coors(d1),
                 *self.get_new_coors(d2), self.color)


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
        arc(surface, *self.get_new_coors(self.coors),
            int(self.r), int(360 - self.end_angle), int(360 - self.start_angle), self.color)

    def rotate(self, alpha: int | float):
        self.start_angle += alpha
        self.start_angle %= 360
        self.end_angle += alpha
        self.end_angle %= 360

    def scale(self, k: int | float):
        self.r *= k

    def rotate_by_dot(self, alpha, d):
        super().rotate_by_dot(alpha, d)
        self.rotate(alpha)

    def scale_by_dot(self, d, k):
        super().scale_by_dot(d, k)
        self.scale(k)

    @property
    def _center(self):
        return self.coors[:2]


class Fractal(Polyline):
    def __init__(self, f_base: tuple[tuple[int | float, int | float]],
                 fragment: tuple[tuple[int | float, int | float]], f_level: int,
                 color: tuple[int, int, int] = (255, 255, 255),
                 layer: str = BACKGROUND):
        coors = self.fractalizator(f_base, fragment, f_level)
        super().__init__(coors=coors, color=color, layer=layer)

    @staticmethod
    def fractalizator(f_base: tuple[tuple[int | float, int | float]],
                      fragment: tuple[tuple[int | float, int | float]],
                      f_level: int):
        l_all = distance(f_base[0], f_base[1])
        if f_base[0] != fragment[0] or f_base[1] != fragment[-1]:
            fragment = Fractal.transform_polyline(f_base, fragment)
        l_line = distance(fragment[0], fragment[1])
        angels = ()
        for point1, point2 in zip(fragment[:-1], fragment[1:]):
            angels += (np.atan2(point2[1] - point1[1], point2[0] - point1[0]), )

        n = len(angels)
        k = l_line / l_all
        l_f_line = k ** f_level * l_all
        coors = (f_base[0], )
        for i in range(n ** f_level):
            fi = 0
            for j in range(f_level):
                fi += angels[i % n]
                i //= n
            coors += ((
                coors[-1][0] + l_f_line * np.cos(fi),
                coors[-1][1] + l_f_line * np.sin(fi)
            ), )
        return coors

    @staticmethod
    def transform_polyline(segment, polyline):
        a, b = segment
        p0 = polyline[0]
        pn = polyline[-1]
        # Вычисляем вектор исходного смещения ломаной (Qn)
        qx = pn[0] - p0[0]
        qy = pn[1] - p0[1]
        # Вычисляем вектор целевого отрезка AB
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        # Вычисляем знаменатель для матрицы преобразования
        denominator = qx ** 2 + qy ** 2
        if denominator == 0:
            return tuple(segment[0] for _ in range(len(polyline)))
        # Элементы матрицы преобразования M
        m00 = (qx * dx + qy * dy) / denominator
        m01 = (-qx * dy + qy * dx) / denominator
        m10 = (qx * dy - qy * dx) / denominator
        m11 = (qx * dx + qy * dy) / denominator
        # Применяем преобразование ко всем точкам ломаной
        transformed = ()
        for point in polyline:
            x, y = point
            # Смещаем точку относительно P0
            x_shifted = x - p0[0]
            y_shifted = y - p0[1]
            # Применяем матрицу преобразования
            new_x = m00 * x_shifted + m01 * y_shifted
            new_y = m10 * x_shifted + m11 * y_shifted
            # Переносим точку в целевую позицию A
            new_x += a[0]
            new_y += a[1]
            transformed += ((new_x, new_y), )
        return transformed


class ShearedArc(Polyline):
    def __init__(self, center: tuple[int, int] = (0, 0),
                 r: int = 10, start_angle: int = 0, end_angle: int = 180,
                 color: tuple[int, int, int] = (255, 255, 255),
                 layer: str = BACKGROUND):
        super().__init__(coors=self._get_coors(r, center, start_angle, end_angle), color=color, layer=layer)
        self.r = r
        self.start_angle = start_angle
        self.end_angle = end_angle

    @staticmethod
    def _get_coors(r, center, start_angle, end_angle):
        start_angle = np.pi * start_angle / 180
        end_angle = np.pi * end_angle / 180
        angle_measure = r * (end_angle - start_angle)
        n = int(angle_measure) // 2
        angle_step = (end_angle - start_angle) / n
        coors = tuple((center[0] + r * np.cos(start_angle + i * angle_step),
                       center[1] + r * np.sin(start_angle + i * angle_step)
                       )
                      for i in range(n + 1))
        return coors


if __name__ == '__main__':
    coors = Fractal.fractalizator(((0, 0), (1, 0)),
                                  ((0, 0), (1/3, 0), (1/2, (1/12)**(1/2)), (2/3, 0), (1, 0)), 5
                                  )
    print(coors)
    print(Fractal.transform_polyline(((-300, 0), (-100, 0)),
                                     ((0, 0), (1/3, 0), (1/2, (1/12)**(1/2)), (2/3, 0), (1, 0))
                                     )
          )
