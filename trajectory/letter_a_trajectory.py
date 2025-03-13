import numpy as np

from geometry.utils import generate_points_on_polygon
from trajectory.base_trajectory import Trajectory


class LetterATrajectory(Trajectory):
    def __init__(self, loop: bool = True, speed: int | float = 1., h: int | float = 100):
        super().__init__(loop=loop, speed=speed)
        self.height = h
        coors_a = np.array([
            [-h / 2, -h / 2],
            [0, h / 2],
            [h / 2, -h / 2],
            [h / 4, 0],
            [-h / 4, 0],
            [-h / 2, -h / 2]
        ])
        self.coors = generate_points_on_polygon(coors_a, speed)
        self.prev_state = 0

    def get_point(self, t):
        t = max(int(t), 1)
        current_index = (self.prev_state + t) % len(self.coors)
        current_point = self.coors[current_index]
        current_step = current_point - self.coors[self.prev_state]
        self.prev_state = current_index
        return current_step


if __name__ == '__main__':
    obj = LetterATrajectory(h=300)
    print(obj.coors)
