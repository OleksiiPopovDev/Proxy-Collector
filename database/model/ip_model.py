from peewee import IntegerField, FloatField, CharField, ForeignKeyField
from database.connector import BaseModel
from database.model.country_model import Country


class IP(BaseModel):
    ip = CharField()
    port = IntegerField()
    type = CharField(null=True)
    country = ForeignKeyField(Country, null=True, on_delete='CASCADE')
    response_time = FloatField(null=True)
    tries = IntegerField(default=0)

    class Meta:
        indexes = (
            (('ip', 'port'), True),
        )
