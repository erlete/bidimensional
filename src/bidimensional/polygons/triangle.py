"""Triangle polygon utilities module.

This module contains all utilities related to the triangle polygon, such as
calculating the area, perimeter, circumcenter and circumradius, etc.

Author:
    Paulo Sanchez (@erlete)
"""


from __future__ import annotations

from itertools import combinations, permutations
from math import sqrt

import matplotlib.pyplot as plt

from ..core import operations as op
from ..core.coordinates import Coordinate
from ..core.lines import Segment


class Circumcircle:
    """Circumcirle calculation utility.

    This class is used to calculate the circumcenter and circumradius of a
    triangle, given its three vertices as 2D coordinates.

    Args:
        a (Coordinate): First vertex of the triangle.
        b (Coordinate): Second vertex of the triangle.
        c (Coordinate): Third vertex of the triangle.

    Attributes:
        a (Coordinate): First vertex of the triangle.
        b (Coordinate): Second vertex of the triangle.
        c (Coordinate): Third vertex of the triangle.
        center (Coordinate): The center of the circumcircle.
        radius (float): The radius of the circumcircle.
    """

    def __init__(self, a: Coordinate, b: Coordinate, c: Coordinate) -> None:
        self._a = a
        self._b = b
        self.c = c  # Automatically calls `Circumcircle._calculate` method.

    @property
    def a(self) -> Coordinate:
        """First vertex of the triangle.

        Returns:
            Coordinate: First vertex of the triangle.

        Note:
            If the value of the vertex is changed, the circumcenter and
            circumradius are recalculated.
        """

        return self._a

    @a.setter
    def a(self, value: Coordinate) -> None:
        """First vertex of the triangle.

        Args:
            value (Coordinate): First vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate object.

        Note:
            If the value of the vertex is changed, the circumcenter and
            circumradius are recalculated.
        """

        if not isinstance(value, Coordinate):
            raise TypeError("a must be a Coordinate instance")

        self._a = value
        self._calculate()

    @property
    def b(self) -> Coordinate:
        """Second vertex of the triangle.

        Returns:
            Coordinate: Second vertex of the triangle.

        Note:
            If the value of the vertex is changed, the circumcenter and
            circumradius are recalculated.
        """

        return self._b

    @b.setter
    def b(self, value: Coordinate) -> None:
        """Second vertex of the triangle.

        Args:
            value (Coordinate): Second vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate object.

        Note:
            If the value of the vertex is changed, the circumcenter and
            circumradius are recalculated.
        """

        if not isinstance(value, Coordinate):
            raise TypeError("b must be a Coordinate instance")

        self._b = value
        self._calculate()

    @property
    def c(self) -> Coordinate:
        """Third vertex of the triangle.

        Returns:
            Coordinate: Third vertex of the triangle.

        Note:
            If the value of the vertex is changed, the circumcenter and
            circumradius are recalculated.
        """

        return self._c

    @c.setter
    def c(self, value: Coordinate) -> None:
        """Third vertex of the triangle.

        Args:
            value (Coordinate): Third vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate object.

        Note:
            If the value of the vertex is changed, the circumcenter and
            circumradius are recalculated.
        """

        if not isinstance(value, Coordinate):
            raise TypeError("c must be a Coordinate instance")

        self._c = value
        self._calculate()

    @property
    def center(self) -> Coordinate:
        """Center of the circumcircle.

        Returns:
            Coordinate: Center of the circumcircle.
        """

        return self._center

    @property
    def radius(self) -> float:
        """Radius of the circumcircle.

        Returns:
            float: Radius of the circumcircle.
        """

        return self._radius

    def _ensure_non_collinear(self) -> None:
        """Ensures that the triangle is not collinear.

        Raises:
            ValueError: If the triangle is collinear.
        """

        x_displacements = {
            "ab": self.b.x - self.a.x,
            "bc": self.c.x - self.b.x,
            "ac": self.c.x - self.a.x
        }

        y_displacements = {
            "ab": self.b.y - self.a.y,
            "bc": self.c.y - self.b.y,
            "ac": self.c.y - self.a.y
        }

        if (self.a.x == self.b.x == self.c.x
                or self.a.y == self.b.y == self.c.y):

            raise ValueError("The triangle is collinear")

        slopes = []

        if x_displacements["ab"] != 0:
            slopes.append(y_displacements["ab"] / x_displacements["ab"])

        if x_displacements["bc"] != 0:
            slopes.append(y_displacements["bc"] / x_displacements["bc"])

        if x_displacements["ac"] != 0:
            slopes.append(y_displacements["ac"] / x_displacements["ac"])

        if any(slope[0] == slope[1]
               for slope in combinations(slopes, 2)):

            raise ValueError("The triangle is collinear")

    def _calculate(self) -> None:
        """Calculates the center and radius of the circumcircle."""

        self._ensure_non_collinear()

        if any(v[1] - v[0] for v in combinations(
                (self._a, self._b, self._c), 2)):

            # Vertical alignment prevention:

            if not (self._b - self._a).x:
                self._a, self._c = self._c, self._a

            if not (self._c - self._a).x:
                self._a, self._b = self._b, self._a

        # Segment displacement:

        displacement = {
            "ab": Coordinate(
                self.b.x - self.a.x,
                self.b.y - self.a.y
            ),
            "ac": Coordinate(
                self.c.x - self.a.x,
                self.c.y - self.a.y
            )
        }

        # Unitary vectors:

        unitary = {
            "ab": Coordinate(
                displacement["ab"].y / sqrt(
                    displacement["ab"].x ** 2 + displacement["ab"].y ** 2
                ),
                -displacement["ab"].x / sqrt(
                    displacement["ab"].x ** 2 + displacement["ab"].y ** 2
                )
            ),
            "ac": Coordinate(
                displacement["ac"].y / sqrt(
                    displacement["ac"].x ** 2 + displacement["ac"].y ** 2
                ),
                -displacement["ac"].x / sqrt(
                    displacement["ac"].x ** 2 + displacement["ac"].y ** 2
                )
            )
        }

        # V-vector for vertical intersection:

        vertical = {
            "ab": Coordinate(
                unitary["ab"].x / unitary["ab"].y,
                1
            ),
            "ac": Coordinate(
                -(unitary["ac"].x / unitary["ac"].y),
                1
            )
        }

        # Midpoint setting:

        midpoint = {
            "ab": Coordinate(
                displacement["ab"].x / 2 + self.a.x,
                displacement["ab"].y / 2 + self.a.y
            ),
            "ac": Coordinate(
                displacement["ac"].x / 2 + self.a.x,
                displacement["ac"].y / 2 + self.a.y
            )
        }

        # Midpoint height equivalence:

        intersection = Coordinate(
            midpoint["ab"].x + (
                (midpoint["ac"].y - midpoint["ab"].y) / unitary["ab"].y
            ) * unitary["ab"].x,
            midpoint["ac"].y
        )

        # Circumcenter calculation:

        self._center = Coordinate(
            intersection.x + (
                (midpoint["ac"].x - intersection.x)
                / (vertical["ab"].x + vertical["ac"].x)
            ) * vertical["ab"].x,
            intersection.y + (
                midpoint["ac"].x - intersection.x
            ) / (
                vertical["ab"].x + vertical["ac"].x
            )
        )

        # Circumradius calculation:

        self._radius = sqrt(
            (self.a.x - self._center.x) ** 2
            + (self.a.y - self._center.y) ** 2
        )


