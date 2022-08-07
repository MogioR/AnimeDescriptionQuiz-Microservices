from peewee import *
from .base_model import BaseModel
from .aggregator_model import AggregatorModel
from .title_model import TitleModel


class AggregatorTitleModel(BaseModel):
    aggregator_title_aggregator_id = ForeignKeyField(AggregatorModel, backref='aggregator', to_field='aggregator_id',
                                                     on_delete='cascade', on_update="cascade")
    aggregator_title_title_id = ForeignKeyField(TitleModel, backref='title', to_field='title_id', on_delete='cascade',
                                                on_update='cascade')
    aggregator_title_aggregator_bd_id = FixedCharField(null=False, max_length=20)

    class Meta:
        db_table = "aggregator_title"
        primary_key = CompositeKey('aggregator_title_aggregator_id', 'aggregator_title_title_id')
