from math import ceil, floor, trunc

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

    def test_add(self):
        assert Coordinate(0, 0) + Coordinate(0, 0) == Coordinate(0, 0)
        assert Coordinate(1, 1) + Coordinate(1, 1) == Coordinate(2, 2)
        assert Coordinate(-1, -1) + Coordinate(-1, -1) == Coordinate(-2, -2)
        assert Coordinate(1, 1) + Coordinate(-1, -1) == Coordinate(0, 0)

        assert (
            Coordinate(0.0, 0.0) + Coordinate(0.0, 0.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1.0, 1.0) + Coordinate(1.0, 1.0)
            == Coordinate(2.0, 2.0)
        )
        assert (
            Coordinate(-1.0, -1.0) + Coordinate(-1.0, -1.0)
            == Coordinate(-2.0, -2.0)
        )
        assert (
            Coordinate(1.0, 1.0) + Coordinate(-1.0, -1.0)
            == Coordinate(0.0, 0.0)
        )

        assert Coordinate(0, 0) + Coordinate(0.0, 0.0) == Coordinate(0.0, 0.0)
        assert Coordinate(1, 1) + Coordinate(1.0, 1.0) == Coordinate(2.0, 2.0)
        assert (
            Coordinate(-1, -1) + Coordinate(-1.0, -1.0)
            == Coordinate(-2.0, -2.0)
        )
        assert (
            Coordinate(1, 1) + Coordinate(-1.0, -1.0)
            == Coordinate(0.0, 0.0)
        )
        
    def test_sub(self):
        assert Coordinate(0, 0) - Coordinate(0, 0) == Coordinate(0, 0)
        assert Coordinate(1, 1) - Coordinate(1, 1) == Coordinate(0, 0)
        assert Coordinate(-1, -1) - Coordinate(-1, -1) == Coordinate(0, 0)
        assert Coordinate(1, 1) - Coordinate(-1, -1) == Coordinate(2, 2)

        assert (
            Coordinate(0.0, 0.0) - Coordinate(0.0, 0.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1.0, 1.0) - Coordinate(1.0, 1.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(-1.0, -1.0) - Coordinate(-1.0, -1.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1.0, 1.0) - Coordinate(-1.0, -1.0)
            == Coordinate(2.0, 2.0)
        )

        assert Coordinate(0, 0) - Coordinate(0.0, 0.0) == Coordinate(0.0, 0.0)
        assert Coordinate(1, 1) - Coordinate(1.0, 1.0) == Coordinate(0.0, 0.0)
        assert (
            Coordinate(-1, -1) - Coordinate(-1.0, -1.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1, 1) - Coordinate(-1.0, -1.0)
            == Coordinate(2.0, 2.0)
        )

    def test_mul(self):
        assert Coordinate(0, 0) * Coordinate(0, 0) == Coordinate(0, 0)
        assert Coordinate(1, 1) * Coordinate(1, 1) == Coordinate(1, 1)
        assert Coordinate(-1, -1) * Coordinate(-1, -1) == Coordinate(1, 1)
        assert Coordinate(1, 1) * Coordinate(-1, -1) == Coordinate(-1, -1)

        assert (
            Coordinate(0.0, 0.0) * Coordinate(0.0, 0.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1.0, 1.0) * Coordinate(1.0, 1.0)
            == Coordinate(1.0, 1.0)
        )
        assert (
            Coordinate(-1.0, -1.0) * Coordinate(-1.0, -1.0)
            == Coordinate(1.0, 1.0)
        )
        assert (
            Coordinate(1.0, 1.0) * Coordinate(-1.0, -1.0)
            == Coordinate(-1.0, -1.0)
        )

        assert Coordinate(0, 0) * Coordinate(0.0, 0.0) == Coordinate(0.0, 0.0)
        assert Coordinate(1, 1) * Coordinate(1.0, 1.0) == Coordinate(1.0, 1.0)
        assert (
            Coordinate(-1, -1) * Coordinate(-1.0, -1.0)
            == Coordinate(1.0, 1.0)
        )
        assert (
            Coordinate(1, 1) * Coordinate(-1.0, -1.0)
            == Coordinate(-1.0, -1.0)
        )

    def test_div(self):
        assert Coordinate(0, 0) / Coordinate(0, 0) == Coordinate(0, 0)
        assert Coordinate(1, 1) / Coordinate(1, 1) == Coordinate(1, -1)
        assert Coordinate(-1, -1) / Coordinate(-1, -1) == Coordinate(1, -1)
        assert Coordinate(1, 1) / Coordinate(-1, -1) == Coordinate(-1, 1)

        assert (
            Coordinate(0.0, 0.0) / Coordinate(0.0, 0.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1.0, 1.0) / Coordinate(1.0, 1.0)
            == Coordinate(1.0, -1.0)
        )
        assert (
            Coordinate(-1.0, -1.0) / Coordinate(-1.0, -1.0)
            == Coordinate(1.0, -1.0)
        )
        assert (
            Coordinate(1.0, 1.0) / Coordinate(-1.0, -1.0)
            == Coordinate(-1.0, 1.0)
        )

        assert Coordinate(0, 0) / Coordinate(0.0, 0.0) == Coordinate(0.0, 0.0)
        assert Coordinate(1, 1) / Coordinate(1.0, 1.0) == Coordinate(1.0, -1.0)
        assert (
            Coordinate(-1, -1) / Coordinate(-1.0, -1.0)
            == Coordinate(1.0, -1.0)
        )
        assert (
            Coordinate(1, 1) / Coordinate(-1.0, -1.0)
            == Coordinate(-1.0, 1.0)
        )

    def test_floor_div(self):
        assert Coordinate(0, 0) // Coordinate(0, 0) == Coordinate(0, 0)
        assert Coordinate(1, 1) // Coordinate(1, 1) == Coordinate(1, -1)
        assert Coordinate(-1, -1) // Coordinate(-1, -1) == Coordinate(1, -1)
        assert Coordinate(1, 1) // Coordinate(-1, -1) == Coordinate(-1, 1)

        assert (
            Coordinate(0.0, 0.0) // Coordinate(0.0, 0.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1.0, 1.0) // Coordinate(1.0, 1.0)
            == Coordinate(1.0, -1.0)
        )
        assert (
            Coordinate(-1.0, -1.0) // Coordinate(-1.0, -1.0)
            == Coordinate(1.0, -1.0)
        )
        assert (
            Coordinate(1.0, 1.0) // Coordinate(-1.0, -1.0)
            == Coordinate(-1.0, 1.0)
        )

        assert Coordinate(0, 0) // Coordinate(0.0, 0.0) == Coordinate(0.0, 0.0)
        assert (
            Coordinate(1, 1) // Coordinate(1.0, 1.0)
            == Coordinate(1.0, -1.0)
        )
        assert (
            Coordinate(-1, -1) // Coordinate(-1.0, -1.0)
            == Coordinate(1.0, -1.0)
        )
        assert (
            Coordinate(1, 1) // Coordinate(-1.0, -1.0)
            == Coordinate(-1.0, 1.0)
        )

    def test_mod(self):
        assert Coordinate(0, 0) % Coordinate(0, 0) == Coordinate(0, 0)
        assert Coordinate(1, 1) % Coordinate(1, 1) == Coordinate(0, 0)
        assert Coordinate(-1, -1) % Coordinate(-1, -1) == Coordinate(0, 0)
        assert Coordinate(1, 1) % Coordinate(-1, -1) == Coordinate(0, 0)

        assert Coordinate(0.0, 0.0) % Coordinate(
            0.0, 0.0) == Coordinate(0.0, 0.0)
        assert Coordinate(1.0, 1.0) % Coordinate(
            1.0, 1.0) == Coordinate(0.0, 0.0)
        assert (
            Coordinate(-1.0, -1.0) % Coordinate(-1.0, -1.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1.0, 1.0) % Coordinate(-1.0, -1.0)
            == Coordinate(0.0, 0.0)
        )

        assert Coordinate(0, 0) % Coordinate(0.0, 0.0) == Coordinate(0.0, 0.0)
        assert Coordinate(1, 1) % Coordinate(1.0, 1.0) == Coordinate(0.0, 0.0)
        assert (
            Coordinate(-1, -1) % Coordinate(-1.0, -1.0)
            == Coordinate(0.0, 0.0)
        )
        assert (
            Coordinate(1, 1) % Coordinate(-1.0, -1.0)
            == Coordinate(0.0, 0.0)
        )

    def test_abs(self):
        assert abs(Coordinate(0, 0)) == Coordinate(0, 0)
        assert abs(Coordinate(1, 1)) == Coordinate(1, 1)
        assert abs(Coordinate(-1, -1)) == Coordinate(1, 1)
        assert abs(Coordinate(1, -1)) == Coordinate(1, 1)
        assert abs(Coordinate(-1, 1)) == Coordinate(1, 1)

        assert abs(Coordinate(1.0, 1.0)) == Coordinate(1.0, 1.0)
        assert abs(Coordinate(-1.0, -1.0)) == Coordinate(1.0, 1.0)
        assert abs(Coordinate(1.0, -1.0)) == Coordinate(1.0, 1.0)
        assert abs(Coordinate(-1.0, 1.0)) == Coordinate(1.0, 1.0)
        assert abs(Coordinate(0.0, 0.0)) == Coordinate(0.0, 0.0)
        assert abs(Coordinate(1.0, 0.0)) == Coordinate(1.0, 0.0)
        assert abs(Coordinate(0.0, 1.0)) == Coordinate(0.0, 1.0)
        assert abs(Coordinate(-1.0, 0.0)) == Coordinate(1.0, 0.0)
        assert abs(Coordinate(0.0, -1.0)) == Coordinate(0.0, 1.0)

    def test_eq(self):
        assert Coordinate(0, 0) == Coordinate(0, 0)
        assert Coordinate(0.0, 0) == Coordinate(0, 0)
        assert Coordinate(0, 0.0) == Coordinate(0, 0)
        assert Coordinate(0.0, 0.0) == Coordinate(0, 0)

    def test_ne(self):
        assert Coordinate(0, 0) != Coordinate(1, 0)
        assert Coordinate(0, 0) != Coordinate(0, 1)
        assert Coordinate(0, 0) != Coordinate(1, 1)

        assert Coordinate(0, 0) != Coordinate(1, 0.0)
        assert Coordinate(0, 0) != Coordinate(0, 1.0)
        assert Coordinate(0, 0) != Coordinate(1, 1.0)
        assert Coordinate(0, 0) != Coordinate(1.0, 0)
        assert Coordinate(0, 0) != Coordinate(0.0, 1)
        assert Coordinate(0, 0) != Coordinate(1.0, 1)
        assert Coordinate(0, 0) != Coordinate(1.0, 0.0)
        assert Coordinate(0, 0) != Coordinate(0.0, 1.0)
        assert Coordinate(0, 0) != Coordinate(1.0, 1.0)

    def test_neg(self):
        assert -Coordinate(0, 0) == Coordinate(0, 0)
        assert -Coordinate(1, 1) == Coordinate(-1, -1)
        assert -Coordinate(-1, -1) == Coordinate(1, 1)
        assert -Coordinate(1, -1) == Coordinate(-1, 1)
        assert -Coordinate(-1, 1) == Coordinate(1, -1)

    def test_floor(self):
        assert floor(Coordinate(0, 0)) == Coordinate(0, 0)
        assert floor(Coordinate(1, 1)) == Coordinate(1, 1)
        assert floor(Coordinate(-1, -1)) == Coordinate(-1, -1)
        assert floor(Coordinate(1, -1)) == Coordinate(1, -1)
        assert floor(Coordinate(-1, 1)) == Coordinate(-1, 1)
        assert floor(Coordinate(0.0, 0.0)) == Coordinate(0, 0)
        assert floor(Coordinate(1.0, 1.0)) == Coordinate(1, 1)
        assert floor(Coordinate(-1.0, -1.0)) == Coordinate(-1, -1)
        assert floor(Coordinate(1.0, -1.0)) == Coordinate(1, -1)
        assert floor(Coordinate(-1.0, 1.0)) == Coordinate(-1, 1)
        assert floor(Coordinate(0.5, 0.5)) == Coordinate(0, 0)
        assert floor(Coordinate(1.5, 1.5)) == Coordinate(1, 1)
        assert floor(Coordinate(-1.5, -1.5)) == Coordinate(-2, -2)
        assert floor(Coordinate(1.5, -1.5)) == Coordinate(1, -2)
        assert floor(Coordinate(-1.5, 1.5)) == Coordinate(-2, 1)
        assert floor(Coordinate(0.9, 0.9)) == Coordinate(0, 0)
        assert floor(Coordinate(1.9, 1.9)) == Coordinate(1, 1)
        assert floor(Coordinate(-1.9, -1.9)) == Coordinate(-2, -2)
        assert floor(Coordinate(1.9, -1.9)) == Coordinate(1, -2)
        assert floor(Coordinate(-1.9, 1.9)) == Coordinate(-2, 1)
        assert floor(Coordinate(0.1, 0.1)) == Coordinate(0, 0)
        assert floor(Coordinate(1.1, 1.1)) == Coordinate(1, 1)
        assert floor(Coordinate(-1.1, -1.1)) == Coordinate(-2, -2)
        assert floor(Coordinate(1.1, -1.1)) == Coordinate(1, -2)
        assert floor(Coordinate(-1.1, 1.1)) == Coordinate(-2, 1)
        assert floor(Coordinate(0.1, 0.9)) == Coordinate(0, 0)
        assert floor(Coordinate(1.1, 1.9)) == Coordinate(1, 1)
        assert floor(Coordinate(-1.1, -1.9)) == Coordinate(-2, -2)
        assert floor(Coordinate(1.1, -1.9)) == Coordinate(1, -2)
        assert floor(Coordinate(-1.1, 1.9)) == Coordinate(-2, 1)

    def test_ceil(self):
        assert ceil(Coordinate(0, 0)) == Coordinate(0, 0)
        assert ceil(Coordinate(1, 1)) == Coordinate(1, 1)
        assert ceil(Coordinate(-1, -1)) == Coordinate(-1, -1)
        assert ceil(Coordinate(1, -1)) == Coordinate(1, -1)
        assert ceil(Coordinate(-1, 1)) == Coordinate(-1, 1)
        assert ceil(Coordinate(0.0, 0.0)) == Coordinate(0, 0)
        assert ceil(Coordinate(1.0, 1.0)) == Coordinate(1, 1)
        assert ceil(Coordinate(-1.0, -1.0)) == Coordinate(-1, -1)
        assert ceil(Coordinate(1.0, -1.0)) == Coordinate(1, -1)
        assert ceil(Coordinate(-1.0, 1.0)) == Coordinate(-1, 1)
        assert ceil(Coordinate(0.5, 0.5)) == Coordinate(1, 1)
        assert ceil(Coordinate(1.5, 1.5)) == Coordinate(2, 2)
        assert ceil(Coordinate(-1.5, -1.5)) == Coordinate(-1, -1)
        assert ceil(Coordinate(1.5, -1.5)) == Coordinate(2, -1)
        assert ceil(Coordinate(-1.5, 1.5)) == Coordinate(-1, 2)
        assert ceil(Coordinate(0.9, 0.9)) == Coordinate(1, 1)
        assert ceil(Coordinate(1.9, 1.9)) == Coordinate(2, 2)
        assert ceil(Coordinate(-1.9, -1.9)) == Coordinate(-1, -1)
        assert ceil(Coordinate(1.9, -1.9)) == Coordinate(2, -1)
        assert ceil(Coordinate(-1.9, 1.9)) == Coordinate(-1, 2)
        assert ceil(Coordinate(0.1, 0.1)) == Coordinate(1, 1)
        assert ceil(Coordinate(1.1, 1.1)) == Coordinate(2, 2)
        assert ceil(Coordinate(-1.1, -1.1)) == Coordinate(-1, -1)
        assert ceil(Coordinate(1.1, -1.1)) == Coordinate(2, -1)
        assert ceil(Coordinate(-1.1, 1.1)) == Coordinate(-1, 2)
        assert ceil(Coordinate(0.1, 0.9)) == Coordinate(1, 1)
        assert ceil(Coordinate(1.1, 1.9)) == Coordinate(2, 2)
        assert ceil(Coordinate(-1.1, -1.9)) == Coordinate(-1, -1)
        assert ceil(Coordinate(1.1, -1.9)) == Coordinate(2, -1)
        assert ceil(Coordinate(-1.1, 1.9)) == Coordinate(-1, 2)

    def test_trunc(self):
        assert trunc(Coordinate(0, 0)) == Coordinate(0, 0)
        assert trunc(Coordinate(1, 1)) == Coordinate(1, 1)
        assert trunc(Coordinate(-1, -1)) == Coordinate(-1, -1)
        assert trunc(Coordinate(1, -1)) == Coordinate(1, -1)
        assert trunc(Coordinate(-1, 1)) == Coordinate(-1, 1)
        assert trunc(Coordinate(0.0, 0.0)) == Coordinate(0, 0)
        assert trunc(Coordinate(1.0, 1.0)) == Coordinate(1, 1)
        assert trunc(Coordinate(-1.0, -1.0)) == Coordinate(-1, -1)
        assert trunc(Coordinate(1.0, -1.0)) == Coordinate(1, -1)
        assert trunc(Coordinate(-1.0, 1.0)) == Coordinate(-1, 1)
        assert trunc(Coordinate(0.5, 0.5)) == Coordinate(0, 0)
        assert trunc(Coordinate(1.5, 1.5)) == Coordinate(1, 1)
        assert trunc(Coordinate(-1.5, -1.5)) == Coordinate(-1, -1)
        assert trunc(Coordinate(1.5, -1.5)) == Coordinate(1, -1)
        assert trunc(Coordinate(-1.5, 1.5)) == Coordinate(-1, 1)
        assert trunc(Coordinate(0.9, 0.9)) == Coordinate(0, 0)
        assert trunc(Coordinate(1.9, 1.9)) == Coordinate(1, 1)
        assert trunc(Coordinate(-1.9, -1.9)) == Coordinate(-1, -1)
        assert trunc(Coordinate(1.9, -1.9)) == Coordinate(1, -1)
        assert trunc(Coordinate(-1.9, 1.9)) == Coordinate(-1, 1)
        assert trunc(Coordinate(0.1, 0.1)) == Coordinate(0, 0)
        assert trunc(Coordinate(1.1, 1.1)) == Coordinate(1, 1)
        assert trunc(Coordinate(-1.1, -1.1)) == Coordinate(-1, -1)
        assert trunc(Coordinate(1.1, -1.1)) == Coordinate(1, -1)
        assert trunc(Coordinate(-1.1, 1.1)) == Coordinate(-1, 1)
        assert trunc(Coordinate(0.1, 0.9)) == Coordinate(0, 0)
        assert trunc(Coordinate(1.1, 1.9)) == Coordinate(1, 1)
        assert trunc(Coordinate(-1.1, -1.9)) == Coordinate(-1, -1)
        assert trunc(Coordinate(1.1, -1.9)) == Coordinate(1, -1)
        assert trunc(Coordinate(-1.1, 1.9)) == Coordinate(-1, 1)

    def test_round(self):
        assert round(Coordinate(0, 0)) == Coordinate(0, 0)
        assert round(Coordinate(1, 1)) == Coordinate(1, 1)
        assert round(Coordinate(-1, -1)) == Coordinate(-1, -1)
        assert round(Coordinate(1, -1)) == Coordinate(1, -1)
        assert round(Coordinate(-1, 1)) == Coordinate(-1, 1)
        assert round(Coordinate(0.0, 0.0)) == Coordinate(0, 0)
        assert round(Coordinate(1.0, 1.0)) == Coordinate(1, 1)
        assert round(Coordinate(-1.0, -1.0)) == Coordinate(-1, -1)
        assert round(Coordinate(1.0, -1.0)) == Coordinate(1, -1)
        assert round(Coordinate(-1.0, 1.0)) == Coordinate(-1, 1)
        assert round(Coordinate(0.5, 0.5)) == Coordinate(0, 0)
        assert round(Coordinate(1.5, 1.5)) == Coordinate(2, 2)
        assert round(Coordinate(-1.5, -1.5)) == Coordinate(-2, -2)
        assert round(Coordinate(1.5, -1.5)) == Coordinate(2, -2)
        assert round(Coordinate(-1.5, 1.5)) == Coordinate(-2, 2)
        assert round(Coordinate(0.9, 0.9)) == Coordinate(1, 1)
        assert round(Coordinate(1.9, 1.9)) == Coordinate(2, 2)
        assert round(Coordinate(-1.9, -1.9)) == Coordinate(-2, -2)
        assert round(Coordinate(1.9, -1.9)) == Coordinate(2, -2)
        assert round(Coordinate(-1.9, 1.9)) == Coordinate(-2, 2)
        assert round(Coordinate(0.1, 0.1)) == Coordinate(0, 0)
        assert round(Coordinate(1.1, 1.1)) == Coordinate(1, 1)
        assert round(Coordinate(-1.1, -1.1)) == Coordinate(-1, -1)
        assert round(Coordinate(1.1, -1.1)) == Coordinate(1, -1)
        assert round(Coordinate(-1.1, 1.1)) == Coordinate(-1, 1)
        assert round(Coordinate(0.1, 0.9)) == Coordinate(0, 1)
        assert round(Coordinate(1.1, 1.9)) == Coordinate(1, 2)
        assert round(Coordinate(-1.1, -1.9)) == Coordinate(-1, -2)
        assert round(Coordinate(1.1, -1.9)) == Coordinate(1, -2)
        assert round(Coordinate(-1.1, 1.9)) == Coordinate(-1, 2)

        assert round(Coordinate(3.1415926, 3.1415926)) == Coordinate(3, 3)
        assert round(Coordinate(3.1415926, 3.1415926), 0) == Coordinate(3, 3)
        assert round(Coordinate(3.1415926, 3.1415926),
                     1) == Coordinate(3.1, 3.1)
        assert round(Coordinate(3.1415926, 3.1415926),
                     2) == Coordinate(3.14, 3.14)
        assert round(Coordinate(3.1415926, 3.1415926),
                     3) == Coordinate(3.142, 3.142)
        assert round(Coordinate(3.1415926, 3.1415926),
                     4) == Coordinate(3.1416, 3.1416)
        assert round(Coordinate(3.1415926, 3.1415926),
                     5) == Coordinate(3.14159, 3.14159)
        assert round(Coordinate(3.1415926, 3.1415926),
                     6) == Coordinate(3.141593, 3.141593)
        assert round(Coordinate(3.1415926, 3.1415926),
                     7) == Coordinate(3.1415926, 3.1415926)
        assert round(Coordinate(3.1415926, 3.1415926),
                     8) == Coordinate(3.1415926, 3.1415926)

    def test_bool(self):
        assert not bool(Coordinate(0, 0))
        assert bool(Coordinate(1, 1))
        assert bool(Coordinate(-1, -1))
        assert bool(Coordinate(1, -1))
        assert bool(Coordinate(-1, 1))
        assert not bool(Coordinate(0.0, 0.0))
        assert bool(Coordinate(1.0, 1.0))
        assert bool(Coordinate(-1.0, -1.0))
        assert bool(Coordinate(1.0, -1.0))
        assert bool(Coordinate(-1.0, 1.0))
        assert bool(Coordinate(0.5, 0.5))
        assert bool(Coordinate(1.5, 1.5))
        assert bool(Coordinate(-1.5, -1.5))
        assert bool(Coordinate(1.5, -1.5))
        assert bool(Coordinate(-1.5, 1.5))
        assert bool(Coordinate(0.9, 0.9))
        assert bool(Coordinate(1.9, 1.9))
        assert bool(Coordinate(-1.9, -1.9))
        assert bool(Coordinate(1.9, -1.9))
        assert bool(Coordinate(-1.9, 1.9))
        assert bool(Coordinate(0.1, 0.1))
        assert bool(Coordinate(1.1, 1.1))
        assert bool(Coordinate(-1.1, -1.1))
        assert bool(Coordinate(1.1, -1.1))
        assert bool(Coordinate(-1.1, 1.1))
        assert bool(Coordinate(0.1, 0.9))
        assert bool(Coordinate(1.1, 1.9))
        assert bool(Coordinate(-1.1, -1.9))
        assert bool(Coordinate(1.1, -1.9))
        assert bool(Coordinate(-1.1, 1.9))
