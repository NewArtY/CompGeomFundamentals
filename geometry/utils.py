import numpy as np


def distance(from_point: tuple[int | float, int | float],
             to_point: tuple[int | float, int | float]) -> float:
    """
    Euclidian distance from one point to another
    :param from_point: first dot of the interval
    :param to_point: second dot of the interval
    """
    return ((from_point[0] - to_point[0])**2 + (from_point[1] - to_point[1])**2)**(1/2)


def interpolation_with_length(length: int | float, coors: tuple) -> tuple:
    """
    Interpolation of each line segment of the polygonal chain
    :param length: length of the partition line segment
    :param coors: coordinates of the polygonal chain vertices
    """
    new_coors = (coors[0], )
    for dot1, dot2 in zip(coors[:-1], coors[1:]):
        n = int(distance(dot1, dot2)/length)
        for i in range(1, n + 1):
            new_coors += ((dot1[0] + (dot2[0] - dot1[0])*(i/n), dot1[1] + (dot2[1] - dot1[1])*(i/n)), )
    return new_coors


def generate_equidistant_points(point1, point2, n):
    t = np.linspace(0, 1, n).reshape(-1, 1)
    return (1 - t) * point1 + t * point2


def generate_points_at_dist(point1, point2, dist):
    vec = point2 - point1
    n = max(1 + int(np.sqrt(vec[0]**2 + vec[1]**2)/dist), 2)
    return generate_equidistant_points(point1, point2, n)


def generate_points_on_polygon(polygon, dist):
    result = np.array([]).reshape(-1, 2)
    for point1, point2 in zip(polygon[:-1], polygon[1:]):
        result = np.vstack((result, generate_points_at_dist(point1, point2, dist)[:-1]))
    return result


def get_step(from_point: np.ndarray, to_point: np.ndarray, length: int | float, accuracy: int | float | None = None):
    vec = to_point - from_point
    dist = np.sqrt(vec[0]**2 + vec[1]**2)
    if accuracy is None:
        accuracy = length / 2
    if dist < accuracy:
        return np.array([0., 0.])
    return length * vec / dist


if __name__ == '__main__':
    print(generate_equidistant_points(np.array([1, 1]), np.array([5, 10]), 14))
