import pytest

from bidimensional import Coordinate, Segment
from bidimensional.polygons import Polygon


class TestPolygon:

    def test_instance(self):
        with pytest.raises(ValueError):
            # Less than three vertices:
            Polygon()
            Polygon(Coordinate(0, 0))
            Polygon(Coordinate(0, 0), Coordinate(1, 1))
            Polygon(1)
            Polygon(1, 2)

            # Duplicate vertices:
            Polygon(Coordinate(0, 0), Coordinate(0, 0), Coordinate(0, 0))
            Polygon(Coordinate(1, 1), Coordinate(1, 1), Coordinate(0, 0))
            Polygon(Coordinate(0, 0), Coordinate(0, 0),
                    Coordinate(0, 0), Coordinate(0, 0))

        with pytest.raises(TypeError):
            Polygon(Coordinate(0, 0), Coordinate(1, 1), 1)
            Polygon(Coordinate(0, 0), 1, Coordinate(1, 1))
            Polygon(1, Coordinate(0, 0), Coordinate(1, 1))
            Polygon(1, 2, 3)
            Polygon(1, 2, 3, 4)

        Polygon(Coordinate(0, 0), Coordinate(1, 1), Coordinate(1, 0))

    def test_vertices(self):
        polygon = Polygon(Coordinate(0, 0), Coordinate(1, 1), Coordinate(1, 0))
        assert polygon.vertices == {
            "A": Coordinate(0, 0),
            "B": Coordinate(1, 1),
            "C": Coordinate(1, 0)
        }

    def test_sides(self):
        polygon = Polygon(Coordinate(0, 0), Coordinate(1, 1), Coordinate(1, 0))
        assert polygon.sides == {
            "a": Segment(Coordinate(0, 0), Coordinate(1, 1)),
            "b": Segment(Coordinate(1, 1), Coordinate(1, 0)),
            "c": Segment(Coordinate(1, 0), Coordinate(0, 0))
        }

    def test_area(self):
        polygon = Polygon(Coordinate(0, 0), Coordinate(1, 1), Coordinate(1, 0))
        assert polygon.area == 0.5

        polygon = Polygon(Coordinate(0, 0), Coordinate(0, 1),
                          Coordinate(1, 1), Coordinate(1, 0))
        assert polygon.area == 1.0

        polygon = Polygon(Coordinate(0, 0), Coordinate(1, 1),
                          Coordinate(1, 0), Coordinate(0, 1),
                          Coordinate(0.5, 0.5))
        assert polygon.area == .25

    def test_perimeter(self):
        polygon = Polygon(Coordinate(0, 0), Coordinate(1, 1), Coordinate(1, 0))
        assert polygon.perimeter == 3.414213562373095

        polygon = Polygon(Coordinate(0, 0), Coordinate(0, 1),
                          Coordinate(1, 1), Coordinate(1, 0))
        assert polygon.perimeter == 4.0

        polygon = Polygon(Coordinate(0, 0), Coordinate(1, 1),
                          Coordinate(1, 0), Coordinate(0, 1),
                          Coordinate(0.5, 0.5))
        assert polygon.perimeter == 5.242640687119286

    def test_eq(self):
        polygon1 = Polygon(Coordinate(0, 0), Coordinate(1, 1),
                           Coordinate(1, 0))
        polygon2 = Polygon(Coordinate(0, 0), Coordinate(1, 1),
                           Coordinate(1, 0))
        polygon3 = Polygon(Coordinate(0, 0), Coordinate(1, 1),
                           Coordinate(1, 0), Coordinate(0, 1))

        assert polygon1 == polygon2
        assert polygon1 != polygon3
        assert polygon2 != polygon3
