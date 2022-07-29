import os
import sys
import peewee
from datetime import date, datetime, timedelta
from peewee import fn, JOIN

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '\\_Shared_modules')
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + '\\_Shared_modules\\_Models')

from i_question_generator import IQuestionGenerator
from question import Question
from _Models import TitleModel, QuestionModel, QuestionAnswerModel, UserTitleModel, TagTitleModel


class DefaultQuestionGenerator(IQuestionGenerator):
    def __init__(self, question_settings: dict, players_ids: list):
        self.question_settings = question_settings
        self.players_ids = players_ids

    def get_question(self):
        title_base_filters = (
                (TitleModel.title_rating >= self.question_settings['rating_min']) &
                (TitleModel.title_rating <= self.question_settings['rating_max']) &
                (TitleModel.title_creation_date >= self.question_settings['creation_date_min']) &
                (TitleModel.title_creation_date <= self.question_settings['creation_date_max']) &
                (TitleModel.title_type << self.question_settings['title_allowed_types'])
        )

        query_titles = TitleModel.select(TitleModel.title_id).where(title_base_filters)

        query_tags = TitleModel.select(TitleModel.title_id) & TagTitleModel.select(TagTitleModel.tag_title_title_id) \
            .where(TagTitleModel.tag_title_tag_id << self.question_settings['allowed_tags'])

        query_tags = query_tags - TagTitleModel.select(TagTitleModel.tag_title_title_id) \
            .where(TagTitleModel.tag_title_tag_id << self.question_settings['exclude_tags'])

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

        questions_query = (
            QuestionModel.select(QuestionModel, QuestionAnswerModel, TitleModel)
            .where(question_base_filters).join(QuestionAnswerModel).join(TitleModel)
            .where(QuestionAnswerModel.question_answer_answer_id << titles)
        )

        print(questions_query)
        for q in questions_query:
            print(q.__data__)
            print(q.questionanswermodel.question_answer_answer_id)

        # QuestionModel.select().where(base_filters).order_by(fn.Random()).get()

    def check_question(self, question: Question, answer: str) -> bool:
        pass


generator = DefaultQuestionGenerator({
    'rating_min': 8,
    'rating_max': 10,
    'creation_date_min': date.today() - timedelta(days=100),
    'creation_date_max': date.today() + timedelta(days=100),
    'quiz_chance_min': 0.0,
    'quiz_chance_max': 1.0,
    'title_allowed_types': [0, 1],
    'question_allowed_types': [0, 1],
    'include_tags': [],
    'exclude_tags': [],
    'allowed_tags': [0, 1, 2, 3],
    'only_users_lists': False
},
    [

    ])

generator.get_question()
