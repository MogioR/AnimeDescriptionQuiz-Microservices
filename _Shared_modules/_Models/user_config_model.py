from peewee import *
from .base_model import BaseModel
from .user_model import UserModel


class UserConfigModel(BaseModel):
    user_config_id = IdentityField()
    user_config_user_id = ForeignKeyField(
        UserModel,
        backref='user',
        to_field='user_id',
        on_delete='cascade',
        on_update='cascade',
    )
    user_shikimori_login = CharField(null=True, max_length=128)
    user_mal_login = CharField(null=True, max_length=128)
    user_anilist_login = CharField(null=True, max_length=128)

    class Meta:
        db_table = "user_config"
