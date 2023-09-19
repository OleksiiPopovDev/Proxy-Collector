from service.gather.proxy_gather_abstract import ProxyGatherAbstract
from bash_menu_builder import View
from alive_progress import alive_bar
from dto.proxy_dto import ProxyDto
import requests
from requests.exceptions import RequestException


class LinkProxyGatherService(ProxyGatherAbstract):
    def get_proxy_list(self) -> list[ProxyDto]:
        with open('resources/source_txt_proxies_links.txt', 'r') as file:
            links: list[str] = file.readlines()
            with alive_bar(len(links)) as bar:
                string: str = 'Parsing Sources:'
                count_spaces: int = View.get_count_spaces_for_line_up(string, 25)
                bar.title(View.paint('\t{Yellow}%s%s{ColorOff}') % (string, ' ' * count_spaces))
                for link in links:
                    self.__call_source(link.strip())
                    bar()

            return self._proxy_list

    def __call_source(self, link: str):
        try:
            response = requests.get(link)
        except RequestException as message:
            print(View.paint('\t\t{BYellow}%s {ColorOff}>> {BRed}Error: {Red} %s{ColorOff}') % (link, message))
            return

        if response.status_code != 200:
            return

        line: list[str] = response.text.split('\n')
        for proxy in line:
            if self.is_proxy(proxy):
                split = proxy.split(':')
                self._proxy_list.append(ProxyDto(
                    ip=split[0],
                    port=int(split[1])
                ))
