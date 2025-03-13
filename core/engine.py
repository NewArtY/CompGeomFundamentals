import pygame
from time import time


class Engine:
    def __init__(self, width=800, height=600, title="Geometry App"):
        from core.scenes.base_scene import Scene

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = 60
        self.dt = 0  # delta time
        self.scenes = {}
        self.current_scene: Scene | None = None

    def add_scene(self, name, scene):
        """Добавляет сцену в движок"""
        self.scenes[name] = scene
        scene.engine = self  # Передаем ссылку на движок в сцену

    def set_scene(self, name):
        """Устанавливает текущую сцену"""
        if name in self.scenes:
            # Завершаем работу текущей сцены, если она существует
            if self.current_scene:
                self.current_scene.on_exit()

            # Очищаем экран при переключении сцен
            self.screen.fill((0, 0, 0))
            pygame.display.flip()  # Обновляем дисплей, чтобы изменения стали видны

            # Устанавливаем новую сцену
            self.current_scene = self.scenes[name]
            self.current_scene.on_enter()

    def message_btw_scenes(self):
        font = pygame.font.Font(None, 24)
        text1 = font.render("Нажмите ", True, (255, 255, 255))
        text2 = font.render("n", True, (255, 0, 0))
        text3 = font.render(", чтобы перейти к следующей сцене", True, (255, 255, 255))
        text_rect1 = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()
        text_rect1.bottomleft = (10, self.screen.get_height() - 10)
        text_rect2.bottomleft = (text_rect1.right, self.screen.get_height() - 10)
        text_rect3.bottomleft = (text_rect2.right, self.screen.get_height() - 10)
        self.screen.blit(text1, text_rect1)
        self.screen.blit(text2, text_rect2)
        self.screen.blit(text3, text_rect3)

    def process_events(self):
        """Обработка событий Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.current_scene:
                self.current_scene.handle_event(event)

    def update(self):
        """Обновление состояния игры/приложения"""
        if self.current_scene:
            self.current_scene.update(self.dt)

    def rendering(self):
        """Отрисовка кадра"""
        self.screen.fill((0, 0, 0))  # Очистка экрана
        if self.current_scene:
            self.message_btw_scenes()  # Сообщение между сценами
            self.current_scene.render(self.screen)  # Отрисовка сцены
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
