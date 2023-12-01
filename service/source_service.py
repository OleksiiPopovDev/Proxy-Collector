import hashlib
import re
from typing import Union

import requests
from alive_progress import alive_bar
from bash_menu_builder import Draw
from peewee import IntegrityError
from requests.exceptions import RequestException

from dto.proxy_dto import ProxyDto
from dto.source_dto import SourceDto
from repository.source_repository import SourceRepository


class SourceService:
    def __init__(self):
        self.__source_list: list[SourceDto] = []
        self.__new_source_count: int = 0
        self.__duplicate_source_count: int = 0

    def seed_sources(self):
        with open('resources/source_txt_proxies_links.txt', 'r') as file:
            links: list[str] = file.readlines()
            with alive_bar(len(links)) as bar:
                string: str = 'Refresh Sources:'
                count_spaces: int = Draw.get_count_spaces_for_line_up(string, 25)
                bar.title(Draw.paint('\t{Yellow}%s%s{ColorOff}') % (string, ' ' * count_spaces))
                for link in links:
                    source = self.get_source_content(link.strip(), parse_proxies=False)
                    if not source:
                        bar()
                        continue

                    try:
                        source.hashsum = None
                        SourceRepository.save(source)
                        self.__new_source_count += 1
                    except IntegrityError:
                        self.__duplicate_source_count += 1
                    bar()

            print(Draw.paint('\t{Cyan}Saved new Sources {ColorOff}>> {BGreen}%d') % self.__new_source_count)
            print(Draw.paint('\t{Cyan}Duplicates Sources {ColorOff}>> {BRed}%d') % self.__duplicate_source_count)

    def get_source_content(self, link: str, parse_proxies: bool = True) -> Union[SourceDto, bool]:
        try:
            source_content = requests.get(link)

        except RequestException as message:
            print(Draw.paint('\t\t{BYellow}%s {ColorOff}>> {BRed}Error: {Red} %s{ColorOff}') % (link, message))
            return False

        else:
            status_code = source_content.status_code
            hasher = hashlib.sha256()
            content = source_content.text
            hasher.update(content.encode('utf-8'))

            proxies_list: list[ProxyDto] = []
            if parse_proxies:
                line: list[str] = content.splitlines()
                for proxy in line:
                    proxy = proxy.strip()
                    if self.is_proxy(proxy):
                        split = proxy.split(':')
                        proxies_list.append(ProxyDto(
                            ip=split[0],
                            port=int(split[1])
                        ))

            return SourceDto(
                url=link,
                hashsum=hasher.hexdigest() if status_code == 200 else None,
                workable=False if status_code != 200 else True,
                proxies=proxies_list
            )

    @staticmethod
    def is_proxy(string: str) -> bool:
        is_proxy = re.match('^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}$', string)
        return is_proxy is not None
