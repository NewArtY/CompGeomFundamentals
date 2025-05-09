import pygame

from core.scenes.fractal_scene import FractalScene
from core.scenes.perlin_dyn_grid import PerlinDynamicGridScene
from core.scenes.perlin_dyn_noise import PerlinDynNoiseScene
from core.scenes.perlin_frac_noise import PerlinFracNoiseScene
from core.scenes.perlin_grid import PerlinGridScene
from core.scenes.perlin_noise import PerlinNoiseScene
from core.scenes.perlin_vec_frac_noise import PerlinVecFracNoiseScene
from core.scenes.static_scene import StaticABScene
from core.scenes.t_scene import MovingPointScene
from core.scenes.test_scene import TestScene
from core.scenes.transformation_scene import TransformationScene
from core.scenes.base_scene import Scene


class SceneManager:
    def __init__(self, engine):
        from core.engine import Engine

        self.engine: Engine = engine  # Ссылка на движок
        self.scenes: dict[str, Scene] = {}  # Словарь всех сцен
        self.current_scene: Scene | None = None  # Текущая активная сцена
        self.transitions: dict[str, dict] = {}  # Переходы с условиями {from_scene: {condition: to_scene}}
        self.default_transitions: dict[str, str] = {}  # Переходы по умолчанию {from_scene: to_scene}
        self.history: list[str] = []  # История сцен для возможности возврата
        self.max_history = 10  # Ограничение размера истории

    def init_scenes(self):
        """Инициализирует все начальные сцены"""
        def click_checker(context: dict):
            return context.get('click') == 't'

        self.add_scene("main", StaticABScene())
        self.add_scene("trajectories", MovingPointScene())
        self.add_scene("transformation", TransformationScene())
        self.add_scene("test", TestScene())
        self.add_scene("fractal", FractalScene())
        self.add_scene("perlin_static_grid", PerlinGridScene())
        self.add_scene("perlin_noise_static", PerlinNoiseScene())
        self.add_scene("perlin_frac_noise", PerlinFracNoiseScene())
        self.add_scene("effective_perlin", PerlinVecFracNoiseScene())
        self.add_scene("perlin_dyn", PerlinDynamicGridScene())
        self.add_scene("perlin_dynamic_noise", PerlinDynNoiseScene())

        list_of_scenes = [val for val, _ in self.scenes.items()]

        self.set_scene(list_of_scenes[0])

        self.add_transition(list_of_scenes[0], list_of_scenes[1])
        self.add_transition(list_of_scenes[0], list_of_scenes[3], click_checker)
        self.add_transition(list_of_scenes[1], list_of_scenes[2])
        self.add_transition(list_of_scenes[2], list_of_scenes[4])
        self.add_transition(list_of_scenes[2], list_of_scenes[9], click_checker)
        self.add_transition(list_of_scenes[3], list_of_scenes[1])
        self.add_transition(list_of_scenes[4], list_of_scenes[5])
        self.add_transition(list_of_scenes[5], list_of_scenes[6])
        self.add_transition(list_of_scenes[6], list_of_scenes[7])
        self.add_transition(list_of_scenes[7], list_of_scenes[8])
        self.add_transition(list_of_scenes[8], list_of_scenes[9])
        self.add_transition(list_of_scenes[9], list_of_scenes[10])
        self.add_transition(list_of_scenes[10], list_of_scenes[0])

    def add_scene(self, name, scene: Scene):
        """Добавляет сцену в менеджер"""
        self.scenes[name] = scene
        scene.engine = self.engine  # Передаем ссылку на движок в сцену
        scene.name = name
        return self  # Для цепочки вызовов

    def set_scene(self, name, save_history=True):
        """Устанавливает текущую сцену"""
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' not found")

        # Сохраняем предыдущую сцену в историю
        if self.current_scene and save_history:
            self.history.append(self.current_scene.name)
            if len(self.history) > self.max_history:
                self.history.pop(0)

        # Завершаем работу текущей сцены
        if self.current_scene:
            self.current_scene.on_exit()

        # Очищаем экран при переключении сцен
        self.engine.screen.fill((0, 0, 0))
        pygame.display.flip()

        # Устанавливаем новую сцену
        self.current_scene = self.scenes[name]
        self.current_scene.on_enter()

        return self  # Для цепочки вызовов

    def add_transition(self, from_scene, to_scene, condition=None):
        """Добавляет переход между сценами, опционально с условием"""
        if from_scene not in self.transitions:
            self.transitions[from_scene] = {}

        if condition:
            self.transitions[from_scene][condition] = to_scene
        else:
            self.default_transitions[from_scene] = to_scene

        return self  # Для цепочки вызовов

    def check_transitions(self, current_scene, **context):
        """Проверяет, есть ли подходящий переход из текущей сцены"""
        if current_scene in self.transitions:
            for condition, next_scene in self.transitions[current_scene].items():
                if condition(context):
                    return next_scene

        if current_scene in self.default_transitions:
            return self.default_transitions[current_scene]

        return None

    def next_scene(self, **context):
        """Переход к следующей сцене согласно установленным переходам"""
        if not self.current_scene:
            return False

        next_scene_name = self.check_transitions(self.current_scene.name, **context)
        if next_scene_name:
            self.set_scene(next_scene_name)
            return True
        return False

    def previous_scene(self):
        """Возвращает к предыдущей сцене из истории"""
        if not self.history:
            return False

        prev_scene = self.history.pop()
        self.set_scene(prev_scene, save_history=False)
        return True

    def render_navigation_hint(self):
        """Отображает подсказку о навигации между сценами с учетом настроек текущей сцены"""
        if not self.current_scene:
            return

        # Проверяем, нужно ли показывать подсказки для этой сцены
        if not self.current_scene.fast_forward_available and not self.current_scene.backward_available:
            return

        font = pygame.font.Font(None, 24)
        current_x = 10
        screen_bottom = self.engine.screen.get_height() - 10

        # Подсказка для перехода вперед
        if self.current_scene.fast_forward_available:
            text1 = font.render("Нажмите ", True, (255, 255, 255))
            text2 = font.render("n", True, (255, 0, 0))
            text3 = font.render(", чтобы перейти далее", True, (255, 255, 255))

            text_rect1 = text1.get_rect()
            text_rect1.bottomleft = (current_x, screen_bottom)
            self.engine.screen.blit(text1, text_rect1)
            current_x += text_rect1.width

            text_rect2 = text2.get_rect()
            text_rect2.bottomleft = (current_x, screen_bottom)
            self.engine.screen.blit(text2, text_rect2)
            current_x += text_rect2.width

            text_rect3 = text3.get_rect()
            text_rect3.bottomleft = (current_x, screen_bottom)
            self.engine.screen.blit(text3, text_rect3)
            current_x += text_rect3.width

        # Подсказка для возврата назад
        if self.current_scene.backward_available and self.history:
            if self.current_scene.fast_forward_available:
                # Добавляем разделитель, если есть обе подсказки
                separator = font.render("   ||   ", True, (255, 255, 255))
                sep_rect = separator.get_rect()
                sep_rect.bottomleft = (current_x, screen_bottom)
                self.engine.screen.blit(separator, sep_rect)
                current_x += sep_rect.width

            back1 = font.render("Нажмите ", True, (255, 255, 255))
            back2 = font.render("b", True, (255, 0, 0))
            back3 = font.render(", чтобы вернуться назад", True, (255, 255, 255))

            back_rect1 = back1.get_rect()
            back_rect1.bottomleft = (current_x, screen_bottom)
            self.engine.screen.blit(back1, back_rect1)
            current_x += back_rect1.width

            back_rect2 = back2.get_rect()
            back_rect2.bottomleft = (current_x, screen_bottom)
            self.engine.screen.blit(back2, back_rect2)
            current_x += back_rect2.width

            back_rect3 = back3.get_rect()
            back_rect3.bottomleft = (current_x, screen_bottom)
            self.engine.screen.blit(back3, back_rect3)
