"""Container module for the Coordinate2D class.

Author:
-------
- Paulo Sanchez (@erlete)
"""


from math import ceil, floor, trunc


class Coordinate2D:
    """Represents a pair of real-value, two dimensional coordinates.

    This class represents a two-dimensional coordinate. Its main purpose is to
    serve as a normalized conversion format for data going in and out of the
    scripts contained in the project.

    Parameters:
    -----------
    - x: float
        The x-coordinate.
    - y: float
        The y-coordinate.
    """

    def __init__(self, x_value, y_value):
        self.x = x_value
        self.y = y_value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("x must be a number")
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("y must be a number")
        self._y = value

    def __add__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return Coordinate2D(self.x + value.x, self.y + value.y)

    def __sub__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return Coordinate2D(self.x - value.x, self.y - value.y)

    def __mul__(self, value):

        return Coordinate2D(self.x * value, self.y * value)

    def __truediv__(self, value):

        return Coordinate2D(self.x / value, self.y / value)

    def __floordiv__(self, value):

        return Coordinate2D(self.x // value, self.y // value)

    def __mod__(self, value):

        return Coordinate2D(self.x % value, self.y % value)

    def __pow__(self, value):

        return Coordinate2D(self.x ** value, self.y ** value)

    def __neg__(self):
        return Coordinate2D(-self.x, -self.y)

    def __pos__(self):
        return Coordinate2D(+self.x, +self.y)

    def __abs__(self):
        return Coordinate2D(abs(self.x), abs(self.y))

    def __invert__(self):
        return Coordinate2D(~self.x, ~self.y)

    def __round__(self, n=0):
        return Coordinate2D(round(self.x, n), round(self.y, n))

    def __floor__(self):
        return Coordinate2D(floor(self.x), floor(self.y))

    def __ceil__(self):
        return Coordinate2D(ceil(self.x), ceil(self.y))

    def __trunc__(self):
        return Coordinate2D(trunc(self.x), trunc(self.y))

    def __lt__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return self.x < value.x and self.y < value.y

    def __le__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return self.x <= value.x and self.y <= value.y

    def __gt__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return self.x > value.x and self.y > value.y

    def __ge__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return self.x >= value.x and self.y >= value.y

    def __eq__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return self.x == value.x and self.y == value.y

    def __ne__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return self.x != value.x or self.y != value.y

    def __str__(self):
        return f"Coordinate({self.x}, {self.y})"

    def __repr__(self):
        return f"Coordinate({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("index must be 0 or 1")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("index must be 0 or 1")

    def __iter__(self):
        yield self.x
        yield self.y

    def __reversed__(self):
        yield self.y
        yield self.x

    def __getattr__(self, name):
        if name == "x":
            return self.x
        elif name == "y":
            return self.y
        else:
            raise AttributeError(f"{name} is not an attribute")

    def __delattr__(self, name):
        if name == "x":
            del self.x
        elif name == "y":
            del self.y
        else:
            raise AttributeError(f"{name} is not an attribute")

    def __getstate__(self):
        return self.x, self.y

    def __setstate__(self, state):
        self.x, self.y = state

    def __reduce__(self):
        return self.__class__, (self.x, self.y)

    def __copy__(self):
        return self.__class__(self.x, self.y)

    def __bytes__(self):
        return bytes(self.x) + bytes(self.y)

    def __int__(self):
        return int(self.x) + int(self.y)

    def __float__(self):
        return float(self.x) + float(self.y)

    def __complex__(self):
        return complex(self.x) + complex(self.y)

    def __oct__(self):
        return oct(self.x) + oct(self.y)

    def __hex__(self):
        return hex(self.x) + hex(self.y)

    def __index__(self):
        return self.x + self.y

    def __coerce__(self, value):
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")
        return self.x, value.x

    def __format__(self, format_spec):
        return format(self.x, format_spec) + format(self.y, format_spec)
