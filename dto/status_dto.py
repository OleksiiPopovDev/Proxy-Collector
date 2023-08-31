from dto.proxy_dto import ProxyDto
from dto.country_dto import CountryDto
from database.enum.proxy_status import ProxyStatus


class StatusDto:
    def __init__(
            self,
            ip: ProxyDto,
            country: CountryDto,
            is_working: bool,
            status: ProxyStatus,
            response_time: float = None,
            response: str = None
    ) -> None:
        self.ip: ProxyDto = ip
        self.country: CountryDto = country
        self.is_working: bool = is_working
        self.status: ProxyStatus = status
        self.response_time: float = response_time
        self.response: str = response
