from alive_progress import alive_bar
from bash_menu_builder import Draw

from dto.proxy_dto import ProxyDto
from repository.source_repository import SourceRepository
from service.gather.proxy_gather_abstract import ProxyGatherAbstract
from service.source_service import SourceService


class LinkProxyGatherService(ProxyGatherAbstract):
    def get_proxy_list(self) -> list[ProxyDto]:
        proxy_list: list[ProxyDto] = []
        source_service = SourceService()
        sources = list(SourceRepository.get_list())
        with alive_bar(len(sources)) as bar:
            bar.title(self.__output_title(0))
            for source_db in sources:
                source_real = source_service.get_source_content(link=source_db.url)
                if not source_real.workable:
                    source_real.hashsum = None
                    SourceRepository.update(source_real)
                    bar()
                    continue

                if source_real.hashsum == source_db.hashsum:
                    bar()
                    continue

                proxy_list += source_real.proxies
                SourceRepository.update(source_real)
                bar()
                bar.title(self.__output_title(len(proxy_list)))

        return proxy_list

    @staticmethod
    def __output_title(proxy_count: int) -> str:
        string: str = 'Check Sources'
        string2: str = ' [%d]:' % proxy_count
        count_spaces: int = Draw.get_count_spaces_for_line_up(string + string2, 25)
        return Draw.paint('\t{Yellow}%s {BBlue}[{Blue}%d{BBlue}]{Yellow}:%s{ColorOff}') % (
            string,
            proxy_count,
            ' ' * count_spaces
        )
