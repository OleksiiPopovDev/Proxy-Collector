from datetime import datetime
from peewee import FloatField, TextField, ForeignKeyField, BooleanField, DateTimeField
from database.connector import BaseModel
from database.model.ip_model import IP
from database.model.country_model import Country


class Status(BaseModel):
    ip = ForeignKeyField(IP, on_delete='CASCADE')
    country = ForeignKeyField(Country, null=True, on_delete='CASCADE')
    is_working = BooleanField(default=False)
    response_time = FloatField(null=True)
    response = TextField(null=True)
    created_at = DateTimeField(default=datetime.now)
