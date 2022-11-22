"""Container module for the Circumcenter class.

This module contains the Circumcenter class, which is used to calculate the
circumcenter of a triangle, given its three vertices as 2D coordinates.

Author:
    Paulo Sánchez (@erlete)
"""


from math import sqrt

from coordinate import Coordinate2D


class Circumcenter:
    """Class for calculating the circumcenter of a triangle.

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

    def __init__(self, a, b, c) -> None:

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
    def radius(self) -> float:
        """Radius of the circumcircle of the triangle.

        Returns:
            float: The radius of the circumcircle of the triangle.
        """

        return self._radius

    def _calculate(self) -> None:
        """Calculates the circumcenter and radius of the triangle."""

        # Segment displacement:

        ab_displacement = Coordinate2D(
            self.b.x - self.a.x,
            self.b.y - self.a.y
        )

        ac_displacement = Coordinate2D(
            self.c.x - self.a.x,
            self.c.y - self.a.y
        )

        # Unitary vectors:

        ab_root = sqrt(ab_displacement.x ** 2 + ab_displacement.y ** 2)
        ac_root = sqrt(ac_displacement.x ** 2 + ac_displacement.y ** 2)

        ab_unitary = Coordinate2D(
            ab_displacement.y / ab_root,
            -ab_displacement.x / ab_root
        )

        ac_unitary = Coordinate2D(
            ac_displacement.y / ac_root,
            -ac_displacement.x / ac_root
        )

        # Mathematical trick that prevents vertical coordinate alignment:

        ab_unitary.y = ab_unitary.y if ab_unitary.y else 1e-5
        ac_unitary.y = ac_unitary.y if ac_unitary.y else 1e-5

        # V-vector for vertical intersection:

        ab_vertical = Coordinate2D(
            ab_unitary.x / ab_unitary.y,
            1
        )

        ac_vertical = Coordinate2D(
            -(ac_unitary.x / ac_unitary.y),
            1
        )

        # Midpoint setting:

        ab_midpoint = Coordinate2D(
            ab_displacement.x / 2 + self.a.x,
            ab_displacement.y / 2 + self.a.y
        )

        ac_midpoint = Coordinate2D(
            ac_displacement.x / 2 + self.a.x,
            ac_displacement.y / 2 + self.a.y
        )

        # Midpoint height equivalence:

        ab_equal = Coordinate2D(
            ab_midpoint.x + (
                (ac_midpoint[1] - ab_midpoint[1]) / ab_unitary[1]
            ) * ab_unitary.x,
            ac_midpoint.y
        )

        # Circumcenter calculation:

        circumcenter = Coordinate2D(
            ab_equal.x + (
                (ac_midpoint.x - ab_equal.x) / (ab_vertical.x + ac_vertical.x)
            ) * ab_vertical.x,
            ab_equal.y + (
                ac_midpoint.x - ab_equal.x
            ) / (
                ab_vertical.x + ac_vertical.x
            )
        )

        # Circumradius calculation:

        radius = sqrt(
            (self.a.x - circumcenter.x) ** 2
            + (self.a.y - circumcenter.y) ** 2
        )

        self._circumcenter = circumcenter
        self._radius = radius
