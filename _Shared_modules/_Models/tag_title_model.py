from peewee import *
from base_model import BaseModel
from tag_model import TagModel
from title_model import TitleModel


class TagTitleModel(BaseModel):
    tag_title_tag_id = ForeignKeyField(TagModel, backref='tag', to_field='tag_id', on_delete='cascade',
                                       on_update="cascade")
    tag_title_title_id = ForeignKeyField(TitleModel, backref='title', to_field='title_id', on_delete='cascade',
                                         on_update='cascade')

    class Meta:
        db_table = "tag_title"
        primary_key = CompositeKey('tag_title_tag_id', 'tag_title_title_id')
