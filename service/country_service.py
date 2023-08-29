from dto.country_dto import CountryDto
from repository.country_repository import CountryRepository
from alive_progress import alive_bar
from view.view import View
from peewee import IntegrityError
import json
import time


class CountryService:
    def seed_countries(self):
        with open('resources/countries.json', 'r') as file:
            countries = self.__prepare_countries(json.load(file))
            country_names: list[str] = list(map(lambda c: c.name, countries))
            biggest_name: int = View.count_biggest_line(country_names)

            with alive_bar(len(countries)) as bar:
                for country in countries:
                    count_spaces: int = View.get_count_spaces_for_line_up(country.name, biggest_name)
                    try:
                        string: str = View.paint('\t{Yellow}Seed Country {ColorOff}-> {BCyan}%s%s{ColorOff}')
                        bar.title(string % (country.name, ' ' * count_spaces))

                        CountryRepository.save(country)
                    except IntegrityError as message:
                        string: str = View.paint('{Yellow}[{BBlue}%s{Yellow}]%s {BRed}Error: {Red}%s{ColorOff}')
                        print(string % (country.name, ' ' * count_spaces, message))

                    time.sleep(0.01)
                    bar()

    @staticmethod
    def __prepare_countries(countries: list[object]) -> list[CountryDto]:
        prepared = map(lambda country: CountryDto(
            name=country['name'],
            code=country['code'],
            code_3=country['code_3'],
            latitude=country['latitude'],
            longitude=country['longitude']
        ), countries)

        return list(prepared)
