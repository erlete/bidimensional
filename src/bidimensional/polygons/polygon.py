"""Container module for the Polygon class.

Author:
    Paulo Sanchez (@erlete)
"""

from __future__ import annotations

from itertools import combinations_with_replacement as cr
from math import ceil, log
from string import ascii_lowercase, ascii_uppercase

import matplotlib
import matplotlib.pyplot as plt

from ..core import operations as op
from ..core.coordinates import Coordinate
from ..core.lines import Segment


class Polygon:
    """Generic polygon class.

    This class represents a generic polygon in the bidimensional plane. It is
    composed of a set of vertices, which are instances of the Coordinate class.

    Attributes:
        ANNOTATIONS (dict[str, str]): annotations for the vertices and sides of
            the polygon.
        vertices (dict[str, Coordinate]): vertices of the polygon.
        sides (dict[str, Segment]): sides of the polygon.
        area (float): area of the polygon.
        perimeter (float): perimeter of the polygon.
    """

    ANNOTATIONS: dict[str, str] = {
        "vertices": ascii_uppercase,
        "sides": ascii_lowercase
    }

    def __init__(self, *vertices: Coordinate):
        """Initialize a polygon instance.

        Args:
            *vertices (Coordinate): vertices of the polygon.

        Notes:
            Duplicate vertices are removed from the list of vertices upon
            polygon instantiation.
        """
        vertices = [  # type: ignore
            vertex for i, vertex in enumerate(vertices)
            if vertex not in vertices[:i]
        ]
        self.vertices = vertices  # type: ignore
        self.sides = [  # type: ignore
            Segment(vertices[i], vertices[i + 1])
            for i in range(len(vertices) - 1)
        ] + [Segment(vertices[-1], vertices[0])]

    @property
    def vertices(self) -> dict[str, Coordinate]:
        """Get the vertices of the polygon.

        Returns:
            dict[str, Coordinate]: vertices of the polygon.
        """
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: tuple[Coordinate]) -> None:
        """Set the vertices of the polygon.

        Args:
            vertices (tuple[Coordinate]): vertices of the polygon.

        Raises:
            TypeError: if any of the vertices is not of type Coordinate.
            ValueError: if the number of vertices is less than 3.
        """
        if len(vertices) < 3:
            raise ValueError("a polygon must have at least 3 vertices")

        if any(not isinstance(vertex, Coordinate) for vertex in vertices):
            raise TypeError("all vertices must be of type Coordinate")

        characters = self.ANNOTATIONS["vertices"]
        padding = ceil(log(len(vertices), len(characters)))

        annotations = [
            ''.join(letters)
            for letters in sorted(
                set(
                    list(cr(characters, padding))
                    + list(cr(reversed(characters), padding))
                )
            )
        ]

        self._vertices = {
            annotation: vertex
            for annotation, vertex in zip(annotations, vertices)
        }

    @property
    def sides(self) -> dict[str, Segment]:
        """Get the sides of the polygon.

        Returns:
            dict[str, Segment]: sides of the polygon.
        """
        return self._sides

    @sides.setter
    def sides(self, sides: tuple[Segment]) -> None:
        """Set the sides of the polygon.

        Args:
            sides (tuple[Segment]): sides of the polygon.

        Raises:
            TypeError: if any of the sides is not of type Segment.
        """
        if any(not isinstance(vertex, Segment) for vertex in sides):
            raise TypeError("all sides must be of type Segment")

        characters = self.ANNOTATIONS["sides"]
        padding = ceil(log(len(sides), len(characters)))

        annotations = [
            ''.join(letters)
            for letters in sorted(
                set(
                    list(cr(characters, padding))
                    + list(cr(reversed(characters), padding))
                )
            )
        ]

        self._sides = {
            annotation: side
            for annotation, side in zip(annotations, sides)
        }

    @property
    def area(self) -> float:
        """Get the area of the polygon.

        Returns:
            float: area of the polygon.
        """
        return op.area(*self.vertices.values())

    @property
    def perimeter(self) -> float:
        """Get the perimeter of the polygon.

        Returns:
            float: perimeter of the polygon.
        """
        return sum(side.distance for side in self.sides.values())

    def plot(self, ax: matplotlib.axes.Axes = None,
             annotate: bool = True, **kwargs) -> None:
        """Plot the polygon.

        Args:
            ax (matplotlib.axes.Axes, optional): axes to plot on. Defaults to
                None.
            annotate (bool, optional): whether to annotate the vertices.
                Defaults to True.
            **kwargs: keyword arguments for `matplotlib.pyplot.plot`.
        """
        if ax is None:
            ax = plt.gca()

        for label, vertex in self._vertices.items():
            vertex.plot(ax=ax)
            if annotate:
                ax.annotate(label, vertex, fontsize=10, fontweight="bold")

        for label, side in self._sides.items():
            side.plot(ax=ax)
            if annotate:
                ax.annotate(label, op.midpoint(*side), fontsize=10)

    def __repr__(self) -> str:
        """Get the raw representation of the polygon.

        Returns:
            str: raw representation of the polygon.
        """
        return f"Polygon({len(self.vertices)} vertices)"

    def __str__(self) -> str:
        """Get the string representation of the polygon.

        Returns:
            str: string representation of the polygon.
        """
        return (
            "Polygon(\n    "
            + ",\n    ".join(map(str, self.vertices.values()))
            + "\n)"
        )

    def __eq__(self, other: object) -> bool:
        """Determine if the polygon is equal to another object.

        Args:
            other (object): object to compare to.

        Returns:
            bool: if the polygon is equal to the other object.
        """
        if not isinstance(other, Polygon):
            return False

        return set(self.vertices.values()) == set(other.vertices.values())

    def __ne__(self, other: object) -> bool:
        """Determine if the polygon is not equal to another object.

        Args:
            other (object): object to compare to.

        Returns:
            bool: if the polygon is not equal to the other object.
        """
        return not self == other

    def __gt__(self, other: object) -> bool:
        """Determine if the polygon is greater than another object.

        Args:
            other (object): object to compare to.

        Returns:
            bool: if the polygon is greater than the other object.
        """
        if not isinstance(other, Polygon):
            return False

        return self.area > other.area

    def __ge__(self, other: object) -> bool:
        """Determine if the polygon is greater than or equal to another object.

        Args:
            other (object): object to compare to.

        Returns:
            bool: if the polygon is greater than or equal to the other object.
        """
        if not isinstance(other, Polygon):
            return False

        return self.area >= other.area

    def __lt__(self, other: object) -> bool:
        """Determine if the polygon is less than another object.

        Args:
            other (object): object to compare to.

        Returns:
            bool: if the polygon is less than the other object.
        """
        if not isinstance(other, Polygon):
            return False

        return self.area < other.area

    def __le__(self, other: object) -> bool:
        """Determine if the polygon is less than or equal to another object.

        Args:
            other (object): object to compare to.

        Returns:
            bool: if the polygon is less than or equal to the other object.
        """
        if not isinstance(other, Polygon):
            return False

        return self.area <= other.area

    def __bool__(self) -> bool:
        """Determine the boolean state of the polygon.

        Returns:
            bool: the boolean state of the polygon.
        """
        return bool(self.vertices)

    def __len__(self) -> int:
        """Get the number of vertices of the polygon.

        Returns:
            int: number of vertices of the polygon.
        """
        return len(self.vertices)

    def __hash__(self) -> int:
        """Get the hash of the polygon.

        Returns:
            int: hash of the polygon.
        """
        return hash(set(self.vertices.values()))
