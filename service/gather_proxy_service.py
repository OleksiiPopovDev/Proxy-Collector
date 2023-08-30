from service.gather.proxy_gather_abstract import ProxyGatherAbstract
from repository.proxy_repository import ProxyRepository
from alive_progress import alive_bar
from view.view import View
from peewee import IntegrityError


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
        with alive_bar(len(proxies_list)) as bar:
            for proxy in proxies_list:
                ip = '%s:%d' % (proxy.ip, proxy.port)
                count_spaces: int = View.get_count_spaces_for_line_up(ip, 25)
                try:
                    string: str = View.paint('\t{Yellow}%s%s{ColorOff}')
                    bar.title(string % (ip, ' ' * count_spaces))

                    ProxyRepository.save(proxy)
                    self.__saved += 1
                except IntegrityError:
                    self.__duplicate += 1
                bar()
