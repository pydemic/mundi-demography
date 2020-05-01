"""
A demography plugin for Mundi.

Expose detailed demographic information about all countries and many sub-regions
of the world.
"""
__author__ = "Fábio Mendes"
__version__ = "0.1.0"
from .functions import population, age_distribution


def enable():
    """
    Enables plugin.
    """
    from mundi.loader import register
    from .functions import loader, age_distribution, age_pyramid, population

    register("population", population)
    register("age_distribution", age_distribution)
    register("age_pyramid", age_pyramid)
