import os
from pathlib import Path

import pandas as pd

from mundi.prepare import Loader


class DataLoader(Loader):
    DATABASES = Path(__file__).parent.parent.absolute() / "databases"
    KEY = property(lambda self: self.kind)

    def __init__(self, kind, path=None, target=None):
        super().__init__(path, target)
        self.kind = kind

    def load(self) -> pd.DataFrame:
        tmp = self.find_path("data") / "tmp"
        files = sorted([x for x in os.listdir(tmp) if x.startswith(self.kind)])
        frames = [pd.read_pickle(tmp / f) for f in files]
        df = pd.concat(frames).sort_index()
        self.log(f"Finish loading {self.kind} ({len(files)} files)")
        return df

    def load_cached(self):
        return self.load()


# Distributions
age_distribution_loader = DataLoader("age-distribution")
age_pyramid_loader = DataLoader("age-pyramid")
population_loader = DataLoader("population")

# Yearly data
yearly_age_distribution_loader = DataLoader("yearly-age-distribution")
yearly_age_pyramid_loader = DataLoader("yearly-age-pyramid")
yearly_population_loader = DataLoader("yearly-population")

if __name__ == "__main__":
    print(population_loader.load())
