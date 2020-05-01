import pytest
import mundi_demography, mundi

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

        df = db.mundi["age_distribution"]
        assert df.shape == (10, 21)
        assert df["age_distribution"].shape == (10, 21)

    def test_br_population(self, br):
        df = br.mundi[..., "population"]
        assert df.shape == (10, 8)

        df = br.mundi[..., "age_distribution"]
        assert df.shape == (10, 28)
        assert df["age_distribution"].shape == (10, 21)

        df = br.mundi[..., "age_pyramid"]
        assert df.shape == (10, 49)
        assert df["male"].shape == (10, 21)
