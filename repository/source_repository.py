from database.model.source_model import Source
from dto.source_dto import SourceDto
from datetime import datetime


class SourceRepository:
    @staticmethod
    def save(source_dto: SourceDto) -> None:
        Source.create(
            url=source_dto.url,
            hashsum=source_dto.hashsum,
            workable=source_dto.workable
        )

    @staticmethod
    def update(source_dto: SourceDto) -> None:
        (Source
         .update(
            hashsum=source_dto.hashsum,
            workable=source_dto.workable,
            updated_at=datetime.now
        )
         .where(Source.url == source_dto.url)
         .execute())

    @staticmethod
    def get_list():
        return Source.select()
