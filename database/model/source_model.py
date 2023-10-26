from datetime import datetime
from peewee import CharField, BooleanField, DateTimeField
from database.connector import BaseModel


class Source(BaseModel):
    url = CharField()
    hashsum = CharField(null=True)
    workable = BooleanField(default=True)
    updated_at = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        indexes = (
            (('url',), True),
        )
