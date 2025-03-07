def distance(from_point: tuple[int, int], to_point: tuple[int, int]) -> float:
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
