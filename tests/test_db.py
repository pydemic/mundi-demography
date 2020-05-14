import numpy as np
import pytest
from pandas.testing import assert_frame_equal, assert_index_equal

import mundi
from mundi_demography import population, age_distribution, age_pyramid


class TestDataFrameAccessor:
    @pytest.fixture(scope="class")
    def db(self):
        db = mundi.countries()
        return db.iloc[:10]

    @pytest.fixture(scope="class")
    def br(self):
        db = mundi.regions(country_code="BR", type="city")
        return db.iloc[:10]

    def test_extract_populations(self, db):
        extra = db.mundi["population"]
        assert (db.index == extra.index).all()
        assert extra.shape == (10, 1)
        assert extra.dropna().shape == (7, 1)  # AD, AI, and AQ
        assert extra.columns == ["population"]

    def test_extract_and_append_extra_columns(self, db):
        df = db.mundi[..., "age_distribution"]
        assert df.shape == (10, 22)
        assert df["age_distribution"].shape == (10, 21)

        extra = db.mundi["age_distribution"]
        assert extra.shape == (10, 21)

        assert_frame_equal(extra, df["age_distribution"], check_column_type=False)

    def test_br_population(self, br):
        df = br.mundi[..., "population"]
        assert df.shape == (10, 2)

        df1 = br.mundi[..., "age_distribution"]
        assert df1.shape == (10, 22)
        assert df1["age_distribution"].shape == (10, 21)

        df2 = br.mundi[..., "age_pyramid"]
        assert df2.shape == (10, 43)
        assert df2["age_pyramid", "male"].shape == (10, 21)

        kwargs = {"check_column_type": False, "check_names": False}
        assert_frame_equal(
            df1["age_distribution"], df.mundi["age_distribution"], **kwargs
        )
        assert_frame_equal(df2["age_pyramid"], df.mundi["age_pyramid"], **kwargs)

    def test_assign_correct_parent_populations(self):
        df = mundi.region("BR-DF")
        brasilia = mundi.region("BR/Brasília")
        assert df.population == brasilia.population

    def test_assign_correct_parent_populations_examples(self):
        assert population("BR-1") > 0
        assert population("BR-PA") > 0
        assert population("BR-1501") > 0
        assert population("BR-150102") > 0
        assert population("BR-1506807") > 0
        assert population("BR-SUS:15013") > 0

    def test_assign_correct_parent_demography(self):
        df = mundi.region("BR/Brasília")
        ages = age_distribution(df.id)
        pyramid = age_pyramid(df.id)
        assert ages.sum() == population(df.id)
        assert np.all(pyramid.sum(1) == ages)

    def test_age_distribution_index(self):
        df = age_distribution("BR-DF")
        us = age_distribution("US")
        assert_index_equal(us.index, df.index)
        assert us.index.dtype == int

        data = age_distribution(["US", "BR"])
        assert_index_equal(us.index, data.columns)
        assert data.columns.dtype == int

    def test_can_slice_age_distribution(self):
        df = age_distribution("BR-DF")
        assert df.loc[60:].sum() < df.sum()

    def test_age_pyramid_index(self):
        df = age_pyramid("BR-DF")
        us = age_pyramid("US", infer=True)
        assert_index_equal(us.index, df.index)
        assert us.index.dtype == int

    def test_can_slice_age_pyramid(self):
        df = age_pyramid("BR-DF")
        assert (df.loc[60:].sum() < df.sum()).all()
