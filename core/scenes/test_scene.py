import pygame

from core.scenes.base_scene import Scene
from geometry.primitives import Polyline, Point
from geometry.shapes import LetterVWithBase


class TestScene(Scene):
    def __init__(self):
        super().__init__()
        self.grid: list[Polyline] | None = None
        self.point: Point | None = None
        self.v_letter: LetterVWithBase | None = None
        self.action_flag: int | None = None
        self.k_flag: bool | None = None
        self.active_step: tuple | None = None
        self.active_angle: int | float | None = None

    def on_enter(self):
        self.grid = [Polyline(coors=((val, -320), (val, 320)), color=(255, 255, 255)) for val in range(-400, 401, 50)]
        self.grid += [Polyline(coors=((-400, val), (400, val)), color=(255, 255, 255)) for val in range(-300, 320, 50)]
        self.v_letter = LetterVWithBase(h=50, center=(25, 50), color=(0, 0, 255))
        print(self.v_letter.base_point.coors)
        self.v_letter.rotate_by_dot(60, (0, 0))
        print(self.v_letter.base_point.coors)
        self.point = Point((0, 0), color=(255, 0, 0))
        self.action_flag = 0

    def on_exit(self):
        self.renderer.clear_all()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.engine.scene_manager.next_scene()
            if event.key == pygame.K_b:
                self.engine.scene_manager.previous_scene()
            if event.key == pygame.K_t:
                self.testing()
            if event.key == pygame.K_s:
                self.k_flag = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.k_flag = False

    def update(self, dt):
        if self.k_flag:
            self.testing()

    def testing(self):
        if self.action_flag == 0:
            print('Копируем информацию перед новой итерацией.')
            self.active_step = (self.v_letter.base_point.coors[0], self.v_letter.base_point.coors[1])
            self.active_angle = self.v_letter.base_angle
            print('Лог:')
            print('Перед перемещением: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
            self.v_letter.move_on((-self.active_step[0], -self.active_step[1]))
            print('После перемещения: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
        elif self.action_flag == 1:
            print('Перед поворотом: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
            self.v_letter.rotate_by_dot(-self.active_angle, (0, 0))
            print('После поворота: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
        elif self.action_flag == 2:
            print('Перед наклоном: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
            self.v_letter.shear_by_segment(0.02, ((0, 0), 0))
            print('После наклона: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
        elif self.action_flag == 3:
            print('Перед поворотом: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
            self.v_letter.rotate_by_dot(self.active_angle, (0, 0))
            print('После поворота: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
        elif self.action_flag == 4:
            print('Перед перемещением: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
            self.v_letter.move_on(self.active_step)
            print('После перемещения: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
            print('!!!Наклон закончен!!!')
        elif self.action_flag == 5:
            print('Перед поворотом: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
            self.v_letter.rotate_by_dot(10, (0, 0))
            print('После поворота: ', self.v_letter.base_point.coors, self.v_letter.base_angle)
            print('!!!После-наклонный поворот закончен!!!')
        self.action_flag += 1
        self.action_flag %= 6
