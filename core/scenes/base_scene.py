from abc import ABC, abstractmethod

from renderers.shape_render import RenderManager


class Scene(ABC):
    def __init__(self):
        from core.engine import Engine

        self.engine: Engine | None = None  # Ссылка на движок должна быть установлена при добавлении сцены
        self.renderer = RenderManager()
        self.fast_forward_available = True
        self.backward_available = True
        self.name: str | None = None

    @abstractmethod
    def on_enter(self):
        """Вызывается при переключении на эту сцену"""
        pass

    @abstractmethod
    def on_exit(self):
        """Вызывается при уходе с этой сцены"""
        pass

    @abstractmethod
    def handle_event(self, event):
        """Обработка событий pygame в этой сцене"""
        pass

    @abstractmethod
    def update(self, dt):
        """Обновление состояния сцены"""
        pass

    def render(self, surface):
        """Отрисовка сцены на указанной поверхности"""
        self.renderer.render_all(surface)


