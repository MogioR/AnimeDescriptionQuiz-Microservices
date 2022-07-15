import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from peewee import *
from base_model import BaseModel
from users_model import UsersModel


class UsersGlobalConfigsModel(BaseModel):
    users_global_configs_id = IdentityField()
    users_global_configs_user_id = ForeignKeyField(
        UsersModel,
        backref='users',
        to_field='users_id',
        on_delete='cascade',
        on_update='cascade',
    )

    class Meta:
        db_table = "users_global_configs"