"""Circumcenter class container module.

This module contains the Circumcenter class, which is used to calculate the
circumcenter of a triangle, given its three vertices as 2D coordinates.

Note:
    By default, this module uses the Coordinate2D class from the `coordinate`
    module. However, said class does not present great difference from the
    builtin `tuple` class, so this change should not pose any major
    inconvenience.

Author:
    Paulo Sanchez (@erlete)
"""


from math import sqrt

from coordinate import Coordinate2D


class Circumcenter:
    """Class for triangle calculation.

    This class is used to calculate the circumcenter of a triangle, given its
    three vertices as 2D coordinates.

    Args:
        a (Coordinate2D): First vertex of the triangle.
        b (Coordinate2D): Second vertex of the triangle.
        c (Coordinate2D): Third vertex of the triangle.

    Attributes:
        a (Coordinate2D): First vertex of the triangle.
        b (Coordinate2D): Second vertex of the triangle.
        c (Coordinate2D): Third vertex of the triangle.
        circumcenter (Coordinate2D): The circumcenter of the triangle.
        radius (float): The radius of the circumcircle of the triangle.
    """

    def __init__(self, a: Coordinate2D,
                 b: Coordinate2D, c: Coordinate2D) -> None:

        # Preliminary setting to ensure that all values are set:

        self._a = a
        self._b = b
        self._c = c

        # Value checking before calculation:

        self.a = a
        self.b = b
        self.c = c

    @property
    def a(self) -> Coordinate2D:
        """First vertex of the triangle.

        Returns:
            Coordinate2D: First vertex of the triangle.

        Note:
            If the value of the vertex is changed, the circumcenter and radius
            of the triangle are recalculated.
        """

        return self._a

    @a.setter
    def a(self, value: Coordinate2D) -> None:
        """First vertex of the triangle.

        Args:
            value (Coordinate2D): First vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate2D object.

        Note:
            If the value of the vertex is changed, the circumcenter and radius
            of the triangle are recalculated.
        """

        if not isinstance(value, Coordinate2D):
            raise TypeError("a must be a Coordinate2D instance")

        self._a = value
        self._calculate()

    @property
    def b(self) -> Coordinate2D:
        """Second vertex of the triangle.

        Returns:
            Coordinate2D: Second vertex of the triangle.

        Note:
            If the value of the vertex is changed, the circumcenter and radius
            of the triangle are recalculated.
        """

        return self._b

    @b.setter
    def b(self, value: Coordinate2D) -> None:
        """Second vertex of the triangle.

        Args:
            value (Coordinate2D): Second vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate2D object.

        Note:
            If the value of the vertex is changed, the circumcenter and radius
            of the triangle are recalculated.
        """

        if not isinstance(value, Coordinate2D):
            raise TypeError("b must be a Coordinate2D instance")

        self._b = value
        self._calculate()

    @property
    def c(self) -> Coordinate2D:
        """Third vertex of the triangle.

        Returns:
            Coordinate2D: Third vertex of the triangle.

        Note:
            If the value of the vertex is changed, the circumcenter and radius
            of the triangle are recalculated.
        """

        return self._c

    @c.setter
    def c(self, value: Coordinate2D) -> None:
        """Third vertex of the triangle.

        Args:
            value (Coordinate2D): Third vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate2D object.

        Note:
            If the value of the vertex is changed, the circumcenter and radius
            of the triangle are recalculated.
        """

        if not isinstance(value, Coordinate2D):
            raise TypeError("c must be a Coordinate2D instance")

        self._c = value
        self._calculate()

    @property
    def circumcenter(self) -> Coordinate2D:
        """Circumcenter of the triangle.

        Returns:
            Coordinate2D: The circumcenter of the triangle.
        """

        return self._circumcenter

    @property
    def circumradius(self) -> float:
        """Radius of the circumcircle of the triangle.

        Returns:
            float: The radius of the circumcircle of the triangle.
        """

        return self._circumradius

    def _calculate(self) -> None:
        """Calculates the circumcenter and radius of the triangle."""

        # Segment displacement:

        displacement = {
            "ab": Coordinate2D(
                self.b.x - self.a.x,
                self.b.y - self.a.y
            ),
            "ac": Coordinate2D(
                self.c.x - self.a.x,
                self.c.y - self.a.y
            )
        }

        # Unitary vectors:

        unitary = {
            "ab": Coordinate2D(
                displacement["ab"].y / sqrt(
                    displacement["ab"].x ** 2 + displacement["ab"].y ** 2
                ),
                -displacement["ab"].x / sqrt(
                    displacement["ab"].x ** 2 + displacement["ab"].y ** 2
                )
            ),
            "ac": Coordinate2D(
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
            "ab": Coordinate2D(
                unitary["ab"].x / unitary["ab"].y,
                1
            ),
            "ac": Coordinate2D(
                -(unitary["ac"].x / unitary["ac"].y),
                1
            )
        }

        # Midpoint setting:

        midpoint = {
            "ab": Coordinate2D(
                displacement["ab"].x / 2 + self.a.x,
                displacement["ab"].y / 2 + self.a.y
            ),
            "ac": Coordinate2D(
                displacement["ac"].x / 2 + self.a.x,
                displacement["ac"].y / 2 + self.a.y
            )
        }

        # Midpoint height equivalence:

        intersection = Coordinate2D(
            midpoint["ab"].x + (
                (midpoint["ac"].y - midpoint["ab"].y) / unitary["ab"].y
            ) * unitary["ab"].x,
            midpoint["ac"].y
        )

        # Circumcenter calculation:

        self._circumcenter = Coordinate2D(
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

        self._circumradius = sqrt(
            (self.a.x - self._circumcenter.x) ** 2
            + (self.a.y - self._circumcenter.y) ** 2
        )
