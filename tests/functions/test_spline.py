import json
from bidimensional import Coordinate
from bidimensional.functions import Spline
import pytest
import matplotlib.pyplot as plt
import numpy as np


class TestSpline:

    DIGITS = 8

    GEN_PARAMS: dict[str, list[float]] = {
        'x': [-2.5, 0.0, 2.5, 5.0, 7.5, 3.0, -1.0],
        'y': [0.7, -6, 5, 6.5, 0.0, 5.0, -2.0],
        "ds": .1
    }

    COORDINATES = [
        Coordinate(x_, y_)
        for x_, y_ in zip(GEN_PARAMS['x'], GEN_PARAMS['y'])
    ]

    SPLINE = Spline(COORDINATES)

    with open("tests/functions/data/spline.json", mode='r', encoding="utf-8") as f:
        DATA_1 = json.load(f)

    def test_x(self):
        spx = [coord.x for coord in self.SPLINE.positions]

        tested = [round(value, self.DIGITS) for value in spx]
        valid = [round(value, self.DIGITS) for value in self.DATA_1['x']]

        assert tested == valid

    def test_y(self):
        spy = [coord.y for coord in self.SPLINE.positions]

        tested = [round(value, self.DIGITS) for value in spy]
        valid = [round(value, self.DIGITS) for value in self.DATA_1['y']]

        assert tested == valid

    def test_yaw(self):
        tested = [round(value, self.DIGITS) for value in self.SPLINE.yaw]
        valid = [round(value, self.DIGITS) for value in self.DATA_1["yaw"]]

        assert tested == valid

    def no_test_curvature(self):
        tested = [
            round(value, self.DIGITS)
            for value in self.SPLINE.curvature
        ]
        valid = [
            round(value, self.DIGITS)
            for value in self.DATA_1["curvature"]
        ]

        base = np.arange(
            self.SPLINE._knots[0],
            self.SPLINE._knots[-1],
            self.SPLINE._generation_step
        )

        plt.plot(base, tested, "r-", label="Tested")
        plt.plot(base, valid, "g-", label="Valid")
        plt.grid()
        plt.show()
        return

        diff = [abs(t - v) for t, v in zip(tested, valid)]
        assert all(d < 1 for d in diff)
