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
from pathlib import Path

import pandas as pd

PATH = Path(__file__).parent.resolve()
DEST = PATH / "processed"


def fix_columns(df, name):
    """
    Create multi-index for male/female columns of age distributions
    """
    df.columns = pd.MultiIndex.from_tuples(
        ((name, int(x)) for x in df.columns), names=["gender", "age"]
    )
    return df


# Read raw data and transform a few columns
data = pd.read_csv(PATH / "age-distribution.csv.gz")
data = data.drop(columns=["name", "state", "total"])
data["id"] = data.pop("code").apply(lambda x: f"BR-{x}")
data["95"] = data["100"] = 0

print("Raw data loaded")


###############################################################################
# Group by municipality and append two columns for male/female distributions


def T(df, gender):
    df = (
        df[df["gender"] == gender]
        .set_index(["id", "year"])
        .drop(columns="gender")
        .sort_index()
        .astype("int32")
    )
    data = ((gender, int(x)) for x in df.columns)
    df.columns = pd.MultiIndex.from_tuples(data, names=["gender", "age"])
    return df


data = data.replace({"f": "female", "m": "male"})
male = T(data, "male")
female = T(data, "female")
data = pd.concat([female, male], axis=1)

# Projections for Brazilian population pyramid. Override UN projections
brazil = (
    data.reset_index()
    .set_index("year")
    .drop(columns="id")
    .groupby("year")
    .sum()
    .reset_index()
)
brazil["id"] = "BR"
data = data.append(brazil.set_index(["id", "year"]))


###############################################################################
# TODO: fix sub-regions

# # Save data for municipalities
print("- Saving age pyramid")
data.to_pickle(DEST / f"yearly-age-pyramid-C1.pkl.gz")

# Save age distribution
print("- Saving age distribution (not separated by gender)")
(data["male"] + data["female"]).to_pickle(DEST / f"yearly-age-distribution-C1.pkl")

# Save total population
print("- Saving total population projections")
data.sum(1).to_pickle(DEST / f"yearly-population-C1.pkl")
print("Files saved")


###############################################################################
# Filtering current year

print("Filtering current year...")
year = 2020
pyramid = data.reset_index()
pyramid = pyramid[pyramid["year"] == year].drop(columns="year").set_index("id")

# Save data for current year
print("Saving age pyramid")
pyramid.to_pickle(DEST / f"age-pyramid-C1.pkl")

print("Saving age distribution")
(pyramid["male"] + pyramid["female"]).to_pickle(DEST / f"age-distribution-C1.pkl")

print("Saving total populations")
pop = pd.DataFrame({"population": pyramid.sum(1)})
pop.to_pickle(DEST / f"population-C1.pkl")

print("\nCurrent year distributions saved!")
