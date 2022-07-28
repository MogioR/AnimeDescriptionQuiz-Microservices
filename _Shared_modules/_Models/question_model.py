from peewee import *
from base_model import BaseModel


class QuestionModel(BaseModel):
    question_id = IdentityField()
    question_lang = SmallIntegerField(null=False, default=0)  # 0-unknown, 1-rus, 2-eng
    question_type = SmallIntegerField(null=False, default=0)  # 0-text, 1-picture, 2-video, 4-music
    question_source = TextField(null=False)

    question_made_up_times = IntegerField(null=False, default=0)
    question_guessed_times = IntegerField(null=False, default=0)

    class Meta:
        db_table = "question"
