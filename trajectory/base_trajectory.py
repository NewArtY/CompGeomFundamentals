from abc import ABC, abstractmethod


class Trajectory(ABC):
    """Базовый класс для всех типов траекторий"""

    def __init__(self, **kwargs):
        self.loop = kwargs.get('loop', False)  # Зацикленность траектории
        self.speed = kwargs.get('speed', 1.0)  # Скорость движения

    @abstractmethod
    def get_point(self, t):
        """
        Получить точку на траектории для параметра t
        t обычно в диапазоне [0, 1], где 0 - начало, 1 - конец
        """
        pass

    def create_generator(self, step=0.01):
        """Создает генератор для получения последовательных точек"""
        t = 0
        while t <= 1 or self.loop:
            t %= 1
            yield self.get_point(t)
            t += step * self.speed
