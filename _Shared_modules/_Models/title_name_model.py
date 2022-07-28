from peewee import *
from base_model import BaseModel
from title_model import TitleModel


class TitleNameModel(BaseModel):
    title_name_id = IdentityField()
    titles_name_title_id = ForeignKeyField(TitleModel, backref='title', to_field='title_id', on_delete='cascade',
                                           on_update='cascade')
    titles_name_name = CharField(null=False, max_length=128)
    titles_names_language = SmallIntegerField(null=False, default=0)  # 0-unknown, 1-rus, 2-eng

    class Meta:
        db_table = "title_name"
        order_by = ('titles_name_title_id',)
