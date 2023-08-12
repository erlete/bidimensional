"""Main import handler.

This script contains relevant shortcuts for import statements. There are a few
rules that must be followed for correct import statement handling:

1. All subpackages (such as `core` or `functions`) must be available for direct
    import though the `from bidimensional import SUBPACKAGE` syntax, thus must
    be imported in this script.
2. Some relevant contents of the modules located on the subpackages, or modules
    themselves can also be made available for direct import, though the
    `from bidimensional import MODULE_OR_CONTENT` depending on their importance
    for the package (i.e. `bidimensional.core.coordinate.Coordinate` is
    fundamental for the package, thus should be available for import via
    `from bidimensional import Coordinate`).
"""

from . import core, functions, polygons
from .core import *
from .core.coordinate import Coordinate
from .core.lines import Line, Segment
