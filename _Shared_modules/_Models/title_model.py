from peewee import *
from datetime import datetime
from .base_model import BaseModel

# FORMAT_TO_INT = {
#     None: 0,
#     'TV': 1,
#     'MOVIE': 2,
#     'SPECIAL': 3,
#     'OVA': 4,
#     'ONA': 5,
#     'TV_SHORT': 6,
#     'MUSIC': 7
# }

class TitleModel(BaseModel):
    title_id = IdentityField()
    title_type = SmallIntegerField(null=False)  # 0-anime, 1-manga, 2-ranobe
    title_sub_type = SmallIntegerField(null=False)
    title_creation_date = DateField(null=False, default=datetime.now())
    title_rating = FloatField(null=False, default=0)

    class Meta:
        db_table = "title"
        order_by = ('title_id',)