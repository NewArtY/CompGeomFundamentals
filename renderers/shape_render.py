from geometry.base import BaseGeoModel


class RenderManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = RenderManager()
        return cls._instance

    def __init__(self):
        if RenderManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            RenderManager._instance = self

        self.objects: list[BaseGeoModel] = []

    def register(self, obj):
        self.objects.append(obj)

    def unregister(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def render_all(self, surface):
        for obj in self.objects:
            if obj.visible:
                obj.render(surface)
