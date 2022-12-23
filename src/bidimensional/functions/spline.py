"""2D cubic spline generation utilities.

This module contains the classes and functions necessary to generate a cubic
spline from a set of points.

Author:
    Atsushi Sakai (@Atsushi_twi) (author of the original code)
    Paulo Sanchez (@erlete) (author of the modified code)
"""


import bisect
import math

import matplotlib.pyplot as plt
import numpy as np

from ..core.coordinates import Coordinate


class SplineBase:
    """Internal spline computation class.

    Args:
        x (list): List of x-coordinates.
        y (list): List of y-coordinates.

    Notes:
        The number of x and y values must be the same.
        Since the spline is a cubic function composite, each segment is defined
            by a polynomial function of the form
            f(x) = a*x^3 + b*x^2 + c*x + d.
        A property of said polynomial function is that, at x = x_n, f(x) = y_n
            and at x = x_(n + 1), f(x) = y_(n + 1), g(x) = y_(n + 1). This
            means that the images of each pair of segments, given a boundary
            point, are the same.
        Another property is that the second and third derivatives of a given
            spline segment have the same images at the boundary points as well.
    """

    def __init__(self, x, y):
        self.x, self.y = x, y

        # Determine the dimension of the X-axis:
        self.x_dim = len(x)

        # Compute the differences between the x-coordinates:
        x_diff = np.diff(x)

        # Compute coefficient d:
        self.d = np.array(y)

        # Compute the difference between d coefficients:
        d_diff = np.diff(self.d)

        # Compute coefficient b:
        self.b = np.linalg.solve(
            self.__calc_matrix_a(x_diff),
            self.__calc_matrix_b(x_diff)
        )

        # Compute the difference between b coefficients:
        b_diff = np.diff(self.b)

        # Compute coefficient c:
        self.c = np.array([
            (d_diff[i]) / x_diff[i]
            - x_diff[i] * (self.b[i + 1] + 2.0 * self.b[i]) / 3.0
            for i in range(self.x_dim - 1)
        ])

        # Compute coefficient a:
        self.a = [b_diff[i] / (3.0 * x_diff[i]) for i in range(self.x_dim - 1)]

    def position(self, x) -> float | None:
        """Computes the image of a given x-value in a spline section.

        Args:
            x (float): The x-value to compute the image of.

        Returns:
            float: The image of the spline section.

        Notes:
            The form of the function is: f(x) = a*x^3 + b*x^2 + c*x + d.
            If x is outside of the X-range, the output is None.
        """

        # Out of bounds handling:

        if not self.x[0] <= x <= self.x[-1]:
            return None

        i = self.__search_index(x)
        dx = x - self.x[i]

        return (
            self.a[i] * dx**3.0
            + self.b[i] * dx**2.0
            + self.c[i] * dx
            + self.d[i]
        )

    def first_derivative(self, x) -> float | None:
        """Computes the first derivative image

        Args:
            x (float): The x-value to compute the image of.

        Returns:
            float: The image of the first derivative of the spline section.

        Notes:
            The form of the function is: f'(x) = 3*a*x^2 + 2*b*x + c.
            If x is outside of the X-range, the output is None.
        """

        # Out of bounds handling:

        if not self.x[0] <= x <= self.x[-1]:
            return None

        i = self.__search_index(x)
        dx = x - self.x[i]

        return (
            3.0 * self.a[i] * dx**2.0
            + 2.0 * self.b[i] * dx
            + self.c[i]
        )

    def second_derivative(self, x) -> float | None:
        """Computes the first derivative of a given spline section.

        Args:
            x (float): The x-value to compute the image of.

        Returns:
            float: The image of the second derivative of the spline section.

        Notes:
            The form of the function is: f''(x) = 6*a*x + 2*b.
            If x is outside of the X-range, the output is None.
        """

        # Out of bounds handling:

        if not self.x[0] <= x <= self.x[-1]:
            return None

        i = self.__search_index(x)
        dx = x - self.x[i]

        return (
            6.0 * self.a[i] * dx
            + 2.0 * self.b[i]
        )

    def __calc_matrix_a(self, diff):
        """Computes the A matrix for the spline coefficient b.

        Args:
            diff (list): List of differences between x-coordinates.

        Returns:
            np.array: The A matrix for the spline coefficient b.
        """

        matrix = np.zeros((self.x_dim, self.x_dim))
        matrix[0, 0] = 1.0

        for i in range(self.x_dim - 1):
            if i != (self.x_dim - 2):
                matrix[i + 1, i + 1] = 2.0 * (diff[i] + diff[i + 1])

            matrix[i + 1, i] = diff[i]
            matrix[i, i + 1] = diff[i]

        matrix[0, 1] = 0.0
        matrix[self.x_dim - 1, self.x_dim - 2] = 0.0
        matrix[self.x_dim - 1, self.x_dim - 1] = 1.0

        return matrix

    def __calc_matrix_b(self, diff):
        """Computes the B matrix for the spline coefficient b.

        Args:
            diff (list): List of differences between x-coordinates.

        Returns:
            np.array: The B matrix for the spline coefficient b.
        """

        matrix = np.zeros(self.x_dim)

        for i in range(self.x_dim - 2):
            matrix[i + 1] = (
                3.0 * (self.d[i + 2] - self.d[i + 1]) / diff[i + 1]
                - 3.0 * (self.d[i + 1] - self.d[i]) / diff[i]
            )

        return matrix

    def __search_index(self, x):
        """Searches the index of the spline section that contains the given
        x-value.

        Args:
            x (float): The x-value to search for.

        Returns:
            int: The index of the spline section that contains the given
        """

        return bisect.bisect(self.x, x) - 1


