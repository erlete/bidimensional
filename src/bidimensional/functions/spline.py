"""2D cubic spline generation utilities.

This module contains the classes and functions necessary to generate a cubic
spline from a set of points.

Authors:
    Atsushi Sakai (@Atsushi_twi) (author of the original code)
    Paulo Sanchez (@erlete) (author of the modified code)
"""

import math
from bisect import bisect
from typing import Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np

from ..core.coordinate import Coordinate


class _UnidimensionalSpline:
    """Unidimensional spline computation class (internal).

    This class is used to compute the interpolation of a set of points using
    a cubic spline.
    """

    def __init__(self, x: list[int | float], y: list[int | float]):
        """Initialize a unidimensional spline instance.

        Args:
            x (list[int | float]): list of x-coordinates.
            y (list[int | float]): list of y-coordinates.

        Raises:
            ValueError: if the x and y lists have different lengths.
        """
        self.x = np.array(x)
        self.y = np.array(y)

        if self.x.shape != self.y.shape:
            raise ValueError("x and y must have the same shape")

        # Determine the dimension of the X-axis:
        self._x_dim = self.x.shape[0]

        # Compute the differences between the x-coordinates:
        self._x_diff = np.diff(x)

        # Compute coefficient d:
        self.d = np.array(y)

        # Compute the difference between d coefficients:
        d_diff = np.diff(self.d)

        # Compute coefficient b:
        self.b = np.linalg.solve(
            self.__calc_matrix_a(),
            self.__calc_matrix_b()
        )

        # Compute the difference between b coefficients:
        b_diff = np.diff(self.b)

        # Compute coefficient c:
        self.c = (
            d_diff / self._x_diff
            - self._x_diff * (self.b[1:] + 2.0 * self.b[:-1]) / 3.0
        )

        # Compute coefficient a:
        self.a = b_diff / (3.0 * self._x_diff)

        self.b = self.b[:-1]
        self.d = self.d[:-1]

        self.pos = None

    def position(self, x: int | float) -> Optional[int | float]:
        """Compute the image of a given x-value in a spline section.

        Args:
            x (float): the x-value to compute the image of.

        Returns:
            int | float: the image of the spline section.

        Notes:
            The form of the function is: f(x) = a*x^3 + b*x^2 + c*x + d.
            If x is outside of the X-range, the output is None.
        """
        if not self.x[0] <= x <= self.x[-1]:
            return None

        i = self.__search_index(x)
        dx = x - self.x[i]

        if self.pos is None:
            self.pos = (
                self.a * dx**3.0
                + self.b * dx**2.0
                + self.c * dx
                + self.d
            )

        return (
            self.a[i] * dx**3.0
            + self.b[i] * dx**2.0
            + self.c[i] * dx
            + self.d[i]
        )

    def first_derivative(self, x: int | float) -> Optional[int | float]:
        """Compute the first derivative of an x-value.

        Args:
            x (float): the x-value to compute the first derivative of.

        Returns:
            int | float: the first derivative of the x-value.

        Notes:
            The form of the function is: f'(x) = 3*a*x^2 + 2*b*x + c.
            If x is outside of the X-range, the output is None.
        """
        if not self.x[0] <= x <= self.x[-1]:
            return None

        i = self.__search_index(x)
        dx = x - self.x[i]

        return (
            3.0 * self.a[i] * dx**2.0
            + 2.0 * self.b[i] * dx
            + self.c[i]
        )

    def second_derivative(self, x: int | float) -> Optional[int | float]:
        """Compute the second derivative of an x-value.

        Args:
            x (float): the x-value to compute the second derivative of.

        Returns:
            int | float: the second derivative of the x-value.

        Notes:
            The form of the function is: f''(x) = 6*a*x + 2*b.
            If x is outside of the X-range, the output is None.
        """
        if not self.x[0] <= x <= self.x[-1]:
            return None

        i = self.__search_index(x)
        dx = x - self.x[i]

        return (
            6.0 * self.a[i] * dx
            + 2.0 * self.b[i]
        )

    def __calc_matrix_a(self) -> np.array:
        """Compute the A matrix for the spline coefficient b.

        Args:
            diff (list): list of differences between x-coordinates.

        Returns:
            np.array: the A matrix for the spline coefficient b.
        """
        matrix = np.zeros((self._x_dim, self._x_dim))
        matrix[0, 0] = 1.0

        for i in range(self._x_dim - 1):
            if i != (self._x_dim - 2):
                matrix[i + 1, i + 1] = 2.0 * \
                    (self._x_diff[i] + self._x_diff[i + 1])

            matrix[i + 1, i] = self._x_diff[i]
            matrix[i, i + 1] = self._x_diff[i]

        matrix[0, 1] = 0.0
        matrix[self._x_dim - 1, self._x_dim - 2] = 0.0
        matrix[self._x_dim - 1, self._x_dim - 1] = 1.0

        return matrix

    def __calc_matrix_b(self) -> np.array:
        """Compute the B matrix for the spline coefficient b.

        Args:
            diff (list): list of differences between x-coordinates.

        Returns:
            np.array: the B matrix for the spline coefficient b.
        """
        matrix = np.zeros(self._x_dim)

        for i in range(self._x_dim - 2):
            matrix[i + 1] = (
                3.0 * (self.d[i + 2] - self.d[i + 1]) / self._x_diff[i + 1]
                - 3.0 * (self.d[i + 1] - self.d[i]) / self._x_diff[i]
            )

        return matrix

    def __search_index(self, x: int | float) -> int:
        """Search for the index of the spline that contains the given x-value.

        Args:
            x (float): the x-value to search for.

        Returns:
            int: the index of the spline section that contains the given
        """
        return bisect(self.x, x) - 1


