"""
Entry point for package
"""
from type_dep._core import dependencyinjected, Dependency, Context

# Version of the type_dep package
__version__ = "0.0.2"

__all__ = [
    dependencyinjected,
    Dependency,
    Context,
]
