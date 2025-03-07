from geometry.base import BaseShapeModel
from geometry.primitives import Polyline, Arc
from geometry.utils import interpolation_with_length


class LetterA(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 0, 0)):
        """
        Information model of the letter A
        :param h: letter height (width = height)
        :param center: central coordinate of the letter
        :param color: letter color (initial)
        """
        super().__init__(color)
        coors = (
            (center[0] - h//2, center[1] - h//2),
            (center[0], center[1] + h//2),
            (center[0] + h//2, center[1] - h//2),
            (center[0] + h//4, center[1]),
            (center[0] - h//4, center[1])
        )
        self.create_shape(Polyline(coors=coors, color=color))


class LetterB(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 255, 255)):
        """
        Information model of the letter B
        :param h: letter height (width = height/2)
        :param center: central coordinate of the letter
        :param color: letter color (initial)
        """
        super().__init__(color)
        coors = (
            (center[0] + h//4, center[1] + h//2),
            (center[0] - h//4, center[1] + h//2),
            (center[0] - h//4, center[1]),
            (center[0], center[1]),
            (center[0] - h//4, center[1]),
            (center[0] - h//4, center[1] - h//2),
            (center[0], center[1] - h//2)
        )
        self.create_shape(
            Polyline(coors=coors, color=color),
            Arc((center[0], center[1] - h // 4), h // 4, -90, 90, color)
        )


class NewLetterA(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 0, 0)):
        """
        Another information model of the letter A
        :param h: letter height (width = height)
        :param center: central coordinate of the letter
        :param color: letter color (initial)
        """
        super().__init__(color)
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

        self.create_shape(
            *shapes
        )
        self.hide_count = 0

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
