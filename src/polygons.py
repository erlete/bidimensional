from coordinate import Coordinate2D
from circumcenter import Circumcenter


class Triangle:

    def __init__(self, a: Coordinate2D, b: Coordinate2D,
                 c: Coordinate2D) -> None:

        self._initial_setting = False

        self.a = a
        self.b = b
        self.c = c

        self._initial_setting = True

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
            self._circumcircle = Circumcenter(self.a, self.b, self.c)

        return self._circumcircle.circumcenter

    @property
    def circumradius(self) -> float:
        """Circumradius of the triangle.

        Returns:
            float: Circumradius of the triangle.
        """

        if self._circumcircle is None:
            self._circumcircle = Circumcenter(self.a, self.b, self.c)

        return self._circumcircle.circumradius
