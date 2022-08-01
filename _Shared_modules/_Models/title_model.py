from peewee import *
from datetime import datetime
from .base_model import BaseModel


class TitleModel(BaseModel):
    title_id = IdentityField()
    title_type = SmallIntegerField(null=False)  # 0-anime, 1-manga, 2-ranobe
    title_sub_type = SmallIntegerField(null=False)  # 0-TV, 1-Film, 2-Speshial, 3-OVA, 4-ONA
    title_shikimori_id = FixedCharField(null=False, max_length=20)
    title_creation_date = DateField(null=False, default=datetime.now())
    title_rating = FloatField(null=False, default=0)

    class Meta:
        db_table = "title"
        order_by = ('title_id',)