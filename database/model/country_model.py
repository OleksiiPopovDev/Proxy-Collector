from peewee import FloatField, CharField
from database.connector import BaseModel


class Country(BaseModel):
    name = CharField()
    code = CharField()
    code_3 = CharField()
    latitude = FloatField()
    longitude = FloatField()

    class Meta:
        indexes = (
            (('name', 'code'), True),
        )
