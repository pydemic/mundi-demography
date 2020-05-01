import pandas as pd
import os
from pathlib import Path

#
# DATA EXTRACTED FROM:
#
# FREIRE, F.H.M.A; GONZAGA, M.R; QUEIROZ, B.L. Projeção populacional municipal
# com estimadores bayesianos, Brasil 2010 - 2030. In: Sawyer, D.O (coord.).
# Seguridade Social Municipais. Projeto Brasil 3 Tempos. Secretaria  Especial
# de Assuntos Estratégicos da Presidência da República (SAE/SG/PR) , United
# Nations Development Programme, Brazil (UNDP) and International Policy Centre
# for Inclusive Growth. Brasília (IPC-IG), 2019
#

suffix = "BR"
TMP = Path(".").absolute().parent / "tmp"
if not TMP.exists():
    os.mkdir(TMP)


def fix_columns(df, name):
    """
    Create multi-index for male/female columns of age distributions
    """
    df.columns = pd.MultiIndex.from_tuples(
        ((name, int(x)) for x in df.columns), names=["gender", "age"]
    )
    return df


# Read raw data and transform a few columns
data = pd.read_csv("age-distribution.csv.gz")
data = data.drop(columns=["name", "state", "total"])
data["id"] = data.pop("code").apply(lambda x: f"BR-{x}")
data["95"] = data["100"] = 0

print("Raw data loaded")

###############################################################################
# Group by municipality and append two columns for male/female distributions
rows = []
groups = data.groupby("id").groups

print(f"Processing municipalities ({len(groups)})")
for i, (k, mask) in enumerate(groups.items(), start=1):
    chunk = data.loc[mask].set_index(["id", "year"])
    mask = chunk.pop("gender") == "m"
    male = fix_columns(chunk[mask], "male")
    female = fix_columns(chunk[~mask], "female")
    row = pd.concat([female, male], axis=1)
    rows.append(row.astype("int32"))
    print(".", flush=True, end="" if i % 100 else f" {i}\n")
print(" finished!", flush=True)

###############################################################################
# TODO: fix sub-regions

# Save data for municipalities
print("saving age pyramid")
df = pd.concat(rows).sort_index()
df.to_pickle(TMP / f"yearly-age-pyramid-{suffix}.pkl.gz")

# Save age distribution
print("saving age distribution (not separated by gender)")
(df["male"] + df["female"]).to_pickle(TMP / f"yearly-age-distribution-{suffix}.pkl.gz")

# Save total population
print("saving total population projections")
df.sum(1).to_pickle(TMP / f"yearly-population-{suffix}.pkl.gz")
print("Files saved")

# Projections for current year
year = 2020

###############################################################################
# Filtering current year
print("Filtering current year...")
curr = df.reset_index()
curr = curr[curr["year"] == year].drop(columns="year").set_index("id")

# Save data for current year
print("Saving age pyramid")
curr.to_pickle(TMP / f"age-pyramid-{suffix}.pkl.gz")

print("Saving age distribution")
(curr["male"] + curr["female"]).to_pickle(TMP / f"age-distribution-{suffix}.pkl.gz")

print("Saving total populations")
curr.sum(1).to_pickle(TMP / f"population-{suffix}.pkl.gz")

print("\nCurrent year distributions saved!")
