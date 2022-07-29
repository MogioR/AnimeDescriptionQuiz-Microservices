from peewee import *
from .base_model import BaseModel
from .question_model import QuestionModel
from .title_model import TitleModel


class QuestionAnswerModel(BaseModel):
    question_answer_question_id = ForeignKeyField(QuestionModel, backref='question', to_field='question_id',
                                                  on_delete='cascade', on_update="cascade")
    question_answer_answer_id = ForeignKeyField(TitleModel, backref='title', to_field='title_id', on_delete='cascade',
                                                on_update='cascade')

    class Meta:
        db_table = "question_answer"
        primary_key = CompositeKey('question_answer_question_id', 'question_answer_answer_id')
