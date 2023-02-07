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

import matplotlib.pyplot as plt


class Coordinate:
    """Real-value, bidimensional coordinate.

    This class represents a two-dimensional coordinate. Its main purpose is to
    serve as a normalized conversion format for data going in and out of the
    scripts contained in the project.

    Args:
        x_value (float): The x value of the coordinate.
        y_value (float): The y value of the coordinate.
    """

    STYLES = {
        "color": "#396fe3",
        "ms": 10
    }

    def __init__(self, x_value: int | float, y_value: int | float) -> None:
        """Initialize a coordinate instance.

        Args:
            x_value (int | float): the X component of the coordinate.
            y_value (int | float): the Y component of the coordinate.
        """
        self.x: float = float(x_value)
        self.y: float = float(y_value)

    @property
    def x(self) -> float:
        """Get the X component of the coordinate.

        Returns:
            float: the X component of the coordinate.
        """
        return self._x

    @x.setter
    def x(self, value: int | float) -> None:
        """Set the X component of the coordinate.

        Args:
            value (int | float): the X component of the coordinate.

        Raises:
            TypeError: of `value` is not an `int` or `float`.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("x must be an int or float")

        self._x = value

    @property
    def y(self) -> float:
        """Get the Y component of the coordinate.

        Returns:
            float: the Y component of the coordinate.
        """
        return self._y

    @y.setter
    def y(self, value) -> None:
        """Set the X component of the coordinate.

        Args:
            value (int | float): the X component of the coordinate.

        Raises:
            TypeError: of `value` is not an `int` or `float`.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("y must be an int or float")

        self._y = value

    def plot(self, *args, ax=None, annotate=False, **kwargs) -> None:
        """Plots the coordinate.

        Args:
            *args: Arguments to pass to the plot function.
            ax (matplotlib.axes.Axes, optional): The axes to plot on. Defaults
                to None (if None, the current axes will be used).
            annotate (bool, optional): Whether to annotate the coordinate.
            **kwargs: Keyword arguments to pass to the plot
        """

        styles = self.STYLES.copy()
        styles.update(kwargs)
        shape = args[0] if args else '.'
        ax = plt.gca() if ax is None else ax

        if annotate:
            ax.annotate(f"({self._x:.4f}, {self._y:.4f})", (self._x, self._y))

        ax.plot(self._x, self._y, shape, **styles)

    def __add__(self, value) -> Coordinate:
        if isinstance(value, Coordinate):
            return Coordinate(self._x + value.x, self._y + value.y)

        raise TypeError("value must be a Coordinate")

    def __sub__(self, value) -> Coordinate:
        if isinstance(value, Coordinate):
            return Coordinate(self._x - value.x, self._y - value.y)

        raise TypeError("value must be a Coordinate")

    def __mul__(self, value) -> Coordinate:
        if isinstance(value, Coordinate):
            return Coordinate(self._x * value.x, self._y * value.y)

        raise TypeError("value must be a Coordinate")

    def __truediv__(self, value) -> Coordinate:
        if isinstance(value, Coordinate):
            return Coordinate(self._x * value.x, self._y * -value.y)

        raise TypeError("value must be a Coordinate")

    def __floordiv__(self, value) -> Coordinate:
        if isinstance(value, Coordinate):
            temp = floor(self / value)
            return Coordinate(temp.x, temp.y)

        raise TypeError("value must be a Coordinate")

    def __mod__(self, value) -> Coordinate:
        if isinstance(value, Coordinate):
            temp = (self / value - self // value) * value
            return Coordinate(temp.x, temp.y)

        raise TypeError("value must be a Coordinate")

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

    def __eq__(self, value) -> bool:
        if not isinstance(value, Coordinate):
            raise TypeError("value must be a Coordinate")

        return self._x == value.x and self._y == value.y

    def __ne__(self, value) -> bool:
        if not isinstance(value, Coordinate):
            raise TypeError("value must be a Coordinate")

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
            raise IndexError("index must be 0 (x) or 1 (y)")

    def __setitem__(self, index, value) -> None:
        if index == 0:
            self._x = value
        elif index == 1:
            self._y = value
        else:
            raise IndexError("index must be 0 (x) or 1 (y)")

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

        raise AttributeError(f"{name} is not an attribute")

    def __delattr__(self, name) -> None:
        if name == 'x':
            del self._x
        elif name == 'y':
            del self._y

        raise AttributeError(f"{name} is not an attribute")

    def __copy__(self) -> Coordinate:
        return self.__class__(self._x, self._y)
