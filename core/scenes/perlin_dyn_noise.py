import numpy as np
import pygame
from itertools import product

from core.config import FOREGROUND
from core.scenes.base_scene import Scene
from geometry.primitives import Polyline, Point


class PerlinDynNoiseScene(Scene):
    def __init__(self):
        super().__init__()
        self.grid: list[Polyline] | None = None
        self.max_size: int | None = None
        self.vecs: None | list[np.ndarray] = None
        self.thetas: list[np.ndarray] | None = None
        self.delta_thetas: list[int | float] | None = None

        self.start_cells_count = 8
        self.octave_count = 4
        self.persist = 0.5
        self.lacunar = 2
        self.offset = [0, 0]
        self.a_max = (1 - self.persist**self.octave_count) / (1 - self.persist)

    def on_enter(self):
        self.max_size = min(self.engine.screen.get_size()) - 80

        font = pygame.font.Font(None, 42)
        text = font.render("Wait...", True, (240, 20, 10))
        text_rect = text.get_rect()
        screen_left = (self.engine.screen.get_width() - text_rect.width) // 2
        screen_bottom = (self.engine.screen.get_height() + text_rect.height) // 2
        text_rect.bottomleft = (screen_left, screen_bottom)
        self.engine.screen.blit(text, text_rect)
        pygame.display.flip()

        self.vecs = []
        self.thetas = []
        self.delta_thetas = []
        for n in range(self.octave_count):
            self.delta_thetas.append((10 + 5 * n) * np.pi / 180)
            size = self.start_cells_count * (self.lacunar ** n)
            grid_size = int(size) + 1
            thetas = np.random.uniform(0, 2 * np.pi, (grid_size, grid_size))
            self.thetas.append(thetas)
            octave_vecs = np.stack([np.cos(thetas), np.sin(thetas)], axis=-1)
            self.vecs.append(octave_vecs)

    def on_exit(self):
        self.renderer.clear_all()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.engine.scene_manager.next_scene()
            if event.key == pygame.K_b:
                self.engine.scene_manager.previous_scene()

    def update(self, dt):
        self.vecs = []
        for n in range(self.octave_count):
            size = self.start_cells_count * (self.lacunar ** n)
            grid_size = int(size) + 1
            dt = np.full((grid_size, grid_size), self.delta_thetas[n])
            self.thetas[n] += dt
            octave_vecs = np.stack([np.cos(self.thetas[n]), np.sin(self.thetas[n])], axis=-1)
            self.vecs.append(octave_vecs)

        x_grid, y_grid = np.meshgrid(np.arange(self.max_size), np.arange(self.max_size))
        perlin_noise = np.zeros((self.max_size, self.max_size), dtype=np.float64)
        for n in range(self.octave_count):
            octave_max_w = self.start_cells_count * (self.lacunar ** n)
            x_r = (self.lacunar ** n * self.start_cells_count * x_grid / self.max_size + self.offset[0]) % octave_max_w
            y_r = (self.lacunar ** n * self.start_cells_count * y_grid / self.max_size + self.offset[1]) % octave_max_w
            ind_x, ind_y = x_r.astype(int), y_r.astype(int)
            dx, dy = x_r - ind_x, y_r - ind_y
            u = 6 * dx ** 5 - 15 * dx ** 4 + 10 * dx ** 3
            v = 6 * dy ** 5 - 15 * dy ** 4 + 10 * dy ** 3
            perlin_octave = np.zeros_like(x_grid, dtype=np.float64)
            for i, j in product(range(2), repeat=2):
                ix, iy = ind_x + i, ind_y + j
                dx_vec, dy_vec = dx - i, dy - j
                gradients = self.vecs[n][ix, iy]
                dot_products = gradients[:, :, 0] * dx_vec + gradients[:, :, 1] * dy_vec
                weight_x = u if i == 1 else 1 - u
                weight_y = v if j == 1 else 1 - v
                perlin_octave += dot_products * weight_x * weight_y
            perlin_noise += self.persist ** n * perlin_octave
        perlin_noise /= self.a_max
        normalized_noise = (perlin_noise + 1) / 2 * 255

        self.renderer.clear_all()
        for x, y in product(range(self.max_size), repeat=2):
            gray_value = int(normalized_noise[y, x])
            Point(coors=(x - self.max_size // 2, y - self.max_size // 2),
                  color=(gray_value, gray_value, gray_value),
                  layer=FOREGROUND)
