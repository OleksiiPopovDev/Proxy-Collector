from alive_progress import alive_bar
from bash_menu_builder import Draw
from peewee import IntegrityError

from repository.proxy_repository import ProxyRepository
from service.gather.proxy_gather_abstract import ProxyGatherAbstract


class GatherProxyService:
    def __init__(self, proxy_gather: ProxyGatherAbstract):
        self.proxy_gather = proxy_gather
        self.__saved: int = 0
        self.__duplicate: int = 0

    def get_count_saved(self) -> int:
        return self.__saved

    def get_count_duplicates(self) -> int:
        return self.__duplicate

    def run(self):
        proxies_list = self.proxy_gather.get_proxy_list()
        proxies_list.sort(key=lambda proxy_data: proxy_data.ip)
        if not proxies_list:
            return
        with alive_bar(len(proxies_list)) as bar:
            for proxy in proxies_list:
                ip = '%s:%d' % (proxy.ip, proxy.port)
                count_spaces: int = Draw.get_count_spaces_for_line_up(ip, 25)
                try:
                    string: str = Draw.paint('\t{Yellow}%s%s{ColorOff}')
                    bar.title(string % (ip, ' ' * count_spaces))

                    ProxyRepository.save(proxy)
                    self.__saved += 1
                except IntegrityError:
                    self.__duplicate += 1
                bar()
