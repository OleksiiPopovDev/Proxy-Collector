from datetime import datetime
from dto.proxy_dto import ProxyDto


class SourceDto:
    def __init__(
            self,
            url: str,
            hashsum: str = None,
            workable: bool = True,
            proxies: list[ProxyDto] = None,
            updated_at: datetime = datetime.now
    ) -> None:
        self.url: str = url
        self.hashsum: str = hashsum
        self.workable: bool = workable
        self.proxies: list[ProxyDto] = proxies
        self.update_at: datetime = updated_at
