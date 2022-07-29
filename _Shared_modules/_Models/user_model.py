from peewee import *
from datetime import datetime
from .base_model import BaseModel


class UserModel(BaseModel):
    user_id = IdentityField()
    user_login = CharField(null=False, max_length=32, unique=True)
    user_pass_hash = CharField(null=False, max_length=128)

    user_registration = DateField(null=False, default=datetime.now())
    user_last_login = DateField(null=False, default=datetime.now())

    class Meta:
        db_table = "user"
        order_by = ('user_id',)
