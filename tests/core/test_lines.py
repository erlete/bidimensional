from bidimensional.core.coordinate import Coordinate
from bidimensional.core.lines import Line, Segment


class TestLine:

    COORDS = (
        Coordinate(0, 0),
        Coordinate(1, 1),
        Coordinate(-1, -1),
        Coordinate(-2, 0)
    )

    def test_instance(self):
        Line(self.COORDS[0], self.COORDS[1])

    def test_access(self):
        line = Line(self.COORDS[0], self.COORDS[1])

        assert line[0] == line.a == self.COORDS[0]
        assert line[1] == line.b == self.COORDS[1]

    def test_eq(self):
        assert Line(self.COORDS[0], self.COORDS[1]) == Line(
            self.COORDS[0], self.COORDS[1])
        assert Line(self.COORDS[0], self.COORDS[1]) == Line(
            self.COORDS[1], self.COORDS[0])

    def test_ne(self):
        assert Line(self.COORDS[0], self.COORDS[1]) != Line(
            self.COORDS[0], self.COORDS[2])

    def test_intersection(self):
        line_1 = Line(self.COORDS[0], self.COORDS[1])
        line_2 = Line(self.COORDS[2], self.COORDS[3])

        assert line_1 * line_2 == line_1.intersect(line_2) == self.COORDS[2]


class TestSegment:

    COORDS = (
        Coordinate(0, 0),
        Coordinate(1, 1),
        Coordinate(-1, 1)
    )

    def test_instance(self):
        Segment(self.COORDS[0], self.COORDS[1])

    def test_access(self):
        segment = Segment(self.COORDS[0], self.COORDS[1])

        assert segment[0] == segment.a == self.COORDS[0]
        assert segment[1] == segment.b == self.COORDS[1]

    def test_eq(self):
        assert Segment(self.COORDS[0], self.COORDS[1]) == Segment(
            self.COORDS[0], self.COORDS[1])
        assert Segment(self.COORDS[0], self.COORDS[1]) == Segment(
            self.COORDS[1], self.COORDS[0])

    def test_ne(self):
        assert Segment(self.COORDS[0], self.COORDS[1]) != Segment(
            self.COORDS[0], self.COORDS[2])

    def test_intersection(self):
        segment_1 = Segment(self.COORDS[0], self.COORDS[1])
        segment_2 = Segment(self.COORDS[0], self.COORDS[2])

        assert segment_1 * \
            segment_2 == segment_1.intersect(segment_2) == self.COORDS[0]
