import pygame
from time import time


class Engine:
    def __init__(self, width=800, height=600, title="Geometry App"):
        from geometry.base import BaseModel
        from core.scene_manager import SceneManager

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.scene_manager: SceneManager = SceneManager(self)
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = 60
        self.dt = 0  # delta time
        BaseModel.w = width
        BaseModel.h = height

    def process_events(self):
        """Обработка событий Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.scene_manager.current_scene:
                self.scene_manager.current_scene.handle_event(event)

    def update(self):
        """Обновление состояния игры/приложения"""
        if self.scene_manager.current_scene:
            self.scene_manager.current_scene.update(self.dt)

    def rendering(self):
        """Отрисовка кадра"""
        self.screen.fill((0, 0, 0))  # Очистка экрана
        if self.scene_manager.current_scene:
            self.scene_manager.render_navigation_hint()  # Сообщение между сценами
            self.scene_manager.current_scene.render(self.screen)  # Отрисовка сцены
        pygame.display.flip()  # Обновление экрана

    def run(self):
        """Основной игровой цикл"""
        self.running = True
        last_time = time()

        while self.running:
            # Вычисление delta time
            current_time = time()
            self.dt = current_time - last_time
            last_time = current_time

            # Три основных этапа игрового цикла
            self.process_events()
            self.update()
            self.rendering()

            # Ограничение FPS
            self.clock.tick(self.fps)

        pygame.quit()
