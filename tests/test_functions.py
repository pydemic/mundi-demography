from mundi_demography import age_distribution, population, age_pyramid


class TestMundiFunctions:
    def test_scalar_functions(self):
        assert population("BR") == 212559000
        assert population("Brazil") == 212559000

        df = age_distribution("BR")
        assert df.shape == (21,)
        assert df.name == "age_distribution"

        df = age_pyramid("BR-5300108")
        assert df.shape == (21, 2)
