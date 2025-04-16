import numpy as np
import pygame

from core.scenes.base_scene import Scene
from geometry.primitives import Arc
from geometry.shapes import LetterA, LetterB, AChain, LetterAWithBase, SpawnerABVChain


class TransformationScene(Scene):
    def __init__(self):
        super().__init__()
        self.letterA = None
        self.letterA2: LetterAWithBase | None = None
        self.letterB = None
        self.arc = None
        self.mult = 0.99
        self.chain = None
        self.mouse_x, self.mouse_y = None, None
        self.steps = [-0.02] * 25 + [0.02] * 50 + [-0.02] * 25
        self.c_s = 0
        self.figures: SpawnerABVChain | None = None

    def on_enter(self):
        self.letterB = LetterB(center=(-200, 125))
        self.letterA = LetterA(h=200)
        self.letterA2 = LetterAWithBase(h=200, color=(100, 255, 0))
        self.arc = Arc((0, 0), 100, 30, 150, (255, 0, 0))
        self.chain = AChain(count_a=20, color=(255, 123, 12))
        self.c_s = 0
        self.figures = SpawnerABVChain(spawn=(0, 150), count=12)

    def on_exit(self):
        self.renderer.clear_all()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.letterA.color = (255, 255, 255)
            if event.key == pygame.K_n:
                self.engine.scene_manager.next_scene()
            if event.key == pygame.K_b:
                self.engine.scene_manager.previous_scene()
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = event.pos

    def update(self, dt):
        self.arc.rotate(5)
        if self.arc.r > 200:
            self.mult = 0.99
        if self.arc.r < 5:
            self.mult = 1.01
        self.arc.scale(self.mult)
        d = np.random.randint(-5, 6, 2)
        self.letterA.move_on(d)
        self.letterA2.shear((self.steps[self.c_s]))
        self.c_s += 1
        self.c_s %= len(self.steps)
        self.letterB.rotate_by_dot(1, (0, 0))
        self.letterB.rotate(-2)
        self.chain.update(self.mouse_x, self.mouse_y, 20)
        self.figures.update()
