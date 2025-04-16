import pygame

from core.scenes.base_scene import Scene
from geometry.primitives import Arc, ShearedArc
from geometry.shapes import LetterA, LetterB, NewLetterA


class StaticABScene(Scene):
    def __init__(self):
        super().__init__()
        self.letterA = None
        self.letterB = None
        self.newLetterA = None

    def on_enter(self):
        LetterA(h=100, color=(0, 0, 255), center=(0, -50))
        self.letterB = LetterB(center=(0, 125))
        self.letterA = LetterA(h=200)
        self.newLetterA = NewLetterA(center=(0, -200), h=150)
        ShearedArc((0, 0), 100, 30, 150, (255, 0, 0))

    def on_exit(self):
        self.renderer.clear_all()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.letterA.color = (0, 255, 0)
            if event.key == pygame.K_t:
                self.engine.scene_manager.next_scene(click='t')
            if event.key == pygame.K_n:
                self.engine.scene_manager.next_scene()
            if event.key == pygame.K_b:
                self.engine.scene_manager.previous_scene()

    def update(self, dt):
        self.newLetterA.update()
