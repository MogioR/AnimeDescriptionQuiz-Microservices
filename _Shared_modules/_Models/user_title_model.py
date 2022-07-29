from peewee import *
from .base_model import BaseModel
from .user_model import UserModel
from .title_model import TitleModel


class UserTitleModel(BaseModel):
    user_title_user_id = ForeignKeyField(UserModel, backref='user', to_field='user_id',
                                         on_delete='cascade', on_update="cascade")
    user_title_title_id = ForeignKeyField(TitleModel, backref='title', to_field='title_id', on_delete='cascade',
                                          on_update='cascade')

    class Meta:
        db_table = "user_title"
        primary_key = CompositeKey('user_title_user_id', 'user_title_title_id')
