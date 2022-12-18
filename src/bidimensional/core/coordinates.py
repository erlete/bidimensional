"""Coordinate class container module.

This module contains the Coordinate class, which is used to represent a 2D
coordinate. It is used by all classes in the `bidimensional` package and
presents many similarities to the builtin `tuple` class.

Author:
    Paulo Sanchez (@erlete)
"""


from __future__ import annotations

from math import ceil, floor, trunc
from typing import Generator


class Coordinate:
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

    SEQUENTIAL = (tuple, list, set)

    _ERROR_MSGS = {
        "TypeError1": "value must be a Coordinate.",
        "TypeError2": "value must be a Coordinate type or one of the "
        f"supported sequential types: {SEQUENTIAL}. Sequential types "
        "must have only 2 items."
    }

    def __init__(self, x_value: float, y_value: float) -> None:
        self.x: float = float(x_value)
        self.y: float = float(y_value)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("x must be an int or float")

        self._x = value

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("y must be an int or float")

        self._y = value

    def __add__(self, value) -> Coordinate:
        if isinstance(value, self.SEQUENTIAL) and len(value) == 2:
            value = Coordinate(*value)

        if isinstance(value, Coordinate):
            return Coordinate(self._x + value.x, self._y + value.y)

        raise TypeError(self._ERROR_MSGS.get("TypeError2"))

    def __sub__(self, value) -> Coordinate:
        if isinstance(value, self.SEQUENTIAL) and len(value) == 2:
            value = Coordinate(*value)

        if isinstance(value, Coordinate):
            return Coordinate(self._x - value.x, self._y - value.y)

        raise TypeError(self._ERROR_MSGS.get("TypeError2"))

    def __mul__(self, value) -> Coordinate:
        if isinstance(value, self.SEQUENTIAL) and len(value) == 2:
            value = Coordinate(*value)

        if isinstance(value, Coordinate):
            return Coordinate(self._x * value.x, self._y * value.y)

        raise TypeError(self._ERROR_MSGS.get("TypeError2"))

    def __truediv__(self, value) -> Coordinate:
        if isinstance(value, self.SEQUENTIAL) and len(value) == 2:
            value = Coordinate(*value)

        if isinstance(value, Coordinate):
            return Coordinate(self._x * value.x, self._y * -value.y)

        raise TypeError(self._ERROR_MSGS.get("TypeError2"))

    def __floordiv__(self, value) -> Coordinate:
        if isinstance(value, self.SEQUENTIAL) and len(value) == 2:
            value = Coordinate(*value)

        if isinstance(value, Coordinate):
            temp = floor(self / value)
            return Coordinate(temp.x, temp.y)

        raise TypeError(self._ERROR_MSGS.get("TypeError2"))

    def __mod__(self, value) -> Coordinate:
        if isinstance(value, self.SEQUENTIAL) and len(value) == 2:
            value = Coordinate(*value)

        if isinstance(value, Coordinate):
            temp = (self / value - self // value) * value
            return Coordinate(temp.x, temp.y)

        raise TypeError(self._ERROR_MSGS.get("TypeError2"))

    def __pow__(self, value) -> Coordinate:
        return NotImplemented

    def __neg__(self) -> Coordinate:
        return Coordinate(-self._x, -self._y)

    def __pos__(self) -> Coordinate:
        return Coordinate(+self._x, +self._y)

    def __abs__(self) -> Coordinate:
        return Coordinate(abs(self._x), abs(self._y))

    def __invert__(self) -> Coordinate:
        return Coordinate(~self._x, ~self._y)

    def __round__(self, n: int = 0) -> Coordinate:
        if not isinstance(n, int):
            raise TypeError("n must be an int.")

        return Coordinate(round(self._x, n), round(self._y, n))

    def __floor__(self) -> Coordinate:
        return Coordinate(floor(self._x), floor(self._y))

    def __ceil__(self) -> Coordinate:
        return Coordinate(ceil(self._x), ceil(self._y))

    def __trunc__(self) -> Coordinate:
        return Coordinate(trunc(self._x), trunc(self._y))

    def __lt__(self, value) -> bool:
        if not isinstance(value, Coordinate):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self._x < value.x and self._y < value.y

    def __le__(self, value) -> bool:
        if not isinstance(value, Coordinate):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self._x <= value.x and self._y <= value.y

    def __gt__(self, value) -> bool:
        if not isinstance(value, Coordinate):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self._x > value.x and self._y > value.y

    def __ge__(self, value) -> bool:
        if not isinstance(value, Coordinate):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self._x >= value.x and self._y >= value.y

    def __eq__(self, value) -> bool:
        if not isinstance(value, Coordinate):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self._x == value.x and self._y == value.y

    def __ne__(self, value) -> bool:
        if not isinstance(value, Coordinate):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self._x != value.x or self._y != value.y

    def __str__(self) -> str:
        return f"Coordinate({self._x}, {self._y})"

    def __repr__(self) -> str:
        return f"Coordinate({self._x}, {self._y})"

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    def __bool__(self) -> bool:
        return self._x != 0 or self._y != 0

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index) -> float:
        if index == 0:
            return self._x
        elif index == 1:
            return self._y
        else:
            raise IndexError("index must be 0 or 1")

    def __setitem__(self, index, value) -> None:
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        else:
            raise IndexError("index must be 0 or 1")

    def __iter__(self) -> Generator[float, None, None]:
        yield self._x
        yield self._y

    def __reversed__(self) -> Generator[float, None, None]:
        yield self._y
        yield self._x

    def __getattr__(self, name) -> float:
        if name == 'x':
            return self._x
        elif name == 'y':
            return self._y
        else:
            raise AttributeError(f"{name} is not an attribute")

    def __delattr__(self, name) -> None:
        if name == 'x':
            del self._x
        elif name == 'y':
            del self._y
        else:
            raise AttributeError(f"{name} is not an attribute")

    def __getstate__(self) -> tuple[float, float]:
        return self._x, self._y

    def __setstate__(self, state) -> None:
        self._x, self._y = state

    def __reduce__(self) -> tuple[Coordinate, tuple[float, float]]:
        return self.__class__, (self._x, self._y)

    def __copy__(self) -> Coordinate:
        return self.__class__(self._x, self._y)

    def __bytes__(self) -> bytes:
        return bytes(self._x) + bytes(self._y)

    def __int__(self) -> int:
        return int(self._x) + int(self._y)

    def __float__(self) -> float:
        return float(self._x) + float(self._y)

    def __complex__(self) -> complex:
        return complex(self._x) + complex(self._y)

    def __oct__(self) -> str:
        return oct(self._x) + oct(self._y)

    def __hex__(self) -> str:
        return hex(self._x) + hex(self._y)

    def __index__(self) -> float:
        return self._x + self._y

    def __coerce__(self, value) -> tuple[float, float]:
        if not isinstance(value, Coordinate):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        return self._x, value.x


