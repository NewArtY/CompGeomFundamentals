from core.config import BACKGROUND, MIDDLE, FOREGROUND
from core.meta import SingletonMeta


class RenderManager(metaclass=SingletonMeta):
    def __init__(self):
        from geometry.base import BaseGeoModel

        self.layers: dict[str, list[BaseGeoModel]] = {
            BACKGROUND: [],   # Нижний слой
            MIDDLE: [],       # Средний слой
            FOREGROUND: []    # Верхний слой
        }

    def register(self, obj, layer="background"):
        if layer not in self.layers:
            raise ValueError(f"Layer '{layer}' does not exist.")
        self.layers[layer].append(obj)

    def unregister(self, obj):
        for layer in self.layers.keys():
            if obj in self.layers[layer]:
                self.layers[layer].remove(obj)

    def clear_all(self):
        self.layers = {"background": [], "middle": [], "foreground": []}

    def render_all(self, surface):
        for _, objects in self.layers.items():
            for obj in objects:
                if obj.visible:
                    obj.render(surface)
