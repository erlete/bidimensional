"""Coordinate2D class container module.

This module contains the Coordinate2D class, which is used to represent a 2D
coordinate. It is used by all classes in the `2d-utils` package and presents
many similarities to the builtin `tuple` class.

Author:
    Paulo Sanchez (@erlete)
"""


from __future__ import annotations

from math import ceil, floor, trunc
from typing import Generator


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

    def __add__(self, value) -> Coordinate2D:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate2D.")

        return Coordinate2D(self._x + value.x, self._y + value.y)

    def __sub__(self, value) -> Coordinate2D:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate2D.")

        return Coordinate2D(self._x - value.x, self._y - value.y)

    def __mul__(self, value) -> Coordinate2D:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate2D.")

        return Coordinate2D(self._x * value, self._y * value)

    def __truediv__(self, value) -> Coordinate2D:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate2D.")

        return Coordinate2D(self._x / value, self._y / value)

    def __floordiv__(self, value) -> Coordinate2D:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate2D.")

        return Coordinate2D(self._x // value, self._y // value)

    def __mod__(self, value) -> Coordinate2D:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate2D.")

        return Coordinate2D(self._x % value, self._y % value)

    def __pow__(self, value) -> Coordinate2D:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate2D.")

        return Coordinate2D(self._x ** value, self._y ** value)

    def __neg__(self) -> Coordinate2D:
        return Coordinate2D(-self._x, -self._y)

    def __pos__(self) -> Coordinate2D:
        return Coordinate2D(+self._x, +self._y)

    def __abs__(self) -> Coordinate2D:
        return Coordinate2D(abs(self._x), abs(self._y))

    def __invert__(self) -> Coordinate2D:
        return Coordinate2D(~self._x, ~self._y)

    def __round__(self, n: int = 0) -> Coordinate2D:
        if not isinstance(n, int):
            raise TypeError("n must be an int.")

        return Coordinate2D(round(self._x, n), round(self._y, n))

    def __floor__(self) -> Coordinate2D:
        return Coordinate2D(floor(self._x), floor(self._y))

    def __ceil__(self) -> Coordinate2D:
        return Coordinate2D(ceil(self._x), ceil(self._y))

    def __trunc__(self) -> Coordinate2D:
        return Coordinate2D(trunc(self._x), trunc(self._y))

    def __lt__(self, value) -> bool:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")

        return self._x < value.x and self._y < value.y

    def __le__(self, value) -> bool:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")

        return self._x <= value.x and self._y <= value.y

    def __gt__(self, value) -> bool:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")

        return self._x > value.x and self._y > value.y

    def __ge__(self, value) -> bool:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")

        return self._x >= value.x and self._y >= value.y

    def __eq__(self, value) -> bool:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")

        return self._x == value.x and self._y == value.y

    def __ne__(self, value) -> bool:
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")

        return self._x != value.x or self._y != value.y

    def __str__(self) -> str:
        return f"Coordinate2D({self._x}, {self._y})"

    def __repr__(self) -> str:
        return f"Coordinate2D({self._x}, {self._y})"

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

    def __reduce__(self) -> tuple[Coordinate2D, tuple[float, float]]:
        return self.__class__, (self._x, self._y)

    def __copy__(self) -> Coordinate2D:
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
        if not isinstance(value, Coordinate2D):
            raise TypeError("value must be a Coordinate.")

        return self._x, value.x

    def __format__(self, format_spec) -> str:
        return format(self._x, format_spec) + format(self._y, format_spec)
