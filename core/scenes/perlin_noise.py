import numpy as np
import pygame
from itertools import product

from core.config import FOREGROUND
from core.scenes.base_scene import Scene
from geometry.primitives import Polyline, Point


class PerlinNoiseScene(Scene):
    def __init__(self):
        super().__init__()
        self.grid: list[Polyline] | None = None
        self.max_size: int | None = None
        self.start_cells_count = 8
        self.vecs: None | np.ndarray = None

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

        def random_unit_vector():
            theta = np.random.uniform(0, 2 * np.pi)
            return np.cos(theta), np.sin(theta)

        def f(t: int | float) -> int | float:
            return 6*t**5 - 15*t**4 + 10*t**3

        def lerp(a: int | float, b: int | float, t: int | float) -> int | float:
            return a + t*(b - a)

        list_of_vec = [[random_unit_vector()
                        for _ in range(self.start_cells_count + 1)]
                       for _ in range(self.start_cells_count + 1)]

        self.vecs = np.array(list_of_vec)

        start_x, start_y = -self.max_size // 2, -self.max_size // 2
        perlin_dots = np.zeros((self.max_size, self.max_size), dtype=np.float64)
        for x, y in product(range(self.max_size), repeat=2):
            x_r, y_r = self.start_cells_count * x / self.max_size, self.start_cells_count * y / self.max_size
            ind_x, ind_y = int(x_r), int(y_r)
            d = [
                [np.array([x_r - ind_x, y_r - ind_y]), np.array([x_r - ind_x, y_r - ind_y - 1])],
                [np.array([x_r - ind_x - 1, y_r - ind_y]), np.array([x_r - ind_x - 1, y_r - ind_y - 1])]
            ]
            s = [
                [sum(d[i][j]*self.vecs[i + ind_x][j + ind_y]) for j in range(2)]
                for i in range(2)
            ]
            u_dot, v_dot = f(x_r - ind_x), f(y_r - ind_y)
            val = perlin_dots[x][y] = lerp(
                lerp(s[0][0], s[1][0], u_dot),
                lerp(s[0][1], s[1][1], u_dot),
                v_dot
            )
            Point(coors=(start_x + x, start_y + y),
                  color=(int(255*(val+1)/2), int(255*(val+1)/2), int(255*(val+1)/2)),
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


if __name__ == '__main__':
    scene = PerlinNoiseScene()
    scene.on_enter()
