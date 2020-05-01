import pandas as pd
import os
from pathlib import Path
import mundi

countries = mundi.countries()
code_map = countries[["code", "numeric_code"]].set_index("numeric_code")["code"].to_dict()

#
# United Nations
# Population Division
# Department of Economic and Social Affairs
#
# World Population Prospects 2019
# File POP/15-1: Annual total population (both sexes combined) by five-year age group,
# region, subregion and country, 1950-2100 (thousands)
# Estimates, 1950 - 2020
# POP/DB/WPP/Rev.2019/POP/F15-1
# © August 2019 by United Nations, made available under a Creative Commons license CC
# BY 3.0 IGO: http://creativecommons.org/licenses/by/3.0/igo/
# Suggested citation: United Nations, Department of Economic and Social Affairs,
# Population Division (2019). World Population Prospects 2019, Online Edition. Rev. 1.
#

suffix = "WORLD"
TMP = Path(".").absolute().parent / "tmp"

if not TMP.exists():
    os.mkdir(TMP)

# Read raw data and transform a few columns
data = pd.read_csv("age-distribution.csv.gz").astype({"year": "int32"})
data["code"] = data["code"].apply(lambda x: f"{x:03}")
# data = data.drop(columns=["name", "state", "total"])
data["id"] = data["code"].apply(code_map.get)

# Channel Islands is not present in the Mundi database.
# TODO: investigate it. Is Pycountry using an old ISO standard? Is it not
# registered in ISO? Is is just a weird geographical denomination?
removed = set(data[data["id"].isna()]["name"])
print(f"WARNING: removed items {removed}\n")

# Reorganize data
data = data[data["id"].notna()].drop(columns=["code", "name"]).set_index(["id", "year"])
data = data.applymap(
    lambda x: 1000 * (x if isinstance(x, int) else int(x.replace(" ", "")))
).astype(int)
data.columns = map(int, data)

print("Raw data loaded")

###############################################################################
# TODO: fix sub-regions

# Save age distribution
print("saving age distribution (not separated by gender)")
data.to_pickle(TMP / f"yearly-age-distribution-{suffix}.pkl.gz")

# Save total population
print("saving total population projections")
data.sum(1).to_pickle(TMP / f"yearly-population-{suffix}.pkl.gz")
print("Files saved")

# Projections for current year
year = 2020

###############################################################################
# Filtering current year
print("Filtering current year...")
curr = data.reset_index()
curr = curr[curr["year"] == year].drop(columns="year").set_index("id")

# Save data for current year
print("Saving age distribution")
curr.to_pickle(TMP / f"age-distribution-{suffix}.pkl.gz")

print("Saving total populations")
curr.sum(1).to_pickle(TMP / f"population-{suffix}.pkl.gz")

print("\nCurrent year distributions saved!")
