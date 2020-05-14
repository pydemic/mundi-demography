================
Mundi Demography
================

Mundi demography plugin. Exposes demographic information about all countries in the world
and a few functions to transform age distributions and other demographic parameters.

Usage
=====

Install it using ``pip install mundi-demography`` or your method of choice. Now, you can just import
it and load the desired information. Mundi exposes collections of entries as dataframes,
which can be manipulated as usual

>>> import mundi, mundi_demography
>>> db = mundi.countries()
>>> db.mundi["population"]  # DOCTEST: +ELLIPSIS
    population
id
AD         NaN
AE   9892000.0
AF  38927000.0
AG     99000.0
AI         NaN
...

>>> db.mundi["age_distribution"]  # DOCTEST: +ELLIPSIS
          0          5          10   ...     90      95   100
id                                   ...
AD        NaN        NaN        NaN  ...     NaN     NaN  NaN
AE   499000.0   513000.0   453000.0  ...  1000.0     0.0  0.0
AF  5673000.0  5416000.0  5192000.0  ...  5000.0  1000.0  0.0
AG     7000.0     7000.0     7000.0  ...     0.0     0.0  0.0
AI        NaN        NaN        NaN  ...     NaN     NaN  NaN
...
