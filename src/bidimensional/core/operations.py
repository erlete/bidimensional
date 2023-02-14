"""2D operations module.

This module contains methods used to perform operations on 2D coordinates, such
as calculating distances and angles between them.

Author:
    Paulo Sanchez (@erlete)
"""


import math
from itertools import combinations

from .coordinates import Coordinate


def distance(a: Coordinate, b: Coordinate) -> float:
    """Calculates the distance between two coordinates.

    Args:
        a (Coordinate): First coordinate.
        b (Coordinate): Second coordinate.

    Raises:
        TypeError: If a or b are not Coordinate objects.

    Returns:
        float: Distance between the two coordinates.
    """

    if not all(isinstance(x, Coordinate) for x in (a, b)):
        raise TypeError("a and b must be Coordinate instances")

    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def angle(a: Coordinate, b: Coordinate, c: Coordinate) -> float:
    """Calculates the angle between three coordinates.

    Args:
        a (Coordinate): First coordinate.
        b (Coordinate): Second coordinate.
        c (Coordinate): Third coordinate.

    Raises:
        TypeError: If a, b or c are not Coordinate objects.

    Returns:
        float: Angle between the three coordinates.
    """

    if not all(isinstance(x, Coordinate) for x in (a, b, c)):
        raise TypeError("a, b and c must be Coordinate instances")

    e1 = distance(b, c)
    e2 = distance(a, c)
    e3 = distance(a, b)

    return math.degrees(math.acos(
        (math.pow(e2, 2) + math.pow(e3, 2) - math.pow(e1, 2)) / (2 * e2 * e3)
    ))


def midpoint(a: Coordinate, b: Coordinate) -> Coordinate:
    """Calculates the midpoint between two coordinates.

    Args:
        a (Coordinate): First coordinate.
        b (Coordinate): Second coordinate.

    Raises:
        TypeError: If a or b are not Coordinate objects.

    Returns:
        Coordinate: Midpoint between the two coordinates.
    """

    if not all(isinstance(x, Coordinate) for x in (a, b)):
        raise TypeError("a and b must be Coordinate instances")

    return Coordinate((a.x + b.x) / 2, (a.y + b.y) / 2)


def area(*vertices: Coordinate):
    """Calculate the area of a polygon.

    Args:
        *vertices (Coordinate): vertices of the polygon.

    Returns:
        float: area of the polygon.
    """
    x = [vertex.x for vertex in vertices]
    y = [vertex.y for vertex in vertices]

    area: float = 0

    j = -1
    for i in range(len(vertices)):
        area += (x[j] + x[i]) * (y[j] - y[i])
        j = i

    return area / 2


def perimeter(*coordinates: Coordinate) -> float:
    """Calculates the perimeter of a polygon.

    Args:
        *coordinates (Coordinate): Coordinates of the polygon.

    Raises:
        TypeError: If any of the coordinates are not Coordinate objects.

    Returns:
        float: Perimeter of the polygon.
    """

    if not all(isinstance(x, Coordinate) for x in coordinates):
        raise TypeError("All coordinates must be Coordinate instances")

    return sum(distance(*pair) for pair in combinations(coordinates, 2))
