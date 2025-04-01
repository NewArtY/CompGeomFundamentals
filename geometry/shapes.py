import numpy as np

from geometry.base import BaseShapeModel
from geometry.primitives import Polyline, Arc
from geometry.utils import interpolation_with_length, get_step


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
            Arc((center[0], center[1] - h // 4), h // 4, -90, 90, color),
            color=color
        )


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
