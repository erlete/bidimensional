"""Notes regarding `bidimensional.core` package imports.

All modules from the `bidimensional.core` subpackage must be available for
direct import through the `from bidimensional import MODULE` syntax. However,
contents of said modules may or may not be available for direct import,
depending on their individual importance. Import statements for said components
must be defined on the root-level `__init__.py` script.
"""
