import random

import numpy as np

from core.config import MIDDLE
from core.tools import TimedSpawner
from geometry.base import BaseShapeModel
from geometry.primitives import Polyline, Arc, Point, ShearedArc, Polygon
from geometry.utils import interpolation_with_length, get_step, distance


class LetterA(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 0, 0)):
        """
        Information model of the letter A
        :param h: letter height (width = height)
        :param center: central coordinate of the letter
        :param color: letter color (initial)
        """
        coors = (
            (center[0] - h//2, center[1] - h//2),
            (center[0], center[1] + h//2),
            (center[0] + h//2, center[1] - h//2),
            (center[0] + h//4, center[1]),
            (center[0] - h//4, center[1])
        )
        super().__init__(Polyline(coors=coors, color=color), color=color)


class LetterB(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 255, 255)):
        """
        Information model of the letter B
        :param h: letter height (width = height/2)
        :param center: central coordinate of the letter
        :param color: letter color (initial)
        """
        coors = (
            (center[0] + h//4, center[1] + h//2),
            (center[0] - h//4, center[1] + h//2),
            (center[0] - h//4, center[1]),
            (center[0], center[1]),
            (center[0] - h//4, center[1]),
            (center[0] - h//4, center[1] - h//2),
            (center[0], center[1] - h//2)
        )
        super().__init__(
            Polyline(coors=coors, color=color),
            ShearedArc((center[0], center[1] - h // 4), h // 4, -90, 90, color),
            color=color
        )


class LetterV(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 0, 0)):
        coors = (
            (center[0], center[1] + h // 2),
            (center[0] - h // 4, center[1] + h // 2),
            (center[0] - h // 4, center[1] + h // 6),
            (center[0], center[1] + h // 6),
            (center[0] - h // 4, center[1] + h // 6),
            (center[0] - h // 4, center[1] - h // 2),
            (center[0], center[1] - h // 2)
        )
        super().__init__(
            Polyline(coors=coors, color=color),
            ShearedArc((center[0], center[1] - h // 6), h // 3, -90, 90, color),
            ShearedArc((center[0], center[1] + h // 3), h // 6, -90, 90, color),
            color=color
        )


class ShapeWithBase(BaseShapeModel):
    def __init__(self, *args, base_point: tuple[int | float, int | float], base_angle: int | float,
                 color: tuple[int, int, int] = (255, 0, 0)):
        BaseShapeModel.__init__(self, args, color=color)
        self.base_point: Point = Point(base_point)
        self.base_point.visible = False
        self.base_angle = base_angle
        self.current_state = 0

    def rotate(self, alpha):
        super().rotate(alpha)
        self.base_angle += alpha
        self.base_angle %= 360

    def rotate_by_dot(self, alpha, d):
        super().rotate_by_dot(alpha, d)
        self.base_angle += alpha
        self.base_angle %= 360

    def shear(self, s):
        self.shear_by_segment(s, ((self.base_point.coors[0], self.base_point.coors[1]), self.base_angle))


class LetterAWithBase(ShapeWithBase, LetterA):  # Тут ромбовидное наследование - отнестись внимательнее
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 255, 255)):
        ShapeWithBase.__init__(self, base_point=(0, center[1] - h//2), base_angle=0)
        LetterA.__init__(self, h, center, color)
        self.shapes.append(self.base_point)


class LetterBWithBase(ShapeWithBase, LetterB):  # Тут тоже ромбовидное наследование
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 255, 255)):
        ShapeWithBase.__init__(self, base_point=(0, center[1] - h//2), base_angle=0)
        LetterB.__init__(self, h, center, color)
        self.shapes.append(self.base_point)


class LetterVWithBase(ShapeWithBase, LetterV):  # И тут тоже ромбовидное наследование
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 255, 255)):
        ShapeWithBase.__init__(self, base_point=(0, center[1] - h//2), base_angle=0)
        LetterV.__init__(self, h, center, color)
        self.shapes.append(self.base_point)


class NewLetterA(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 0, 0)):
        """
        Another information model of the letter A
        :param h: letter height (width = height)
        :param center: central coordinate of the letter
        :param color: letter color (initial)
        """
        length_step = 2
        shapes = []
        coors = (
            (
                (center[0] - h // 2, center[1] - h // 2),
                (center[0], center[1] + h // 2),
                (center[0] + h // 2, center[1] - h // 2)
            ),
            (
                (center[0] + h // 4, center[1]),
                (center[0] - h // 4, center[1])
            )
        )

        for coord in coors:
            new_coord = interpolation_with_length(length_step, coord)
            shapes += [Polyline(coors=(dot1, dot2), color=color) for dot1, dot2 in zip(new_coord[:-1], new_coord[1:])]

        self.hide_count = 0
        super().__init__(*shapes, color=color)

    def update(self) -> bool:
        """
        Letter update rules: letters gradually become invisible
        :returns: True if letter state has been changed and False otherwise
        """
        if self.hide_count < len(self.shapes):
            self.shapes[self.hide_count].visible = False
            self.hide_count += 1
            return True
        return False


class AChain(BaseShapeModel):
    def __init__(self, h: int = 20, center: tuple[int, int] = (0, 0), count_a: int = 1,
                 color: tuple[int, int, int] = (255, 0, 0)):
        self.steps: list[tuple[int, int]] = [(0, 0)] * count_a
        shapes = []
        for _ in range(count_a):
            shapes.append(LetterA(h, center, color))
        super().__init__(*shapes, color=color)

    def update(self, move_on_x: int | float, move_on_y: int | float, by_step: int | float):
        del self.steps[0]
        if move_on_x is not None and move_on_y is not None:
            self.steps += [
                tuple(get_step(self.shapes[-1]._center,
                               np.array(self.get_old_coors((move_on_x, move_on_y))),
                               by_step)
                      )
            ]
        else:
            self.steps += [
                tuple(get_step(self.shapes[-1]._center,
                               np.array((0, 0)),
                               by_step)
                      )
            ]

        for shape, step in zip(self.shapes, self.steps):
            shape.move_on(step)


class SpawnerABVChain(BaseShapeModel):
    def __init__(self, h: int = 50, spawn: tuple[int, int] = (0, 0), count: int = 10, time_spawn: int = 30,
                 color: tuple[int, int, int] = (255, 0, 0)):
        self.h = h
        self.spawn_place = spawn
        self.spawn_count = count
        self.time_spawn = time_spawn
        self.spawner = TimedSpawner(time_spawn, count)
        step_length = 0.02
        step_half_count = 25
        self.track = ([-step_length] * step_half_count +
                      [step_length] * 2 * step_half_count +
                      [-step_length] * step_half_count
                      )
        super().__init__(color=color)

    def update(self):
        if self.spawner.update(len(self.shapes)):
            self.shapes.append(
                random.choice(
                    [LetterAWithBase, LetterBWithBase, LetterVWithBase]
                              )(
                    self.h, self.spawn_place,
                    (random.randint(0, 255),
                     random.randint(0, 255),
                     random.randint(0, 255)
                     )
                )
            )
        self.rotate_by_dot(1, (0, 0))
        for shape in self.shapes:
            if hasattr(shape, 'current_state'):
                shape.shear(self.track[shape.current_state])
                shape.current_state += 1
                shape.current_state %= len(self.track)


class Arrow(BaseShapeModel):
    def __init__(self, arrow_start: tuple | np.ndarray, arrow_dir: tuple | np.ndarray, arrow_length: float | int = 10,
                 color: tuple[int, int, int] = (255, 255, 255)):
        dx, dy = arrow_length * arrow_dir[0], arrow_length * arrow_dir[1]
        head_size = min(10, arrow_length // 4)
        arrow_end = (arrow_start[0] + dx, arrow_start[1] + dy)
        perp_dx = -arrow_dir[1]
        perp_dy = arrow_dir[0]
        left_point = (
            arrow_end[0] - arrow_dir[0] * head_size + perp_dx * head_size / 2,
            arrow_end[1] - arrow_dir[1] * head_size + perp_dy * head_size / 2
        )
        right_point = (
            arrow_end[0] - arrow_dir[0] * head_size - perp_dx * head_size / 2,
            arrow_end[1] - arrow_dir[1] * head_size - perp_dy * head_size / 2
        )
        shapes = (
            Polyline(
                coors=(arrow_start, arrow_end),
                color=color,
                layer=MIDDLE
            ),
            Polygon(
                coors=(arrow_end, left_point, right_point),
                color=color,
                layer=MIDDLE
            )
        )
        super().__init__(*shapes, color=color)