class Line:
    """A class to represent a line in 2D space.

    This class provides a way to represent a line in 2D space. It must be
    composed by two Coordinate objects.

    Args:
        a (Coordinate): The first coordinate.
        b (Coordinate): The second coordinate.

    Attributes:
        a (Coordinate): The first coordinate.
        b (Coordinate): The second coordinate.
        slope (float): The slope of the line.
    """

    def __init__(self, a: Coordinate, b: Coordinate) -> None:
        self._properties = {}

        self.a = a
        self.b = b

    @property
    def a(self) -> Coordinate:
        return self._a

    @a.setter
    def a(self, value) -> None:
        if not isinstance(value, Coordinate):
            raise TypeError("value must be a Coordinate object.")

        self._a = value
        self._properties.clear()

    @property
    def b(self) -> Coordinate:
        return self._b

    @b.setter
    def b(self, value) -> None:
        if not isinstance(value, Coordinate):
            raise TypeError("value must be a Coordinate object.")

        self._b = value
        self._properties.clear()

    @property
    def slope(self) -> float:
        if self._properties.get("slope") is None:
            self._properties["slope"] = (
                (self.b.y - self.a.y)
                / (self.b.x - self.a.x)
            )

        return self._properties["slope"]

    def intersect(self, line: Line) -> Coordinate | None:
        """Determines the intersection between two lines.

        Args:
            line (Line): the line to determine the intersection with.

        Raises:
            TypeError: if line is not a Line object.

        Returns:
            Coordinate | None: the intersection between the two lines (if it
                exists, otherwise None).
        """

        if not isinstance(line, Line):
            raise TypeError(f"Expected Line, got {type(line)}")

        if self.slope == line.slope:
            return None

        x = (line.b.y - self.b.y + self.slope * self.b.x - line.slope * line.b.x) / (self.slope - line.slope)
        y = self.slope * (x - self.b.x) + self.b.y

        return Coordinate(x, y)

    def __mul__(self, line: Line) -> Coordinate | None:
        return self.intersect(line)

    def __eq__(self, value) -> bool:
        if not isinstance(value, Line):
            raise TypeError("value must be a Line object.")

        return self.a == value.a and self.b == value.b

    def __ne__(self, value) -> bool:
        if not isinstance(value, Line):
            raise TypeError("value must be a Line object.")

        return self.a != value.a or self.b != value.b

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    def __getitem__(self, index) -> Coordinate:
        if index == 0:
            return self.a
        elif index == 1:
            return self.b
        else:
            raise IndexError("index must be 0 or 1")

    def __setitem__(self, index, value) -> None:
        if index == 0:
            self.a = value
        elif index == 1:
            self.b = value
        else:
            raise IndexError("index must be 0 or 1")

    def __iter__(self) -> Generator[Coordinate, None, None]:
        yield self.a
        yield self.b

    def __reversed__(self) -> Generator[Coordinate, None, None]:
        yield self.b
        yield self.a

    def __getattr__(self, name) -> Coordinate:
        if name == 'a':
            return self.a
        elif name == 'b':
            return self.b
        else:
            raise AttributeError(f"{name} is not an attribute")

    def __delattr__(self, name) -> None:
        if name == 'a':
            del self.a
        elif name == 'b':
            del self.b
        else:
            raise AttributeError(f"{name} is not an attribute")

    def __str__(self) -> str:
        return f"Line({self.a}, {self.b})"

    def __repr__(self) -> str:
        return f"Line({self.a}, {self.b})"

    def __len__(self) -> int:
        return 2
