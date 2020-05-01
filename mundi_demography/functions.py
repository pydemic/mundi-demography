import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Union

import pandas as pd

ModRef = Union[str, ModuleType]


def age_pyramid(df):
    return loader("mundi_demography", "age-pyramid", df)


def age_distribution(df):
    df = loader("mundi_demography", "age-distribution", df)
    cols = (("age_distribution", x) for x in df.columns)
    df.columns = pd.MultiIndex.from_tuples(cols)
    return df


def population(df):
    return loader("mundi_demography", "population", df)


def loader(package: ModRef, db_name, idx):
    """Load distribution from package"""

    db = database(package, "db-" + db_name + ".pkl.gz")

    if isinstance(idx, (pd.DataFrame, pd.Series)):
        idx = idx.index

    # Try to get from index
    return db.reindex(idx)


@lru_cache(32)
def database(package, name):
    """Lazily load db from name"""

    if isinstance(package, str):
        package = sys.modules[package]
    path = Path(package.__file__).parent.absolute()
    db_path = path / "databases" / name
    return pd.read_pickle(db_path)
