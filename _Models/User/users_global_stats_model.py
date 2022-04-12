import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from peewee import *
from base_model import BaseModel
from users_model import UsersModel


class UsersGlobalStatsModel(BaseModel):
    users_global_stats_id = IdentityField()
    users_global_stats_user_id = ForeignKeyField(
        UsersModel,
        backref='users',
        to_field='users_id',
        on_delete='cascade',
        on_update='cascade',
    )
    users_global_stats_exp = IntegerField(null=False, default=0)
    users_global_stats_special_points = IntegerField(null=False, default=0)

    class Meta:
        db_table = "users_global_stats"
