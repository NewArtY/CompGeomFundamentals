import pygame

from core.scenes.base_scene import Scene
from geometry.primitives import Point
from geometry.shapes import LetterA
from trajectory.circle_trajectory import CircleTrajectory
from trajectory.letter_a_trajectory import LetterATrajectory


class MovingPointScene(Scene):
    def __init__(self):
        super().__init__()
        self.point_1: Point | None = None
        self.point_2: Point | None = None
        self.point_3: Point | None = None
        self.letter_a: LetterA | None = None
        self.circle_t = None
        self.letter_a_t = None

    def on_enter(self):
        height_a = 300
        self.letter_a = LetterA(center=(height_a // 2, height_a // 2), h=height_a, color=(50, 50, 50))
        self.point_1 = Point((-100, 0), (255, 0, 0))
        self.point_2 = Point((0, 0), (0, 255, 0))
        self.point_3 = Point((100, 0), (255, 255, 255))
        gen_1 = CircleTrajectory()
        gen_2 = LetterATrajectory(h=height_a)
        self.circle_t = gen_1.create_generator(step=0.02)
        self.letter_a_t = gen_2.create_generator()

    def on_exit(self):
        self.renderer.clear_all()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.engine.set_scene('main')

    def update(self, dt):
        self.point_1.move_on(next(self.circle_t))
        self.point_2.move_on(next(self.letter_a_t))
        self.point_3.move_on(next(self.circle_t))