class Spline:
    """2D cubic spline class.

    This class generates a 2D spline from two lists of x and y coordinates.
    Intermediary points are generated with a separation determined by the
    generation step parameter.

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

    def __init__(self, coordinates: Iterable[Coordinate],
                 gen_step: int | float = 0.1) -> None:
        """Initialize a spline instance.

        Args:
            coordinates (Iterable[Coordinate]): collection of coordinates for
                the interpolation process.
            gen_step (int | float, optional): interpolation step. Defaults to
                0.1.
        """
        self._x = [coord.x for coord in coordinates]
        self._y = [coord.y for coord in coordinates]

        if len(self._x) != len(self._y):
            raise ValueError("The number of x and y values must be the same.")

        self._knots = self._compute_knots(self._x, self._y)
        self._spline_x = _UnidimensionalSpline(self._knots, self._x)
        self._spline_y = _UnidimensionalSpline(self._knots, self._y)
        self._generation_step = gen_step
        self._positions, self._curvature, self._yaw = self._compute_results()

    @property
    def x(self) -> list[float]:
        """Return the x coordinates of the spline.

        Returns:
            list: x coordinates of the spline.
        """
        return self._x

    @x.setter
    def x(self, value: list[float]) -> None:
        """Set the x coordinates of the spline.

        Args:
            value (list): x coordinates of the spline.
        """
        if not isinstance(value, (list, tuple, np.ndarray)):
            raise TypeError("x must be a list, tuple or numpy array.")

        elif not all(isinstance(val, (int, float)) for val in value):
            raise TypeError("x must contain only numbers.")

        self._x = value

    @property
    def y(self) -> list[float]:
        """Return the y coordinates of the spline.

        Returns:
            list: y coordinates of the spline.
        """
        return self._y

    @y.setter
    def y(self, value: list[float]) -> None:
        """Set the y coordinates of the spline.

        Args:
            value (list): y coordinates of the spline.
        """
        if not isinstance(value, (list, tuple, np.ndarray)):
            raise TypeError("y must be a list, tuple or numpy array.")

        elif not all(isinstance(val, (int, float)) for val in value):
            raise TypeError("y must contain only numbers.")

        self._y = value

    @property
    def generation_step(self) -> float:
        """Return the generation step of the spline.

        Returns:
            float: generation step of the spline.
        """
        return self._generation_step

    @generation_step.setter
    def generation_step(self, value: float) -> None:
        """Set the generation step of the spline.

        Args:
            value (float): generation step of the spline.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("generation_step must be a number.")

        elif value <= 0:
            raise ValueError("generation_step must be positive.")

        self._generation_step = value

    @property
    def knots(self) -> list[float]:
        """Return the knots of the spline.

        Returns:
            list: knots of the spline.
        """
        return self._knots

    @property
    def positions(self) -> list[tuple[float, float]]:
        """Return the positions of the spline.

        Returns:
            list: positions of the spline.
        """
        return self._positions

    @property
    def curvature(self) -> list[float]:
        """Return the curvature of the spline.

        Returns:
            list: curvature of the spline.
        """
        return self._curvature

    @property
    def yaw(self) -> list[float]:
        """Return the yaw of the spline.

        Returns:
            list: yaw of the spline.
        """
        return self._yaw

    def _compute_knots(self, x, y):
        """Compute the knots of the spline.

        Args:
            x (list): x coordinates.
            y (list): y coordinates.

        Returns:
            list: knots of the spline.
        """
        return np.concatenate((
            np.zeros(1),
            np.cumsum(np.hypot(np.diff(x), np.diff(y)))
        ))

    def _compute_position(self,
                          i: int) -> Optional[tuple[int | float, int | float]]:
        """Compute the image of a given x-value in a spline section.

        Args:
            i (int): index of the spline section.

        Returns:
            tuple | None: image of the x-value in the spline section. If the
                image is outside the generation range, the output is None.
        """
        return self._spline_x.position(i), self._spline_y.position(i)

    def _compute_curvature(self, i: int) -> float:
        """Compute the curvature of a given spline section.

        Args:
            i (int): index of the spline section.

        Returns:
            float | None: curvature of a given spline section. If i is outside
                the generation range, the output is None.
        """
        dx1 = self._spline_x.first_derivative(i)
        dx2 = self._spline_x.second_derivative(i)
        dy1 = self._spline_y.first_derivative(i)
        dy2 = self._spline_y.second_derivative(i)

        return (dy2 * dx1 - dx2 * dy1) / math.sqrt((dx1**2 + dy1**2))

    def _compute_yaw(self, i: int) -> float:
        """Compute the yaw of a given spline section.

        Args:
            i (int): index of the spline section.

        Returns:
            float | None: yaw of a given spline section. If i is outside the
                generation range, the output is None.
        """
        return math.atan2(
            self._spline_y.first_derivative(i),
            self._spline_x.first_derivative(i)
        )

    def _compute_results(self) -> tuple:
        """Compute the coordinates, curvature and yaw of the spline.

        Returns:
            tuple: coordinates, curvature and yaw of the spline.
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
        """Plot the input of the spline.

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
        """Plot the spline."""
        styles = self.STYLES.copy()
        styles.update({"label": "Spline"})
        styles.update(kwargs)
        shape = args[0] if args else self.SHAPES["line"]

        ax = plt.gca() if ax is None else ax
        ax.plot(*zip(*self._positions), shape, **styles)

    def plot_curvature(self, *args, ax=None, **kwargs) -> None:
        """Plot the curvature function of the spline.

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
        """Plot the YAW function of the spline.

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
        """Get the string epresentation of the spline.

        Returns:
            str: string representation of the spline.
        """
        return f"Spline of {len(self._x)} points"

    def __repr__(self) -> str:
        """Raw representation of the spline.

        Returns:
            str: raw representation of the spline.
        """
        return f"Spline of {len(self._x)} points"
