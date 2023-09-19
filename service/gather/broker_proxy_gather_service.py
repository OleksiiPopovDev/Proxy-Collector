from service.gather.proxy_gather_abstract import ProxyGatherAbstract
from dto.proxy_dto import ProxyDto
from dto.country_dto import CountryDto
from proxybroker import Broker
from asyncio import Queue
from repository.country_repository import CountryRepository
from bash_menu_builder import View
from alive_progress import alive_bar
import asyncio


class BrokerProxyGatherService(ProxyGatherAbstract):
    def __init__(self):
        super().__init__()
        self.__countries_found: list[str] = []
        self.__types: list[str] = ['HTTP', 'HTTPS']
        self.__countries: list[str] = []
        self.__limit: int = 10

    def set_limit(self, limit: int) -> None:
        self.__limit = limit

    def get_proxy_list(self) -> list[ProxyDto]:
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(
            broker.find(types=self.__types, countries=self.__countries, limit=self.__limit),
            self.__gather(proxies)
        )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)

        countries: dict[CountryDto] = self.__prepare_countries()

        return self.__prepare_proxies(self._proxy_list, countries)

    async def __gather(self, proxies: Queue):
        with alive_bar(self.__limit) as bar:
            while True:
                title = 'Broker runing...'
                count_spaces: int = View.get_count_spaces_for_line_up('Broker running...', 26)
                bar.title(View.paint('\t{Yellow}%s%s{ColorOff}') % (title, ' ' * count_spaces))

                proxy = await proxies.get()
                if proxy is None: break

                if proxy.geo.name not in self.__countries_found:
                    self.__countries_found.append(proxy.geo.name)

                self._proxy_list.append(ProxyDto(
                    ip=proxy.host,
                    port=int(proxy.port),
                    type=proxy.types,
                    country_name=proxy.geo.name,
                    response_time=proxy.avg_resp_time
                ))

                bar()

    def __prepare_countries(self) -> dict[CountryDto]:
        countries: dict[CountryDto] = {}

        for county in list(CountryRepository.get_list(self.__countries_found)):
            countries[county.name] = CountryDto(
                id=county.id,
                name=county.name,
                code=county.code,
                code_3=county.code_3
            )

        return countries

    @staticmethod
    def __prepare_proxies(proxies: list[ProxyDto], countries: dict[CountryDto]) -> list[ProxyDto]:
        index: int = 0
        for proxy in proxies:
            country_name = proxy.country_name
            country = countries.get(country_name)
            if isinstance(country, CountryDto):
                proxy.country = country

            proxies[index] = proxy
            index += 1

        return proxies
