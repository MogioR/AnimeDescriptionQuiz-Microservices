from peewee import *
from .base_model import BaseModel


class AggregatorModel(BaseModel):
    aggregator_id = IdentityField()
    aggregator_name = CharField(null=False, max_length=64)

    class Meta:
        db_table = "aggregator"
        order_by = ('aggregator_name',)