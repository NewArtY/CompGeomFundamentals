import numpy as np

from trajectory.base_trajectory import Trajectory


class CircleTrajectory(Trajectory):
    def __init__(self, loop: bool = True, speed: int | float = 1.0, r: int | float = 100, center: tuple = (0, 0),
                 clockwise: bool = False):
        super().__init__(loop=loop, speed=speed)
        self.r = r
        self.center = np.array(center, dtype=np.float64)
        self.clockwise = clockwise
        self.prev_state = self.center + np.array([r, 0])

    def get_point(self, t):
        if self.clockwise:
            t *= -1
        fi = 2*np.pi*t
        current_point = self.center + self.r * np.array([np.cos(fi), np.sin(fi)])
        current_step = current_point - self.prev_state
        self.prev_state = current_point
        return current_step
