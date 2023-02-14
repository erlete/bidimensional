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

from bidimensional import Coordinate, Segment
from bidimensional import operations as op


class Polygon:
    """Generic polygon class.

    This class represents a generic polygon in the bidimensional plane. It is
    composed of a set of vertices, which are instances of the Coordinate class.

    Attributes:
        ANNOTATIONS (dict[str, str]): annotations for the vertices and sides of
            the polygon.
        vertices (dict[str, Coordinate]): vertices of the polygon.
    """

    ANNOTATIONS: dict[str, str] = {
        "vertices": ascii_uppercase,
        "sides": ascii_lowercase
    }

    def __init__(self, *vertices: Coordinate):
        """Initialize a polygon instance.

        Args:
            *vertices (Coordinate): vertices of the polygon.
        """
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
        """
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
