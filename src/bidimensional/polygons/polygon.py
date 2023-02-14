"""Container module for the Polygon class.

Author:
    Paulo Sanchez (@erlete)
"""

from __future__ import annotations

from itertools import combinations_with_replacement as cr
from math import ceil
from string import ascii_lowercase, ascii_uppercase

import matplotlib
import matplotlib.pyplot as plt

from bidimensional import Coordinate


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

    def _get_annotations(self, vertices: tuple[Coordinate]) -> list[str]:
        """Compute the annotations for the vertices.

        Args:
            vertices (tuple[Coordinate]): vertices of the polygon.

        Returns:
            list[str]: annotations for the vertices.
        """
        annotations = self.ANNOTATIONS["vertices"]
        padding = ceil(len(vertices) / len(annotations))

        return [
            ''.join(letters)
            for letters in sorted(
                set(
                    list(cr(annotations, padding))
                    + list(cr(reversed(annotations), padding))
                )
            )
        ]

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

        self._vertices = {
            annotation: coordinate
            for annotation, coordinate in zip(
                self._get_annotations(vertices),
                vertices
            )
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

        x = [vertex.x for vertex in self._vertices.values()]
        y = [vertex.y for vertex in self._vertices.values()]

        ax.plot(
            x + [x[0]],
            y + [y[0]],
            **kwargs
        )

        for label, vertex in self._vertices.items():
            vertex.plot(ax=ax)
            if annotate:
                ax.annotate(label, vertex, fontsize=12, fontweight="bold")
