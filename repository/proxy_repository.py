from database.model.ip_model import IP
from dto.proxy_dto import ProxyDto
from dto.country_dto import CountryDto


class ProxyRepository:
    @staticmethod
    def save(proxy: ProxyDto) -> None:
        IP.create(
            ip=proxy.ip,
            port=proxy.port,
            type=proxy.type,
            country_id=proxy.country.id if isinstance(proxy.country, CountryDto) else None,
            response_time=proxy.response_time,
        )
