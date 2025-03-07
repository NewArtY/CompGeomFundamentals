from geometry.base import BaseShapeModel
from geometry.primitives import Polyline, Arc
from geometry.utils import interpolation_with_length


class LetterA(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 0, 0)):
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
            Arc((center[0], center[1] - h//4), h//4, -90, 90, color)
        )


class NewLetterA(BaseShapeModel):
    def __init__(self, h: int = 100, center: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (255, 0, 0)):
        super().__init__(color)
        coors_out = (
            (center[0] - h // 2, center[1] - h // 2),
            (center[0], center[1] + h // 2),
            (center[0] + h // 2, center[1] - h // 2)
        )
        coors_in = (
            (center[0] + h // 4, center[1]),
            (center[0] - h // 4, center[1])
        )
        coors = interpolation_with_length(5, coors_out) + interpolation_with_length(5, coors_in)
        self.create_shape(
            *(
                Polyline(coors=(dot1, dot2), color=color) for dot1, dot2 in zip(coors[:-1], coors[1:])
            )
        )
        self.hide_count = 0

    def update(self):
        if self.hide_count < len(self.shapes):
            self.shapes[self.hide_count].visible = False
            self.hide_count += 1
            return True
        return False
