"""Circumcircle class container module.

This module contains the Circumcircle class, which is used to calculate the
circumcenter and circumradius of a triangle, given its three vertices as 2D
coordinates.

Author:
    Paulo Sanchez (@erlete)
"""


from itertools import combinations
from math import sqrt

from bidimensional.coordinates import Coordinate


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

    def __init__(self, a: Coordinate, b: Coordinate,
                 c: Coordinate) -> None:

        # The initial setting variable allows value validation via attribute
        #   setters but prevents automatic recalculation of the circumcenter
        #   and circumradius.

        self._initial_setting = False

        self._a = a
        self._b = b
        self._c = c

        self._initial_setting = True

        self._calculate()  # Initial calculation:

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

        if not self._initial_setting:
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

        if not self._initial_setting:
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

        if not self._initial_setting:
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

        if not (self._a.x * (self._b.y - self._c.y)
                + self._b.x * (self._c.y - self._a.y)
                + self._c.x * (self._a.y - self._b.y)):

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
