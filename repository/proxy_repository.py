from database.model.ip_model import IP
from dto.proxy_dto import ProxyDto


class ProxyRepository:
    @staticmethod
    def save(proxy: ProxyDto) -> None:
        IP.create(
            ip=proxy.ip,
            port=proxy.port,
            type=proxy.type,
            country=proxy.country,
            response_time=proxy.response_time,
        )
