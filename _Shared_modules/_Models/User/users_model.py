import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from peewee import *
from datetime import datetime
from base_model import BaseModel


class UsersModel(BaseModel):
    users_id = IdentityField()
    users_login = CharField(null=False, max_length=32, unique=True)
    users_pass_hash = CharField(null=False, max_length=128)

    users_registration = DateField(null=False, default=datetime.now())
    users_last_login = DateField(null=False, default=datetime.now())

    # players_exp = IntegerField(null=False, default=0)
    # players_speshal_points = IntegerField(null=False, default=0)
    #
    # players_true_answers = IntegerField(null=False, default=0)
    # players_rounds_played = IntegerField(null=False, default=0)
    #
    # players_registration = DateField(null=False, default=datetime.now())
    # players_last_login = DateField(null=False, default=datetime.now())
    # players_is_baned = BooleanField(null=False, default=False)
    #
    # players_shikimori_login = CharField(null=True, max_length=128)
    # players_mal_login = CharField(null=True, max_length=128)
    # players_anilist_login = CharField(null=True, max_length=128)

    class Meta:
        db_table = "users"
        order_by = ('users_id',)