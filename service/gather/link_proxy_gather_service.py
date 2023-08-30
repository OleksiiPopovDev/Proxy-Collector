from service.gather.proxy_gather_abstract import ProxyGatherAbstract
from dto.proxy_dto import ProxyDto
import requests


class LinkProxyGatherService(ProxyGatherAbstract):
    def get_proxy_list(self) -> list[ProxyDto]:
        with open('resources/source_txt_proxies_links.txt', 'r') as file:
            links: list[str] = file.readlines()
            for link in links:
                self.__call_source(link.strip())

            return self._proxy_list

    def __call_source(self, link: str):
        response = requests.get(link)
        if response.status_code != 200:
            return

        line: list[str] = response.text.split('\n')
        for proxy in line:
            if not self.is_proxy(proxy):
                split = proxy.split(':')
                self._proxy_list.append(ProxyDto(
                    ip=split[0],
                    port=int(split[1])
                ))
