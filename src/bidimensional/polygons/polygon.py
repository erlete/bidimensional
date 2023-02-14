from __future__ import annotations

from itertools import combinations_with_replacement as cr
from math import ceil
from string import ascii_lowercase, ascii_uppercase

import matplotlib.pyplot as plt

from bidimensional import Coordinate


class Polygon:

    ANNOTATIONS = {
        "vertices": ascii_uppercase,
        "sides": ascii_lowercase
    }

    def __init__(self, *vertices: Coordinate):
        self.vertices = vertices

    def _get_annotations(self, vertices: tuple[Coordinate]) -> list[str]:
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
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: tuple[Coordinate]) -> None:
        self._vertices = {
            annotation: coordinate
            for annotation, coordinate in zip(
                self._get_annotations(vertices),
                vertices
            )
        }

    def plot(self):
        x = [vertex.x for vertex in self._vertices.values()]
        y = [vertex.y for vertex in self._vertices.values()]

        plt.plot(x, y, 'k-')

        for label, vertex in self._vertices.items():
            print(f"{label = }   {vertex = }")
            plt.plot(*vertex, 'ro')
            plt.annotate(label, vertex)
