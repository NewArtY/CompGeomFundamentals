import numpy as np
import pygame
from itertools import product

from core.config import FOREGROUND
from core.scenes.base_scene import Scene
from geometry.primitives import Polyline, Point


class RadialPerlinScene(Scene):
    def __init__(self):
        super().__init__()
        self.grid: list[Polyline] | None = None
        self.max_size: int | None = None
        self.vecs: None | np.ndarray = None

        self.start_cells_count = 8
        self.octave_count = 4
        self.persist = 0.5
        self.lacunar = 2
        self.offset = [0, 0]

        self.island_center: tuple[int, int] | None = (4, 4)
        self.island_rad = self.start_cells_count / 1.5
        self.island_peek = 3
        self.island_octaves = {0, 1, 2}

        self.coloring: dict[float, tuple[int, int ,int]] = {
            -0.7: (10, 0, 160),
            -0.2: (0, 125, 255),
            0.: (10, 220, 255),
            0.1: (255, 255, 100),
            0.7: (30, 200, 10),
            0.95: (100, 70, 10),
            1: (255, 255, 255)
        }
        self.thresholds = np.array(sorted(self.coloring.keys()))
        self.colors = np.array([self.coloring[k] for k in self.thresholds])

    def on_enter(self):
        self.max_size = min(self.engine.screen.get_size()) - 80

        def island_mask(x_c, y_c, n):
            return self.island_peek * np.exp(-((x_c - self.island_center[0] * self.lacunar ** n)**2 +
                                               (y_c - self.island_center[1] * self.lacunar ** n)**2)/
                                             (2*self.island_rad**2))

        def get_color(x):
            idx = np.searchsorted(self.thresholds, x, side='left')
            return self.colors[idx]

        font = pygame.font.Font(None, 42)
        text = font.render("Wait...", True, (240, 20, 10))
        text_rect = text.get_rect()
        screen_left = (self.engine.screen.get_width() - text_rect.width) // 2
        screen_bottom = (self.engine.screen.get_height() + text_rect.height) // 2
        text_rect.bottomleft = (screen_left, screen_bottom)
        self.engine.screen.blit(text, text_rect)
        pygame.display.flip()

        self.vecs = []
        for n in range(self.octave_count):
            size = self.start_cells_count * (self.lacunar ** n)
            grid_size = int(size) + 1
            thetas = np.random.uniform(0, 2 * np.pi, (grid_size, grid_size))
            octave_vecs = np.stack([np.cos(thetas), np.sin(thetas)], axis=-1)
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

            if n in self.island_octaves:
                mask = island_mask(x_r, y_r, n)
                perlin_octave += mask

            perlin_noise += self.persist ** n * perlin_octave

        # Нормализация
        perlin_noise = (perlin_noise - np.min(perlin_noise)) / (np.max(perlin_noise) - np.min(perlin_noise))
        perlin_noise *= 2
        perlin_noise -= 1

        # Визуализация
        for x, y in product(range(self.max_size), repeat=2):
            color = get_color(perlin_noise[y, x])
            Point(coors=(x - self.max_size // 2, y - self.max_size // 2),
                  color=color,
                  layer=FOREGROUND)


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

