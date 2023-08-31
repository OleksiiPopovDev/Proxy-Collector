from database.model.ip_model import IP
from database.model.status_model import Status
from database.model.country_model import Country
from dto.status_dto import StatusDto
from database.connector import Connector


class StatusRepository:
    @staticmethod
    def save(status_dto: StatusDto) -> None:
        db = Connector.get_connection()
        with db.transaction() as transaction:
            try:
                country = (Country.select().where(
                    (Country.name == status_dto.country.name) |
                    (Country.code == status_dto.country.code)
                ).get() if status_dto.country.name is not None else None)
            except Exception as message:
                print(message)
                country = None

            Status.insert(
                ip=IP.get(ip=status_dto.ip.ip, port=status_dto.ip.port),
                country=country,
                is_working=status_dto.is_working,
                status=status_dto.status.value,
                response_time=status_dto.response_time,
                response=status_dto.response
            ).on_conflict(
                update={Status.country: None}
            ).execute()

            (IP
             .update(tries=IP.tries + 1)
             .where((IP.ip == status_dto.ip.ip) & (IP.port == status_dto.ip.port))
             .execute())

            transaction.commit()
