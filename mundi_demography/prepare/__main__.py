from . import loader


def main():
    loader.population_loader.run()
    loader.age_distribution_loader.run()
    loader.age_pyramid_loader.run()
    loader.yearly_population_loader.run()
    loader.yearly_age_distribution_loader.run()
    loader.yearly_age_pyramid_loader.run()


if __name__ == "__main__":
    main()
