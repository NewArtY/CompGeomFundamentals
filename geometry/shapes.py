from geometry.base import BaseShapeModel
from geometry.primitives import Polyline, Arc


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
