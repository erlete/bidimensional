from matplotlib import pyplot as plt

import bidimensional.operations as op
from bidimensional.circumcircle import Circumcircle
from coordinate import Coordinate2D


class Triangle:
    """Triangle class.

    This class represents a triangle in the 2D plane. It is defined by three
    vertices, a, b and c (Coordinate2D objects). The class provides methods to
    compute the angles of the triangle, the circumcenter and the circumradius.
    It also provides methods used to determine special properties of the
    triangle, such as if it is equilateral, isosceles, scalene, right, obtuse
    or acute.

    Args:
        a (Coordinate2D): First vertex of the triangle.
        b (Coordinate2D): Second vertex of the triangle.
        c (Coordinate2D): Third vertex of the triangle.

    Attributes:
        a (Coordinate2D): First vertex of the triangle.
        b (Coordinate2D): Second vertex of the triangle.
        c (Coordinate2D): Third vertex of the triangle.
        circumcenter (Coordinate2D): Circumcenter of the triangle.
        circumradius (float): Circumradius of the triangle.
    """

    TOL_DIGITS = 10

    def __init__(self, a: Coordinate2D, b: Coordinate2D,
                 c: Coordinate2D) -> None:

        self._circumcircle = None

        self._initial_setting = False

        self.a = a
        self.b = b
        self.c = c

        self._initial_setting = True
        self._compute_angles()

    @property
    def a(self) -> Coordinate2D:
        """First vertex of the triangle.

        Returns:
            Coordinate2D: First vertex of the triangle.
        """

        return self._a

    @a.setter
    def a(self, value: Coordinate2D) -> None:
        """First vertex of the triangle.

        Args:
            value (Coordinate2D): First vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate2D object.
        """

        if not isinstance(value, Coordinate2D):
            raise TypeError("a must be a Coordinate2D instance")

        self._a = value

    @property
    def b(self) -> Coordinate2D:
        """Second vertex of the triangle.

        Returns:
            Coordinate2D: Second vertex of the triangle.
        """

        return self._b

    @b.setter
    def b(self, value: Coordinate2D) -> None:
        """Second vertex of the triangle.

        Args:
            value (Coordinate2D): Second vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate2D object.
        """

        if not isinstance(value, Coordinate2D):
            raise TypeError("b must be a Coordinate2D instance")

        self._b = value

    @property
    def c(self) -> Coordinate2D:
        """Third vertex of the triangle.

        Returns:
            Coordinate2D: Third vertex of the triangle.
        """

        return self._c

    @c.setter
    def c(self, value: Coordinate2D) -> None:
        """Third vertex of the triangle.

        Args:
            value (Coordinate2D): Third vertex of the triangle.

        Raises:
            TypeError: If the value is not a Coordinate2D object.
        """

        if not isinstance(value, Coordinate2D):
            raise TypeError("c must be a Coordinate2D instance")

        self._c = value

    @property
    def circumcenter(self) -> Coordinate2D:
        """Circumcenter of the triangle.

        Returns:
            Coordinate2D: Circumcenter of the triangle.
        """

        if self._circumcircle is None:
            self._circumcircle = Circumcircle(self.a, self.b, self.c)

        return self._circumcircle.center

    @property
    def circumradius(self) -> float:
        """Circumradius of the triangle.

        Returns:
            float: Circumradius of the triangle.
        """

        if self._circumcircle is None:
            self._circumcircle = Circumcircle(self.a, self.b, self.c)

        return self._circumcircle.radius

    def is_right(self) -> bool:
        """Checks if the triangle has a right angle.

        Returns:
            bool: True if the triangle has a right angle, False otherwise.
        """

        return any([
            round(angle_, self.TOL_DIGITS) == 90
            for angle_ in self._angles.values()
        ])

    def is_obtuse(self) -> bool:
        """Checks if the triangle has an obtuse angle.

        Returns:
            bool: True if the triangle has an obtuse angle, False otherwise.
        """

        return any([
            angle_ > 90
            for angle_ in self._angles.values()
        ])

    def is_acute(self) -> bool:
        """Checks if the triangle has an acute angle.

        Returns:
            bool: True if the triangle has an acute angle, False otherwise.
        """

        return all([
            angle_ < 90
            for angle_ in self._angles.values()
        ])

    def is_equilateral(self) -> bool:
        """Checks if the triangle is equilateral.

        Returns:
            bool: True if the triangle is equilateral, False otherwise.
        """

        return len(set(self._angles.values())) == 1

    def is_isosceles(self) -> bool:
        """Checks if the triangle is isosceles.

        Returns:
            bool: True if the triangle is isosceles, False otherwise.
        """

        return len(set(self._angles.values())) == 2

    def is_scalene(self) -> bool:
        """Checks if the triangle is scalene.

        Returns:
            bool: True if the triangle is scalene, False otherwise.
        """

        return len(set(self._angles.values())) == 3

    def _compute_angles(self) -> None:
        """Computes the angles of the triangle.
        """

        if self._initial_setting:
            self._angles = {
                'a': round(op.angle(self.b, self.c, self.a), self.TOL_DIGITS),
                'b': round(op.angle(self.c, self.a, self.b), self.TOL_DIGITS),
                'c': round(op.angle(self.a, self.b, self.c), self.TOL_DIGITS)
            }

    def plot(self, **kwargs) -> None:
        """Plots the triangle.

        Args:
            **kwargs: Keyword arguments for matplotlib.pyplot.plot.
        """

        plt.plot(
            [self.a.x, self.b.x, self.c.x, self.a.x],
            [self.a.y, self.b.y, self.c.y, self.a.y],
            **kwargs
        )
