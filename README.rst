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
...

>>> db.mundi["age_distribution"]  # DOCTEST: +ELLIPSIS
...
