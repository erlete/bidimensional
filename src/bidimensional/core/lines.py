from __future__ import annotations

from typing import Generator

import matplotlib.pyplot as plt

from . import operations as op
from .coordinates import Coordinate


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

    STYLES = {
        "color": "#7d4e11",
        "lw": 1.25,
        "alpha": .3,
        "linestyle": (5, (10, 3))
    }

    _ERROR_MSGS = {
        "TypeError1": "value must be a Coordinate object.",
        "TypeError2": "value must be a Line object."
    }

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
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        self._a = value
        self._properties.clear()

    @property
    def b(self) -> Coordinate:
        return self._b

    @b.setter
    def b(self, value) -> None:
        if not isinstance(value, Coordinate):
            raise TypeError(self._ERROR_MSGS.get("TypeError1"))

        self._b = value
        self._properties.clear()

    @property
    def slope(self) -> float:
        if self._properties.get("slope") is None:

            if self.b.x - self.a.x == 0:
                print("Warning: slope has an infinite value.")

                self._properties["slope"] = (
                    (self.b.y - self.a.y)
                    / 1e-14
                )

            else:
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

        x = (
            line.b.y - self.b.y + self.slope
            * self.b.x - line.slope * line.b.x
        ) / (self.slope - line.slope)
        y = self.slope * (x - self.b.x) + self.b.y

        return Coordinate(x, y)

    def plot(self, ax=None, **kwargs) -> None:
        """Plots the line.

        Args:
            ax (matplotlib.axes.Axes, optional): The axes to plot on. Defaults
                to None (if None, the current axes will be used).
            **kwargs: Keyword arguments to pass to the plot
        """

        styles = self.STYLES.copy()
        styles.update(kwargs)
        ax = plt.gca() if ax is None else ax

        ax.axline(self.a, self.b, **styles)

    def __mul__(self, line: Line) -> Coordinate | None:
        return self.intersect(line)

    def __eq__(self, value) -> bool:
        if not isinstance(value, Line):
            raise TypeError(self._ERROR_MSGS.get("TypeError2"))

        return self.a == value.a and self.b == value.b

    def __ne__(self, value) -> bool:
        if not isinstance(value, Line):
            raise TypeError(self._ERROR_MSGS.get("TypeError2"))

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


class Segment(Line):
    """A class to represent a segment in 2D space.

    This class provides a way to represent a segment in 2D space. It must be
    composed by two Coordinate objects.

    Args:
        a (Coordinate): The first coordinate.
        b (Coordinate): The second coordinate.

    Attributes:
        a (Coordinate): The first coordinate.
        b (Coordinate): The second coordinate.
        slope (float): The slope of the segment.
    """

    STYLES = {
        "color": "#396fe3",
        "lw": 1.5,
        "alpha": .9
    }

    def __init__(self, a: Coordinate, b: Coordinate) -> None:
        super().__init__(a, b)

    @property
    def x(self) -> float:
        """Returns the x difference between the two coordinates.

        Returns:
            float: The x difference between the two coordinates.
        """

        return self.b.x - self.a.x

    @property
    def y(self) -> float:
        """Returns the y difference between the two coordinates.

        Returns:
            float: The y difference between the two coordinates.
        """

        return self.b.y - self.a.y

    @property
    def distance(self) -> float:
        if self._properties.get("distance") is None:
            self._properties["distance"] = op.distance(self._a, self._b)

        return self._properties["distance"]

    def intersect(self, line: Line) -> Coordinate | None:
        """Determines the intersection between two segments.

        Args:
            line (Line): the line to determine the intersection with.

        Raises:
            TypeError: if line is not a Line object.

        Returns:
            Coordinate | None: the intersection between the two segments (if it
                exists, otherwise None).
        """

        if not isinstance(line, Line):
            raise TypeError(f"Expected Line, got {type(line)}")

        intersection = super().intersect(line)
        if intersection is None:
            return None

        if (
            self.a.x <= intersection.x <= self.b.x
            or self.b.x <= intersection.x <= self.a.x
        ) and (
            self.a.y <= intersection.y <= self.b.y
            or self.b.y <= intersection.y <= self.a.y
        ) and (
            line.a.x <= intersection.x <= line.b.x
            or line.b.x <= intersection.x <= line.a.x
        ) and (
            line.a.y <= intersection.y <= line.b.y
            or line.b.y <= intersection.y <= line.a.y
        ):
            return intersection

        return None

    def plot(self, *args, ax=None, **kwargs) -> None:
        """Plots the segment.

        Args:
            *args: Arguments to pass to the plot function.
            ax (matplotlib.axes.Axes, optional): The axes to plot on. Defaults
                to None (if None, the current axes will be used).
            **kwargs: Keyword arguments to pass to the plot
        """

        styles = self.STYLES.copy()
        styles.update(kwargs)
        shape = args[0] if args else '-'
        ax = plt.gca() if ax is None else ax

        ax.plot(
            (self._a.x, self._b.x), (self._a.y, self._b.y),
            shape, **styles
        )

    def __eq__(self, value) -> bool:
        if not isinstance(value, Segment):
            raise TypeError("value must be a Segment object.")

        return self.a in (value.a, value.b) and self.b in (value.a, value.b)

    def __hash__(self) -> int:
        return hash(hash(self.a) + hash(self.b))

    def __str__(self) -> str:
        return f"Segment({self.a}, {self.b})"

    def __repr__(self) -> str:
        return f"Segment({self.a}, {self.b})"
