"""
A demography plugin for Mundi.

Expose detailed demographic information about all countries and many sub-regions
of the world.
"""
__author__ = "Fábio Mendes"
__version__ = "0.1.0"

from .functions import population, age_distribution, age_pyramid

FUNCTIONS = {
    "population": population,
    "age_distribution": age_distribution,
    "age_pyramid": age_pyramid,
}


def register(check_environ=False):
    """
    Enable plugin.

    This is executed automatically
    """
    from mundi.loader import register
    from mundi.types.region import REGION_PLUGINS

    if check_environ:
        import os

        if os.environ.get("MUNDI_DEMOGRAPHY", "on").lower() in ("off", "false", "no"):
            return

    for k, v in FUNCTIONS.items():
        register(k, v)

    REGION_PLUGINS["population"] = lambda x: population(x.id)
    REGION_PLUGINS["age_distribution"] = lambda x: age_distribution(x.id)
    REGION_PLUGINS["age_pyramid"] = lambda x: age_pyramid(x.id)


def unregister():
    """
    Disable plugin.
    """
    from mundi.loader import unregister

    for k, v in FUNCTIONS.items():
        unregister(k, function=v)


register(check_environ=True)
