import pygame

from geometry.primitives import Arc
from geometry.shapes import LetterA, LetterB, NewLetterA
from renderers.shape_render import RenderManager


class Engine:
    def __init__(self, width=800, height=600, title="Geometry App"):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = False
        self.render = RenderManager.get_instance()
        self.fps = 60
        self.letterA = None
        self.newLetterA = None

    def process_events(self):
        """Обработка событий Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    self.letterA.shapes[0].color = (0, 255, 0)

    def start_scene(self):
        LetterA(h=100, color=(0, 0, 255), center=(0, -50))
        self.letterA = LetterA(h=200)
        self.newLetterA = NewLetterA(center=(0, -200), h=150)
        LetterB(center=(0, 125))
        Arc((0, 0), 100, 30, 150, (255, 0, 0))

    def update(self):
        """Обновление состояния игры/приложения"""
        self.newLetterA.update()

    def rendering(self):
        """Отрисовка кадра"""
        self.screen.fill((0, 0, 0))  # Очистка экрана
        self.render.render_all(self.screen)
        pygame.display.flip()  # Обновление экрана

    def run(self):
        """Основной игровой цикл"""
        self.running = True
        self.start_scene()

        while self.running:
            # Три основных этапа игрового цикла
            self.process_events()
            self.update()
            self.rendering()
            # Ограничение FPS
            self.clock.tick(self.fps)

        pygame.quit()
