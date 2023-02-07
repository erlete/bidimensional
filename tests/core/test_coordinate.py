from bidimensional import Coordinate


class TestCoordinate:

    SAMPLE = (1, 2)

    def test_instance(self):
        Coordinate(0, 0)
        Coordinate(0.0, 0)
        Coordinate(0, 0.0)
        Coordinate(0.0, 0.0)
        Coordinate(*self.SAMPLE)

    def test_access(self):
        coord = Coordinate(*self.SAMPLE)

        assert coord[0] == coord.x == self.SAMPLE[0]
        assert coord[1] == coord.y == self.SAMPLE[1]

    def test_eq(self):
        c1 = Coordinate(0, 0)
        c2 = Coordinate(0, 0)

        assert c1 == c2

    def test_ne(self):
        c1 = Coordinate(0, 0.00001)
        c2 = Coordinate(0, 0)

        assert c1 != c2
