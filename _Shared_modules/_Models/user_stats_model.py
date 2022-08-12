from peewee import *
from .base_model import BaseModel
from .user_model import UserModel


class UserStatsModel(BaseModel):
    user_stats_id = IdentityField()
    user_stats_user_id = ForeignKeyField(
        UserModel,
        backref='user',
        to_field='user_id',
        on_delete='cascade',
        on_update='cascade',
    )
    user_stats_exp = IntegerField(null=False, default=0)
    user_stats_special_points = IntegerField(null=False, default=0)

    user_stats_made_up_times = IntegerField(null=False, default=1)
    user_stats_guessed_times = IntegerField(null=False, default=1)

    class Meta:
        db_table = "user_stats"
