import pygame

from core.scenes.base_scene import Scene
from geometry.primitives import Fractal


class FractalScene(Scene):
    def __init__(self):
        super().__init__()
        self.frac_1 = None
        self.frac_2 = None
        self.frac_3 = None
        self.frac_4 = None

    def on_enter(self):
        koh = ((0, 0), (1/3, 0), (1/2, (1/12)**(1/2)), (2/3, 0), (1, 0))
        self.frac_1 = Fractal(((-350, 150), (-50, 150)), koh, 1)
        self.frac_2 = Fractal(((50, 150), (350, 150)), koh, 2)
        self.frac_3 = Fractal(((-350, -150), (-50, -150)), koh, 3)
        self.frac_4 = Fractal(((50, -150), (350, -150)), koh, 4)

    def on_exit(self):
        self.renderer.clear_all()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.engine.scene_manager.next_scene()
            if event.key == pygame.K_b:
                self.engine.scene_manager.previous_scene()

    def update(self, dt):
        pass
