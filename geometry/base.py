import numpy as np

from core.config import BACKGROUND
from renderers.shape_render import RenderManager


class BaseModel:
    w, h = None, None

    def __init__(self, color: tuple[int, int, int]):
        self.__color = color
        self.__visible = True

    @staticmethod
    def get_new_coors(old: tuple[int, int]) -> tuple[int, int]:
        return int(old[0] + BaseModel.w // 2), int(BaseModel.h // 2 - old[1])

    @staticmethod
    def get_old_coors(new: tuple[int, int]) -> tuple[int, int]:
        return int(new[0] - BaseModel.w // 2), int(BaseModel.h // 2 - new[1])

    def render(self, surface):
        pass  # Переопределяется в дочерних классах

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: tuple[int, int, int]):
        self.__color = color

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, visible: bool):
        self.__visible = visible

    @property
    def _center(self):
        return None

    def move_on(self, d: tuple[int | float, int | float]):
        pass

    def rotate_by_dot(self, alpha, d):
        pass

    def scale_by_dot(self, d, k):
        pass

    def rotate(self, alpha):
        pass

    def scale(self, k):
        pass

    def shear(self, s):
        pass

    def shear_by_segment(self, s: int | float, directed_segment: tuple[tuple[int | float, int | float], int | float]):
        pass


class BaseGeoModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.manager = RenderManager()
        self.manager.register(self, layer=kwargs.get('layer', BACKGROUND))
        self.coors = self._generalized_mod(kwargs.get('coors'))
        super().__init__(color=kwargs.get('color'))

    def _generalized_mod(self, coors: tuple[int, int]):
        """Обобщённые координаты для ломанной точки"""
        return np.hstack((coors, (1, )))

    def abstract_transformation(self, alpha: int | float = 0,
                                d: tuple[int | float, int | float] = (0, 0),
                                k: int | float = 1,
                                s: int | float = 0):
        f = np.array([
            [k * np.cos(np.deg2rad(alpha)),     k * np.sin(np.deg2rad(alpha)), 0],
            [s - k * np.sin(np.deg2rad(alpha)), k * np.cos(np.deg2rad(alpha)), 0],
            [d[0],                              d[1],                          1]
        ])
        self.coors = self.coors.dot(f)

    def move_on(self, d: tuple[int | float, int | float]):
        self.abstract_transformation(0, d, 1)

    def rotate_by_dot(self, alpha, d):
        self.abstract_transformation(0, (-d[0], -d[1]), 1)
        self.abstract_transformation(alpha, (0, 0), 1)
        self.abstract_transformation(0, d, 1)

    def scale_by_dot(self, d, k):
        self.abstract_transformation(0, (-d[0], -d[1]), 1)
        self.abstract_transformation(0, (0, 0), k)
        self.abstract_transformation(0, d, 1)

    def shear(self, s):
        self.abstract_transformation(s=s)

    def shear_by_segment(self, s: int | float, directed_segment: tuple[tuple[int | float, int | float], int | float]):
        self.move_on((-directed_segment[0][0], -directed_segment[0][1]))
        self.rotate(-directed_segment[1])
        self.shear(s)
        self.rotate(directed_segment[1])
        self.move_on(directed_segment[0])


class BaseShapeModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(color=kwargs.get('color'))
        self.shapes: list[BaseModel] = list(args)

    def render(self, surface):
        for shape in self.shapes:
            shape.render(surface)

    @BaseModel.color.setter
    def color(self, color: tuple[int, int, int]):
        for shape in self.shapes:
            shape.color = color

    @BaseModel.visible.setter
    def visible(self, visible: bool):
        for shape in self.shapes:
            shape.visible = visible

    @property
    def _center(self):
        center = np.array([0, 0], dtype=np.float64)
        for shape in self.shapes:
            center += shape._center
        return center/len(self.shapes)

    def rotate(self, alpha):
        center = self._center
        for shape in self.shapes:
            shape.rotate_by_dot(alpha, center)

    def scale(self, alpha):
        center = self._center
        for shape in self.shapes:
            shape.scale_by_dot(alpha, center)

    def rotate_by_dot(self, alpha, d):
        for shape in self.shapes:
            shape.rotate_by_dot(alpha, d)

    def scale_by_dot(self, d, k):
        for shape in self.shapes:
            shape.scale_by_dot(d, k)

    def move_on(self, d):
        for shape in self.shapes:
            shape.move_on(d)

    def shear(self, s):
        for shape in self.shapes:
            shape.shear(s)

    def shear_by_segment(self, s: int | float, directed_segment: tuple[tuple[int | float, int | float], int | float]):
        for shape in self.shapes:
            shape.shear_by_segment(s, directed_segment)
