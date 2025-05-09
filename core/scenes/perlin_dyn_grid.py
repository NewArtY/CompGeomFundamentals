import numpy as np
import pygame

from core.scenes.base_scene import Scene
from geometry.primitives import Polyline
from geometry.shapes import Arrow


class PerlinDynamicGridScene(Scene):
    def __init__(self):
        super().__init__()
        self.grid: list[Polyline] | None = None
        self.max_size: int | None = None
        self.start_cells_count = 8
        self.vecs: None | np.ndarray = None
        self.arrows: None | list[list[Arrow]] = None

    def on_enter(self):
        self.max_size = min(self.engine.screen.get_size()) - 80

        def random_unit_vector():
            theta = np.random.uniform(0, 2 * np.pi)
            return np.cos(theta), np.sin(theta)

        list_of_vec = [[((-self.max_size // 2 + i * (self.max_size // self.start_cells_count),
                          -self.max_size // 2 + j * (self.max_size // self.start_cells_count)),
                         random_unit_vector())
                        for i in range(self.start_cells_count + 1)]
                       for j in range(self.start_cells_count + 1)]

        self.vecs = np.array(list_of_vec)
        self.arrows = [
            [
                Arrow(self.vecs[i][j][0], self.vecs[i][j][1], 40, (255, 0, 255))
                for i in range(self.start_cells_count + 1)
            ]
            for j in range(self.start_cells_count + 1)
        ]

        self.grid = [Polyline(coors=((val, -self.max_size // 2), (val, self.max_size // 2)), color=(255, 255, 255))
                     for val in range(-self.max_size // 2,
                                      1 + self.max_size // 2,
                                      self.max_size // self.start_cells_count)
                     ]
        self.grid += [Polyline(coors=((-self.max_size // 2, val), (self.max_size // 2, val)), color=(255, 255, 255))
                      for val in range(-self.max_size // 2,
                                      1 + self.max_size // 2,
                                      self.max_size // self.start_cells_count)
                      ]

    def on_exit(self):
        self.renderer.clear_all()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.engine.scene_manager.next_scene()
            if event.key == pygame.K_b:
                self.engine.scene_manager.previous_scene()

    def update(self, dt):
        for arrows_array in self.arrows:
            for arrow in arrows_array:
                arrow.rotate(5)
