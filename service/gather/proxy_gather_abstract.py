from abc import ABC, abstractmethod
from dto.proxy_dto import ProxyDto
import re


class ProxyGatherAbstract(ABC):
    def __init__(self):
        self._proxy_list: list[ProxyDto] = []

    @abstractmethod
    def get_proxy_list(self) -> list[ProxyDto]:
        pass

    @staticmethod
    def is_proxy(string: str) -> bool:
        is_proxy = re.match('^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5}$', string)
        return is_proxy is not None
