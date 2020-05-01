import pytest
from pandas.testing import assert_frame_equal

import mundi
import mundi_demography

mundi_demography.enable()


class TestDataFrameAccessor:
    @pytest.fixture(scope="class")
    def db(self):
        db = mundi.countries()
        return db.iloc[:10]

    @pytest.fixture(scope="class")
    def br(self):
        db = mundi.regions(country_code="BR", type="municipality")
        return db.iloc[:10]

    def test_extract_populations(self, db):
        extra = db.mundi["population"]
        assert extra.shape == (10, 1)
        assert extra.dropna().shape == (7, 1)  # AD, AI, and AQ

    def test_extract_and_append_extra_columns(self, db):
        df = db.mundi[..., "age_distribution"]
        assert df.shape == (10, 28)
        assert df["age_distribution"].shape == (10, 21)

        extra = db.mundi["age_distribution"]
        assert extra.shape == (10, 21)

        assert_frame_equal(extra, df["age_distribution"], check_column_type=False)

    def test_br_population(self, br):
        df = br.mundi[..., "population"]
        assert df.shape == (10, 8)

        df1 = br.mundi[..., "age_distribution"]
        assert df1.shape == (10, 28)
        assert df1["age_distribution"].shape == (10, 21)

        df2 = br.mundi[..., "age_pyramid"]
        assert df2.shape == (10, 49)
        assert df2["age_pyramid", "male"].shape == (10, 21)

        kwargs = {"check_column_type": False, "check_names": False}
        assert_frame_equal(
            df1["age_distribution"], df.mundi["age_distribution"], **kwargs
        )
        assert_frame_equal(df2["age_pyramid"], df.mundi["age_pyramid"], **kwargs)