class Triangle:
    """Triangle class.

    This class represents a triangle in the 2D plane. It is defined by three
    vertices, a, b and c (Coordinate objects). The class provides methods to
    compute the angles of the triangle, the circumcenter and the circumradius.
    It also provides methods used to determine special properties of the
    triangle, such as if it is equilateral, isosceles, scalene, right, obtuse
    or acute.

    Args:
        a (Coordinate): First vertex of the triangle.
        b (Coordinate): Second vertex of the triangle.
        c (Coordinate): Third vertex of the triangle.

    Attributes:
        a (Coordinate): First vertex of the triangle.
        b (Coordinate): Second vertex of the triangle.
        c (Coordinate): Third vertex of the triangle.
        circumcenter (Coordinate): Circumcenter of the triangle.
        circumradius (float): Circumradius of the triangle.
    """

    _ERROR_MSGS = {
        "TypeError1": "value must be a Triangle instance"
    }

    TOL_DIGITS = 10

    def __init__(self, a: Coordinate, b: Coordinate, c: Coordinate) -> None:

        self._properties = {}

        self.a = a
        self.b = b
        self.c = c

    @property
    def a(self) -> Coordinate:
        """First vertex of the triangle.

        Returns:
            Coordinate: First vertex of the triangle.
        """

        return self._a

    @a.setter
    def a(self, value: Coordinate) -> None:
        """First vertex of the triangle.

        Args:
            value (Coordinate): First vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate object.
        """

        if not isinstance(value, Coordinate):
            raise TypeError("a must be a Coordinate instance")

        self._a = value
        self._properties.clear()

    @property
    def b(self) -> Coordinate:
        """Second vertex of the triangle.

        Returns:
            Coordinate: Second vertex of the triangle.
        """

        return self._b

    @b.setter
    def b(self, value: Coordinate) -> None:
        """Second vertex of the triangle.

        Args:
            value (Coordinate): Second vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate object.
        """

        if not isinstance(value, Coordinate):
            raise TypeError("b must be a Coordinate instance")

        self._b = value
        self._properties.clear()

    @property
    def c(self) -> Coordinate:
        """Third vertex of the triangle.

        Returns:
            Coordinate: Third vertex of the triangle.
        """

        return self._c

    @c.setter
    def c(self, value: Coordinate) -> None:
        """Third vertex of the triangle.

        Args:
            value (Coordinate): Third vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate object.
        """

        if not isinstance(value, Coordinate):
            raise TypeError("c must be a Coordinate instance")

        self._c = value
        self._properties.clear()

    @property
    def vertices(self) -> dict[str, Coordinate]:
        """Vertices of the triangle.

        Returns:
            dict[str, Coordinate]: Vertices of the triangle.
        """

        if self._properties.get("vertices") is None:
            self._properties["vertices"] = {
                'a': self.a,
                'b': self.b,
                'c': self.c
            }

        return self._properties["vertices"]

    @property
    def sides(self) -> dict[str, float]:
        """Sides of the triangle.

        Returns:
            dict[str, Segment]: Sides of the triangle.
        """

        if self._properties.get("sides") is None:
            self._properties["sides"] = {
                ''.join(pair): Segment(
                    self.vertices.get(pair[0]),
                    self.vertices.get(pair[1])
                ) for pair in permutations(self.vertices.keys(), 2)
            }

        return self._properties["sides"]

    @property
    def area(self) -> float:
        """Area of the triangle.

        Returns:
            float: Area of the triangle.
        """

        if self._properties.get("area") is None:
            self._properties["area"] = op.area(self.a, self.b, self.c)

        return self._properties["area"]

    @property
    def perimeter(self) -> float:
        """Perimeter of the triangle.

        Returns:
            float: Perimeter of the triangle.
        """

        if self._properties.get("perimeter") is None:
            self._properties["perimeter"] = sum(
                side.distance
                for side in set(self.sides.values())
            )

        return self._properties["perimeter"]

    @property
    def angles(self) -> dict[str, float]:
        """Inner angles of the triangle.

        Returns:
            dict[str, float]: Angles of the triangle.
        """

        if self._properties.get("angles") is None:
            self._properties["angles"] = {
                'a': round(op.angle(self.b, self.c, self.a), self.TOL_DIGITS),
                'b': round(op.angle(self.c, self.a, self.b), self.TOL_DIGITS),
                'c': round(op.angle(self.a, self.b, self.c), self.TOL_DIGITS)
            }

        return self._properties["angles"]

    @property
    def circumcenter(self) -> Coordinate:
        """Circumcenter of the triangle.

        Returns:
            Coordinate: Circumcenter of the triangle.
        """

        if self._properties.get("circumcircle") is None:
            self._properties["circumcircle"] = Circumcircle(
                self.a, self.b, self.c
            )

        return self._properties["circumcircle"].center

    @property
    def circumradius(self) -> float:
        """Circumradius of the triangle.

        Returns:
            float: Circumradius of the triangle.
        """

        if self._properties.get("circumcircle") is None:
            self._properties["circumcircle"] = Circumcircle(
                self.a, self.b, self.c
            )

        return self._properties["circumcircle"].radius

    def is_right(self) -> bool:
        """Checks if the triangle has a right angle.

        Returns:
            bool: True if the triangle has a right angle, False otherwise.
        """

        return any(
            round(angle_, self.TOL_DIGITS) == 90
            for angle_ in self.angles.values()
        )

    def is_obtuse(self) -> bool:
        """Checks if the triangle has an obtuse angle.

        Returns:
            bool: True if the triangle has an obtuse angle, False otherwise.
        """

        return any(
            angle_ > 90
            for angle_ in self.angles.values()
        )

    def is_acute(self) -> bool:
        """Checks if every angle in the triangle is an acute angle.

        Returns:
            bool: True if the triangle has an acute angle, False otherwise.
        """

        return all(
            angle_ < 90
            for angle_ in self.angles.values()
        )

    def is_equilateral(self) -> bool:
        """Checks if the triangle is equilateral.

        Returns:
            bool: True if the triangle is equilateral, False otherwise.
        """

        return len(set(self.angles.values())) == 1

    def is_isosceles(self) -> bool:
        """Checks if the triangle is isosceles.

        Returns:
            bool: True if the triangle is isosceles, False otherwise.
        """

        return len(set(self.angles.values())) == 2

    def is_scalene(self) -> bool:
        """Checks if the triangle is scalene.

        Returns:
            bool: True if the triangle is scalene, False otherwise.
        """

        return len(set(self.angles.values())) == 3

    def is_collinear(self) -> bool:
        """Checks if the triangle is collinear.

        Returns:
            bool: True if the triangle is collinear, False otherwise.
        """

        x_displacements = {
            "ab": self.b.x - self.a.x,
            "bc": self.c.x - self.b.x,
            "ac": self.c.x - self.a.x
        }

        y_displacements = {
            "ab": self.b.y - self.a.y,
            "bc": self.c.y - self.b.y,
            "ac": self.c.y - self.a.y
        }

        if (self.a.x == self.b.x == self.c.x
                or self.a.y == self.b.y == self.c.y):

            return True

        slopes = []

        if x_displacements["ab"] != 0:
            slopes.append(y_displacements["ab"] / x_displacements["ab"])

        if x_displacements["bc"] != 0:
            slopes.append(y_displacements["bc"] / x_displacements["bc"])

        if x_displacements["ac"] != 0:
            slopes.append(y_displacements["ac"] / x_displacements["ac"])

        if any(slope[0] == slope[1]
               for slope in combinations(slopes, 2)):

            return True

        return False

    def plot(self, ax=None, **kwargs) -> None:
        """Plots the triangle.

        Args:
            ax (matplotlib.axes.Axes, optional): Axes to plot on. Defaults to
                None.
            **kwargs: Keyword arguments for matplotlib.pyplot.plot.
        """

        if ax is None:
            ax = plt.gca()

        ax.plot(
            [self.a.x, self.b.x, self.c.x, self.a.x],
            [self.a.y, self.b.y, self.c.y, self.a.y],
            **kwargs
        )

    def __repr__(self) -> str:
        """String representation of the triangle.

        Returns:
            str: String representation of the triangle.
        """

        return f"Triangle({self.a}, {self.b}, {self.c})"

    def __str__(self) -> str:
        """String representation of the triangle.

        Returns:
            str: String representation of the triangle.
        """

        return f"Triangle({self.a}, {self.b}, {self.c})"

    def __eq__(self, value: Triangle) -> bool:
        """Checks if two triangles are equal.

        Args:
            value (Triangle): Triangle to compare.

        Returns:
            bool: True if the triangles are equal, False otherwise.
        """

        if not isinstance(value, Triangle):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return {self.a, self.b, self.c} == {value.a, value.b, value.c}

    def __ne__(self, value: Triangle) -> bool:
        """Checks if two triangles are not equal.

        Args:
            value (Triangle): Triangle to compare.

        Returns:
            bool: True if the triangles are not equal, False otherwise.
        """

        return not self.__eq__(value)

    def __gt__(self, value: Triangle) -> bool:
        """Checks if a triangle is greater than another.

        Args:
            value (Triangle): Triangle to compare.

        Returns:
            bool: True if the triangle is greater than the other, False
                otherwise.
        """

        if not isinstance(value, Triangle):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self.area > value.area

    def __ge__(self, value: Triangle) -> bool:
        """Checks if a triangle is greater than or equal to another.

        Args:
            value (Triangle): Triangle to compare.

        Returns:
            bool: True if the triangle is greater than or equal to the other,
                False otherwise.
        """

        return self.__gt__(value) or self.__eq__(value)

    def __lt__(self, value: Triangle) -> bool:
        """Checks if a triangle is less than another.

        Args:
            value (Triangle): Triangle to compare.

        Returns:
            bool: True if the triangle is less than the other, False otherwise.
        """

        if not isinstance(value, Triangle):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self.area < value.area

    def __le__(self, value: Triangle) -> bool:
        """Checks if a triangle is less than or equal to another.

        Args:
            value (Triangle): Triangle to compare.

        Returns:
            bool: True if the triangle is less than or equal to the other,
                False otherwise.
        """

        return self.__lt__(value) or self.__eq__(value)

    def __contains__(self, value: Coordinate) -> bool:
        """Checks if a point is inside the triangle.

        Args:
            point (Coordinate): Point to check.

        Returns:
            bool: True if the point is inside the triangle, False otherwise.

        Note:
            This method excludes points on the edges of the triangle up to a
            tolerance of 1e-14. This means that if the point is located exacly
            at the edge of the triangle, it will be considered outside the
            figure, but if it is located 1e-14 units towards the baricenter of
            the triangle, it will be considered inside the figure.

        Reference:
            http://totologic.blogspot.com/2014/01/accurate-point-in-triangle-test.html
        """

        a = (
            (self._b.y - self._c.y) * (value.x - self._c.x)
            + (self._c.x - self._b.x) * (value.y - self._c.y)
        ) / (
            (self._b.y - self._c.y) * (self._a.x - self._c.x)
            + (self._c.x - self._b.x) * (self._a.y - self._c.y)
        )

        b = (
            (self._c.y - self._a.y) * (value.x - self._c.x)
            + (self._a.x - self._c.x) * (value.y - self._c.y)
        ) / (
            (self._b.y - self._c.y) * (self._a.x - self._c.x)
            + (self._c.x - self._b.x) * (self._a.y - self._c.y)
        )

        c = 1 - a - b

        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1
