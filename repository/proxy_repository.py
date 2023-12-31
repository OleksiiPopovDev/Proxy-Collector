from peewee import JOIN
from database.model.ip_model import IP
from database.model.status_model import Status
from dto.proxy_dto import ProxyDto
from dto.country_dto import CountryDto
from database.enum.proxy_status import ProxyStatus


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

    def get_unchecked_count(self, tries_limit: int):
        return self.__unchecked_query(tries_limit).count()

    def get_unchecked(self, tries_limit: int, limit: int = None, iteration: int = None):
        query = self.__unchecked_query(tries_limit)

        if limit is not None:
            query = query.limit(limit)
            if iteration is not None:
                query = query.offset(limit * (iteration - 1))

        return query.execute()

    @staticmethod
    def __unchecked_query(tries_limit: int = 5):
        return (
            IP
            .select()
            .join(Status, JOIN.LEFT_OUTER, on=(IP.id == Status.ip))
            .where((Status.status == ProxyStatus.INVALID.value) | (Status.status >> None))
            .where(IP.tries < tries_limit)
            .group_by(IP)
            .order_by(Status.created_at.desc(), IP.created_at.desc())
        )
