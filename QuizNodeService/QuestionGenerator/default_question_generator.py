import os
import sys
import json
from datetime import date, datetime, timedelta
from peewee import fn, JOIN
from playhouse.shortcuts import model_to_dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '\\_Shared_modules')
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '\\_Shared_modules\\_Models')

from i_question_generator import IQuestionGenerator
from question import Question
from _Models import TitleModel, QuestionModel, QuestionAnswerModel, UserTitleModel, TagTitleModel, TitleNameModel

ALL_TAGS = [1, 2, 3, 4, 5, 6, 7, 8, 9,
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 14, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 14, 35, 36, 37, 38, 39,
            40]


class DefaultQuestionGenerator(IQuestionGenerator):
    def __init__(self, question_settings: dict, players_ids: list):
        self.question_settings = question_settings
        self.players_ids = players_ids
        self.question_pool = []

    def get_questions(self, questions_count: int):
        title_base_filters = (
                (TitleModel.title_rating >= self.question_settings['rating_min']) &
                (TitleModel.title_rating <= self.question_settings['rating_max']) &
                (TitleModel.title_creation_date >= self.question_settings['creation_date_min']) &
                (TitleModel.title_creation_date <= self.question_settings['creation_date_max']) &
                (TitleModel.title_type << self.question_settings['title_allowed_types'])
        )

        query_titles = TitleModel.select(TitleModel.title_id).where(title_base_filters)

        allowed_tags = [tag for tag in ALL_TAGS if tag not in self.question_settings['exclude_tags']]
        query_tags = TitleModel.select(TitleModel.title_id) & TagTitleModel.select(TagTitleModel.tag_title_title_id) \
            .where(TagTitleModel.tag_title_tag_id << allowed_tags)

        if len(self.question_settings['include_tags']) > 0:
            query_tags = query_tags & TagTitleModel.select(TagTitleModel.tag_title_title_id) \
                .where(TagTitleModel.tag_title_tag_id << self.question_settings['include_tags'])

        if self.question_settings['only_users_lists']:
            query_players_lists_filters = UserTitleModel.select(UserTitleModel.user_title_title_id) \
                .where(UserTitleModel.user_title_user_id << self.players_ids)
        else:
            query_players_lists_filters = TitleModel.select(TitleModel.title_id)

        question_base_filters = (
                (QuestionModel.question_type << self.question_settings['question_allowed_types']) &
                (QuestionModel.question_made_up_times / QuestionModel.question_guessed_times >=
                 self.question_settings['quiz_chance_min']) &
                (QuestionModel.question_made_up_times / QuestionModel.question_guessed_times <=
                 self.question_settings['quiz_chance_max'])
        )

        query_filter = query_titles & query_tags & query_players_lists_filters
        titles = [row.title_id for row in query_filter]

        questions_query = QuestionModel.select(QuestionModel, QuestionAnswerModel, TitleModel) \
            .where(question_base_filters).join(QuestionAnswerModel).join(TitleModel) \
            .where(QuestionAnswerModel.question_answer_answer_id << titles) \
            .order_by(fn.Random())

        questions = []

        i = 0
        for q in questions_query:
            questions.append(q)
            i += 1
            if i == questions_count:
                break

        self.question_pool = []
        for question in questions:
            also_answer = QuestionAnswerModel.select(QuestionAnswerModel.question_answer_answer_id) \
                .where(QuestionAnswerModel.question_answer_question_id == question.question_id)
            also_answer = [answer.question_answer_answer_id.title_id for answer in also_answer]

            question = Question(
                json.loads(question.question_source),
                question.question_lang,
                question.question_made_up_times / question.question_made_up_times,
                question.question_type,
                also_answer,
                {
                    'title_names': list(TitleNameModel.select().where(
                        TitleNameModel.title_name_title_id == question.questionanswermodel.question_answer_answer_id
                    ).dicts()),
                    'title_data': model_to_dict(question.questionanswermodel.question_answer_answer_id)
                }
            )
            self.question_pool.append(question)

    def get_question(self):
        return self.question_pool.pop()

    def check_question(self, question: Question, answer: str) -> bool:
        pass


generator = DefaultQuestionGenerator({
    'rating_min': 8,
    'rating_max': 10,
    'creation_date_min': datetime(2020, 1, 1, 0, 00),
    'creation_date_max': datetime(2022, 12, 1, 0, 00),
    'quiz_chance_min': 0.0,
    'quiz_chance_max': 1.0,
    'title_allowed_types': [0],
    'question_allowed_types': [0],
    'include_tags': [],
    'exclude_tags': [1],
    'only_users_lists': False
},
    [

    ])



