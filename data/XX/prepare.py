#
# Data from United Nations, Population Division, Department of Economic and
# Social Affairs
#
# World Population Prospects 2019
#
# File POP/15-1: Annual total population (both sexes combined) by five-year age group,
# region, subregion and country, 1950-2100 (thousands)
# Estimates, 1950 - 2020
# POP/DB/WPP/Rev.2019/POP/F15-1
#
# © August 2019 by United Nations, made available under a Creative Commons license CC
# BY 3.0 IGO: http://creativecommons.org/licenses/by/3.0/igo/
# Suggested citation: United Nations, Department of Economic and Social Affairs,
# Population Division (2019). World Population Prospects 2019, Online Edition. Rev. 1.
#
from pathlib import Path

import pandas as pd

import mundi

PATH = Path(__file__).parent.resolve()

countries = mundi.countries()
code_map = (
    countries.mundi["short_code", "numeric_code"]
    .set_index("numeric_code")["short_code"]
    .to_dict()
)

# Read raw data and transform a few columns
data = pd.read_csv(PATH / "age-distribution.csv.gz").astype({"year": "int32"})
data["code"] = data["code"].apply(lambda x: f"{x:03}")
data["id"] = data["code"].apply(code_map.get)

# Channel Islands is not present in the Mundi database.
# TODO: investigate it. Is Pycountry using an old ISO standard? Is it not
# registered in ISO? Is is just a weird geographical denomination?
removed = set(data[data["id"].isna()]["name"])
print(f"WARNING: removed items {removed}")

# Reorganize data
data = data[data["id"].notna()].drop(columns=["code", "name"]).set_index(["id", "year"])
data = data.applymap(
    lambda x: 1000 * (x if isinstance(x, int) else int(x.replace(" ", "")))
).astype(int)
data.columns = map(int, data)

print("Processing raw data...")

###############################################################################
# Save age distribution
print("- Saving age distribution (not separated by gender)")
data.to_pickle(PATH / "processed" / f"yearly-age-distribution-A1.pkl.gz")

# Save total population
print("- Saving total population projections")
data.sum(1).to_pickle(PATH / "processed" / f"yearly-population-A1.pkl.gz")

# Projections for current year
year = 2020

###############################################################################
# Filtering current year
print("Filtering current year...")
curr = data.reset_index()
curr = curr[curr["year"] == year].drop(columns="year").set_index("id")

# Save data for current year
print("- Saving age distribution")
curr.to_pickle(PATH / "processed" / f"age-distribution-A1.pkl.gz")

print("- Saving total populations")
pop = pd.DataFrame({"population": curr.sum(1)})
pop.to_pickle(PATH / "processed" / f"population-A1.pkl.gz")

print("Current year distributions saved!")
