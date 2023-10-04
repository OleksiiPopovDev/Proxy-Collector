import requests
import hashlib
from alive_progress import alive_bar
from bash_menu_builder import View
from requests.exceptions import RequestException

from dto.country_dto import CountryDto
from dto.source_dto import SourceDto


class SourceService:
    def __init__(self):
        self.__source_list: list[SourceDto] = []

    def seed_sources(self):
        with open('resources/source_txt_proxies_links.txt', 'r') as file:
            links: list[str] = file.readlines()
            with alive_bar(len(links)) as bar:
                string: str = 'Checking Sources:'
                count_spaces: int = View.get_count_spaces_for_line_up(string, 25)
                bar.title(View.paint('\t{Yellow}%s%s{ColorOff}') % (string, ' ' * count_spaces))
                for link in links:
                    self.__prepare_sources(link)
                    bar()
                    exit()

            return self._proxy_list

            # countries = self.__prepare_countries(json.load(file))
            # country_names: list[str] = list(map(lambda c: c.name, countries))
            # biggest_name: int = View.count_biggest_line(country_names)
            #
            # with alive_bar(len(countries)) as bar:
            #     for country in countries:
            #         count_spaces: int = View.get_count_spaces_for_line_up(country.name, biggest_name)
            #         try:
            #             string: str = View.paint('\t{Yellow}Seed Country {ColorOff}-> {BCyan}%s%s{ColorOff}')
            #             bar.title(string % (country.name, ' ' * count_spaces))
            #
            #             CountryRepository.save(country)
            #         except IntegrityError as message:
            #             string: str = View.paint('{Yellow}[{BBlue}%s{Yellow}]%s {BRed}Error: {Red}%s{ColorOff}')
            #             print(string % (country.name, ' ' * count_spaces, message))
            #
            #         time.sleep(0.01)
            #         bar()

    def get_source_content(self, link: str) -> str:
        try:
            response = requests.get(link)
            return response.text

        except RequestException as message:
            print(View.paint('\t\t{BYellow}%s {ColorOff}>> {BRed}Error: {Red} %s{ColorOff}') % (link, message))
            return ''

    def __prepare_sources(self, link: str) -> None:
        source_content: str = self.get_source_content(link.strip())
        hasher = hashlib.sha256()
        hasher.update(source_content.encode('utf-8'))

        self.__source_list.append(SourceDto(
            url=link,
            hashsum=hasher.hexdigest(),
            workable=False if source_content == '' else True
        ))
