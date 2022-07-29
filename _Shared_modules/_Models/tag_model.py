from peewee import *
from .base_model import BaseModel


class TagModel(BaseModel):
    tag_id = IdentityField()
    tag_name = CharField(null=False, max_length=64)

    class Meta:
        db_table = "tag"
        order_by = ('tag_name',)
