import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Union, Tuple

import pandas as pd

import mundi

ModRef = Union[str, ModuleType]


def age_pyramid(df):
    """
    Return age_pyramid for given region or collection of regions.
    """
    data, is_row = loader("mundi_demography", "age-pyramid", df)
    if is_row:
        data = {"male": data.loc["male"].T, "female": data.loc["female"].T}
        data = pd.DataFrame(data)
    return data


def age_distribution(df):
    """
    Return age_distribution for given region or collection of regions.
    """
    data, is_row = loader("mundi_demography", "age-distribution", df)
    if is_row:
        data.name = "age_distribution"
    return data


def population(df):
    """
    Return population for given region or collection of regions.
    """
    data, is_row = loader("mundi_demography", "population", df)
    return data


def loader(package: ModRef, db_name, idx) -> Tuple[pd.DataFrame, bool]:
    """Load distribution from package.

    Return a tuple of (Data, is_row). The boolean "is_row" tells
    the returned data concerns a collection of items or a single row in the
    database.
    """

    db = database(package, "db-" + db_name + ".pkl.gz")

    if isinstance(idx, (pd.DataFrame, pd.Series)):
        idx = idx.index
    elif isinstance(idx, str):
        idx = mundi.code(idx)
        df, _ = loader(package, db_name, [idx])
        return df.iloc[0], True

    # Try to get from index
    return db.reindex(idx), False


@lru_cache(32)
def database(package, name):
    """Lazily load db from name"""

    if isinstance(package, str):
        package = sys.modules[package]
    path = Path(package.__file__).parent.absolute()
    db_path = path / "databases" / name
    return pd.read_pickle(db_path)
