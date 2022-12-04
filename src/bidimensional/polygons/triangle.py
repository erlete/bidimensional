from matplotlib import pyplot as plt

import bidimensional.operations as op
from bidimensional.circumcircle import Circumcircle
from bidimensional.coordinates import Coordinate


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

    TOL_DIGITS = 10

    def __init__(self, a: Coordinate, b: Coordinate,
                 c: Coordinate) -> None:

        self._circumcircle = None

        self._initial_setting = False

        self.a = a
        self.b = b
        self.c = c

        self._initial_setting = True
        self._compute_angles()

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

    @property
    def circumcenter(self) -> Coordinate:
        """Circumcenter of the triangle.

        Returns:
            Coordinate: Circumcenter of the triangle.
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

    def is_collinear(self) -> bool:
        """Checks if the triangle is collinear.

        Returns:
            bool: True if the triangle is collinear, False otherwise.
        """

        return not (
            self._a.x * (self._b.y - self._c.y)
            + self._b.x * (self._c.y - self._a.y)
            + self._c.x * (self._a.y - self._b.y)
        )

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

    def __eq__(self, other: object) -> bool:
        """Checks if two triangles are equal.

        Args:
            other (object): Other object.

        Returns:
            bool: True if the triangles are equal, False otherwise.
        """

        if not isinstance(other, Triangle):
            return False

        return (
            self.a == other.a
            and self.b == other.b
            and self.c == other.c
        )

    def __neq__(self, other: object) -> bool:
        """Checks if two triangles are not equal.

        Args:
            other (object): Other object.

        Returns:
            bool: True if the triangles are not equal, False otherwise.
        """

        return not self.__eq__(other)

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
