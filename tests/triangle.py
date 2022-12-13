from ..src.bidimensional.polygons.triangle import Triangle
from ..src.bidimensional.coordinates import Coordinate
from math import sqrt
from itertools import combinations, permutations


class TestTriangle:
    """Triangle tests class.

    This class contains all relevant test cases for the `polygons.triangle`
    module.

    Note:
        Tests contained here are intended to be run with the `pytest` module.
    """

    DEFINITION_TOL = 1e-14

    def test_generation(self) -> None:
        """Triangle generation test.

        This test case checks if the triangle is correctly generated from the
        given coordinates. It also checks if the definition order is correct
        and each vertex is associated with the correct coordinate.
        """

        triangle = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        # Coordinate components' checks:

        assert triangle.a.x == 0 and triangle.a.y == 0
        assert triangle.b.x == 1 and triangle.b.y == 1
        assert triangle.c.x == 1 and triangle.c.y == 0

    def test_definition_order(self) -> None:
        """Triangle definition order test.

        This test case checks if the definition order matters defines unique
        triangle objects. This should not be the case, as the definition order
        should not matter.
        """

        coordinates = (
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        # Generate all possible triangle definitions:

        triangles = [
            Triangle(*triplet)
            for triplet in permutations(coordinates, 3)
        ]

        # Check if all triangles are equal:

        assert all(
            pair[0] == pair[1]
            for pair in combinations(triangles, 2)
        )

    def test_area(self) -> None:
        """Triangle area test.

        This test case checks if the triangle area is correctly calculated.
        """

        triangle = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        assert triangle.area == 0.5

    def test_perimeter(self) -> None:
        """Triangle perimeter test.

        This test case checks if the triangle perimeter is correctly
        calculated.
        """

        triangle = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        assert triangle.perimeter == sqrt(2) + 2

    def test_collinear_1(self) -> None:
        """Vertex collinearity test 1.

        This test case checks if the `is_collinear` method correctly detects
        vertex alignments on three scenarios:
            Vertical alignment (Y axis)
            Horizontal alignment (X axis)
            Diagonal alignment (y = ax + b form)
        """

        coordinates = (
            (  # Vertical alignment:
                Coordinate(0, 0),
                Coordinate(0, 1),
                Coordinate(0, 2)
            ), (  # Horizontal alignment:
                Coordinate(1, 0),
                Coordinate(2, 0),
                Coordinate(3, 0)
            ), (  # Diagonal alignment:
                Coordinate(0, 0),
                Coordinate(1, 1),
                Coordinate(2, 2)
            )
        )

        # Coordinate order mixing:

        for coordinate_set in coordinates:
            for triplet in permutations(coordinate_set, 3):
                triangle = Triangle(*triplet)
                assert triangle.is_collinear()

    def test_collinear_2(self) -> None:
        """Vertex collinearity test 2.

        This test case checks if the `is_collinear` method behaves correctly
        when the vertices of a given set of triangles are not collinear.
        """

        coordinates = (
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(0, 1),
            Coordinate(1, 1)
        )

        for triplet in permutations(coordinates, 3):
            triangle = Triangle(*triplet)
            assert not triangle.is_collinear()

    def test_eq(self) -> None:
        """Triangle equality test.

        This test case checks if the triangle equality operator correctly
        detects equal triangles.
        """

        triangle_1 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        triangle_2 = Triangle(
            Coordinate(1, 1),
            Coordinate(0, 0),
            Coordinate(1, 0)
        )

        assert triangle_1 == triangle_2

    def test_neq(self) -> None:
        """Triangle inequality test.

        This test case checks if the triangle inequality operator correctly
        detects inequal triangles.
        """

        triangle_1 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        triangle_2 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 1)
        )

        assert triangle_1 != triangle_2

    def test_gt(self) -> None:
        """Triangle greater than test.

        This test case checks if the triangle greater than operator correctly
        detects greater triangles.
        """

        triangle_1 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1 + self.DEFINITION_TOL, 0)
        )

        triangle_2 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        assert triangle_1 > triangle_2

    def test_lt(self) -> None:
        """Triangle less than test.

        This test case checks if the triangle less than operator correctly
        detects lesser triangles.
        """

        triangle_1 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        triangle_2 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1 + self.DEFINITION_TOL, 0)
        )

        assert triangle_1 < triangle_2

    def test_ge(self) -> None:
        """Triangle greater than or equal test.

        This test case checks if the triangle greater than or equal operator
        correctly detects greater or equal triangles.
        """

        triangle_1 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1 + self.DEFINITION_TOL, 0)
        )

        triangle_2 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        assert triangle_1 >= triangle_2
        assert triangle_1 >= triangle_1

    def test_le(self) -> None:
        """Triangle less than or equal test.

        This test case checks if the triangle less than or equal operator
        correctly detects lesser or equal triangles.
        """

        triangle_1 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1, 0)
        )

        triangle_2 = Triangle(
            Coordinate(0, 0),
            Coordinate(1, 1),
            Coordinate(1 + self.DEFINITION_TOL, 0)
        )

        assert triangle_1 <= triangle_2
        assert triangle_1 <= triangle_1

    def test_is_right(self) -> None:
        """Triangle right angle test.

        This test case checks if the `is_right` method correctly detects
        right triangles.
        """

        coordinates = (
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(0, 1)
        )

        assert all(
            Triangle(*triplet).is_right() is True
            for triplet in permutations(coordinates, 3)
        )

    def test_is_obtuse(self) -> None:
        """Triangle obtuse angle test.

        This test case checks if the `is_obtuse` method correctly detects
        obtuse triangles.
        """

        coordinates = (
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(2, 2)
        )

        assert all(
            Triangle(*triplet).is_obtuse() is True
            for triplet in permutations(coordinates, 3)
        )

    def test_is_acute(self) -> None:
        """Triangle acute angle test.

        This test case checks if the `is_acute` method correctly detects
        acute triangles.
        """

        coordinates = (
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(0.5, sqrt(1))
        )

        assert all(
            Triangle(*triplet).is_acute() is True
            for triplet in permutations(coordinates, 3)
        )

    def test_is_equilateral(self) -> None:
        """Triangle equilateral test.

        This test case checks if the `is_equilateral` method correctly detects
        equilateral triangles.
        """

        coordinates = (
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(0.5, sqrt(3) / 2)
        )

        assert all(
            Triangle(*triplet).is_equilateral() is True
            for triplet in permutations(coordinates, 3)
        )

    def test_is_isosceles(self) -> None:
        """Triangle isosceles test.

        This test case checks if the `is_isosceles` method correctly detects
        isosceles triangles.
        """

        coordinates = (
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(0.5, 3)
        )

        assert all(
            Triangle(*triplet).is_isosceles() is True
            for triplet in permutations(coordinates, 3)
        )

    def test_is_scalene(self) -> None:
        """Triangle scalene test.

        This test case checks if the `is_scalene` method correctly detects
        scalene triangles.
        """

        coordinates = (
            Coordinate(0, 0),
            Coordinate(1, 0),
            Coordinate(2, 2.543)
        )

        assert all(
            Triangle(*triplet).is_scalene() is True
            for triplet in permutations(coordinates, 3)
        )
