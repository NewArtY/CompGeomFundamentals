from renderers.shape_render import RenderManager


class BaseModel:
    def __init__(self, color: tuple[int, int, int]):
        self.color = color

    def render(self, surface):
        pass  # Переопределяется в дочерних классах

    def set_color(self, color: tuple[int, int, int]):
        self.color = color


class BaseGeoModel(BaseModel):
    def __init__(self, *args, **kwargs):
        self.manager = RenderManager.get_instance()
        self.manager.register(self)
        self.coors = self.__generalized_mod(kwargs.get('coors'))
        super().__init__(color=kwargs.get('color'))
        self.visible = True

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

    def set_color(self, new_color: tuple[int, int, int]):
        for shape in self.shapes:
            shape.set_color(new_color)
