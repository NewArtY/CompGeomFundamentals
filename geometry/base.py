from renderers.shape_render import RenderManager


class BaseModel:
    def __init__(self, color: tuple[int, int, int]):
        self.__color = color
        self.__visible = True

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


class BaseGeoModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.manager = RenderManager.get_instance()
        self.manager.register(self)
        self.coors = self.__generalized_mod(kwargs.get('coors'))
        super().__init__(color=kwargs.get('color'))

    @staticmethod
    def __generalized_mod(coors: tuple[tuple, ...]):
        return coors

    @staticmethod
    def get_new_coors(old: tuple[int, int], h: int, w: int) -> tuple[int, int]:
        return int(old[0] + w // 2), int(h // 2 - old[1])


class BaseShapeModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(color=kwargs.get('color'))
        self.shapes: list[BaseModel] | None = None

    def create_shape(self, *args: BaseModel):
        self.shapes = list(args)

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