class Spline:
    """2D cubic spline class.

    This class generates a 2D spline from two lists of x and y coordinates.
    Intermediary points are generated with a separation determined by the
    generation step parameter.

    Args:
        coordiantes (list): The list of coordinates to generate the spline.
        gen_step (float): The step used to generate the spline.

    Notes:
        The number of x and y values must be the same.
        The value used for the generation step must not be negative not zero.
    """

    SHAPES = {
        "point": 'x',
        "line": '-'
    }

    STYLES = {
        "color": "black",
        "lw": 1.5
    }

    def __init__(self, coordinates, gen_step=.1) -> None:
        self._x = [coord.x for coord in coordinates]
        self._y = [coord.y for coord in coordinates]

        if len(self._x) != len(self._y):
            raise ValueError("The number of x and y values must be the same.")

        self._knots = self._compute_knots(self._x, self._y)
        self._spline_x = SplineBase(self._knots, self._x)
        self._spline_y = SplineBase(self._knots, self._y)
        self._generation_step = gen_step
        self._positions, self._curvature, self._yaw = self._compute_results()

    @property
    def x(self) -> list[float]:
        """Returns the x coordinates of the spline.

        Returns:
            list: List of x coordinates.
        """

        return self._x

    @x.setter
    def x(self, value: list[float]) -> None:
        """Sets the x coordinates of the spline.

        Args:
            value (list): List of x coordinates.
        """

        if not isinstance(value, (list, tuple, np.array)):
            raise TypeError("x must be a list, tuple or numpy array.")

        elif not all(isinstance(val, (int, float)) for val in value):
            raise TypeError("x must contain only numbers.")

        self._x = value

    @property
    def y(self) -> list[float]:
        """Returns the y coordinates of the spline.

        Returns:
            list: List of y coordinates.
        """

        return self._y

    @y.setter
    def y(self, value: list[float]) -> None:
        """Sets the y coordinates of the spline.

        Args:
            value (list): List of y coordinates.
        """

        if not isinstance(value, (list, tuple, np.array)):
            raise TypeError("y must be a list, tuple or numpy array.")

        elif not all(isinstance(val, (int, float)) for val in value):
            raise TypeError("y must contain only numbers.")

        self._y = value

    @property
    def generation_step(self) -> float:
        """Returns the generation step of the spline.

        Returns:
            float: The generation step of the spline.
        """

        return self._generation_step

    @generation_step.setter
    def generation_step(self, value: float) -> None:
        """Sets the generation step of the spline.

        Args:
            value (float): The generation step of the spline.
        """

        if not isinstance(value, (int, float)):
            raise TypeError("generation_step must be a number.")

        elif value <= 0:
            raise ValueError("generation_step must be positive.")

        self._generation_step = value

    @property
    def knots(self) -> list[float]:
        """Returns the knots of the spline.

        Returns:
            list: List of knots.
        """

        return self._knots

    @property
    def positions(self) -> list[tuple[float, float]]:
        """Returns the positions of the spline.

        Returns:
            list: List of positions.
        """

        return self._positions

    @property
    def curvature(self) -> list[float]:
        """Returns the curvature of the spline.

        Returns:
            list: List of curvature.
        """

        return self._curvature

    @property
    def yaw(self) -> list[float]:
        """Returns the yaw of the spline.

        Returns:
            list: List of yaw.
        """

        return self.plot_yaw

    def _compute_knots(self, x, y):
        """Computes the knots of the spline.

        Args:
            x (list): List of x coordinates.
            y (list): List of y coordinates.

        Returns:
            list: List of knots.
        """

        return [0] + list(np.cumsum(np.hypot(np.diff(x), np.diff(y))))

    def _compute_position(self, i):
        """Computes the image of a given x-value in a spline section.

        Args:
            i (int): The index of the spline section.

        Returns:
            tuple: The image of the x-value in the spline section.

        Notes:
            If x is outside of the X-range, the output is None.
        """

        return self._spline_x.position(i), self._spline_y.position(i)

    def _compute_curvature(self, i: int) -> float:
        """Computes the curvature of a given spline section.

        Args:
            i (int): The index of the spline section.

        Returns:
            float: The curvature of the spline section.

        Notes:
            If x is outside of the X-range, the output is None.
        """

        # This dictionary allows fast value checking:
        derivatives = {
            'x1': self._spline_x.first_derivative(i),
            'x2': self._spline_x.second_derivative(i),
            'y1': self._spline_y.first_derivative(i),
            'y2': self._spline_y.second_derivative(i)
        }

        return (
            derivatives["y2"] * derivatives["x1"]
            - derivatives["x2"] * derivatives["y1"]
        ) / ((derivatives["x1"]**2 + derivatives["y1"]**2) ** (3 / 2))

    def _compute_yaw(self, i: int) -> float:
        """Computes the yaw of a given spline section.

        Args:
            i (int): The index of the spline section.

        Returns:
            float: The yaw of the spline section.

        Notes:
            If x is outside of the X-range, the output is None.
        """

        return math.atan2(
            self._spline_y.first_derivative(i),
            self._spline_x.first_derivative(i)
        )

    def _compute_results(self):
        """Computes the coordinates, curvature and yaw of the spline.

        Returns:
            tuple: The coordinates, curvature and yaw of the spline.
        """

        knots_ext = np.arange(
            self._knots[0],
            self._knots[-1],
            self._generation_step
        )

        data = np.array(
            [(
                Coordinate(*self._compute_position(i)),
                self._compute_curvature(i),
                self._compute_yaw(i)
            ) for i in knots_ext],
            dtype=object
        )

        return data[:, 0], data[:, 1], data[:, 2]

    def plot_input(self, *args, ax=None, **kwargs) -> None:
        """Plots the input of the spline.

        Args:
            *args: Arguments to pass to the plot function.
            ax (matplotlib.axes.Axes, optional): The axes to plot on. Defaults
                to None.
            **kwargs: Keyword arguments to pass to the plot
        """

        styles = self.STYLES.copy()
        styles.update({"label": "Input"})
        styles.update(kwargs)
        shape = args[0] if args else self.SHAPES["point"]

        ax = plt.gca() if ax is None else ax
        ax.plot(self._x, self._y, shape, **styles)

    def plot_positions(self, *args, ax=None, **kwargs) -> None:
        """Plots the spline."""

        styles = self.STYLES.copy()
        styles.update({"label": "Spline"})
        styles.update(kwargs)
        shape = args[0] if args else self.SHAPES["line"]

        ax = plt.gca() if ax is None else ax
        ax.plot(*zip(*self._positions), shape, **styles)

    def plot_curvature(self, *args, ax=None, **kwargs) -> None:
        """Plots the curvature function of the spline.

        Args:
            *args: Arguments to pass to the plot function.
            ax (matplotlib.axes.Axes, optional): The axes to plot on. Defaults
                to None.
            **kwargs: Keyword arguments to pass to the plot
        """

        styles = self.STYLES.copy()
        styles.update({"label": "Curvature"})
        styles.update(kwargs)
        shape = args[0] if args else self.SHAPES["line"]

        ax = plt.gca() if ax is None else ax
        ax.plot(
            np.arange(self._knots[0],
                      self._knots[-1],
                      self._generation_step
                      ),
            self._curvature, shape, **styles
        )

    def plot_yaw(self, *args, ax=None, **kwargs) -> None:
        """Plots the YAW function of the spline.

        Args:
            *args: Arguments to pass to the plot function.
            ax (matplotlib.axes.Axes, optional): The axes to plot on. Defaults
                to None.
            **kwargs: Keyword arguments to pass to the plot
        """

        styles = self.STYLES.copy()
        styles.update({"label": "YAW"})
        styles.update(kwargs)
        shape = args[0] if args else self.SHAPES["line"]

        ax = plt.gca() if ax is None else ax
        ax.plot(
            np.arange(self._knots[0],
                      self._knots[-1],
                      self._generation_step
                      ),
            self._yaw, shape, **styles
        )

    def __str__(self) -> str:
        return f"Spline2D of {len(self._x)} points"

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self._x)
