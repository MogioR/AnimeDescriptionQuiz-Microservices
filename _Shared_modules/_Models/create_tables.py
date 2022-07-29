import json

from _Models.user_model import UserModel
from _Models.user_stats_model import UserStatsModel
from _Models.user_config_model import UserConfigModel

from _Models.title_model import TitleModel
from _Models.title_name_model import TitleNameModel

from _Models.question_model import QuestionModel
from _Models.question_answer_model import QuestionAnswerModel

from _Models.tag_model import TagModel
from _Models.tag_title_model import TagTitleModel

from _Models.user_title_model import UserTitleModel


UserTitleModel.drop_table()
UserConfigModel.drop_table()
UserStatsModel.drop_table()
UserModel.drop_table()
TagTitleModel.drop_table()
TagModel.drop_table()
QuestionAnswerModel.drop_table()
QuestionModel.drop_table()
TitleNameModel.drop_table()
TitleModel.drop_table()

TitleModel.create_table()
TitleNameModel.create_table()
QuestionModel.create_table()
QuestionAnswerModel.create_table()
TagModel.create_table()
TagTitleModel.create_table()
UserModel.create_table()
UserStatsModel.create_table()
UserConfigModel.create_table()
UserTitleModel.create_table()

# Users
user = UserModel.create(user_login='Blackfan', user_pass_hash='precure==black')
UserConfigModel.create(user_config_user_id=user.user_id)
UserStatsModel.create(user_stats_user_id=user.user_id)

user = UserModel.create(user_login='admin', user_pass_hash='admin')
UserConfigModel.create(user_config_user_id=user.user_id)
UserStatsModel.create(user_stats_user_id=user.user_id)

user = UserModel.create(user_login='mogior', user_pass_hash='mogior')
UserConfigModel.create(user_config_user_id=user.user_id)
UserStatsModel.create(user_stats_user_id=user.user_id, user_stats_special_points=1000)

# Tags
comedy_tag = TagModel.create(tag_name='Comedy')


# Titles
    # Clanad
title = TitleModel.create(title_type=0, title_shikimori_id='z2167', title_rating=8.03)
TitleNameModel.create(title_name_title_id=title.title_id, title_name_name='Кланнад', title_names_language=1)
TitleNameModel.create(title_name_title_id=title.title_id, title_name_name='Clannad', title_names_language=2)

question = QuestionModel.create(question_lang=1, question_type=0, question_source=json.dumps(
    ['Томоя Окадзаки — бездельник, уверенный, что жизнь скучна, а сам он ни на что не годен. Он ненавидит свой город. '
     'Вместе с другом Сунохарой они постоянно прогуливают школу и делают что им заблагорассудится.'
     ], ensure_ascii=False))

QuestionAnswerModel.create(question_answer_question_id=question.question_id, question_answer_answer_id=title.title_id)
TagTitleModel.create(tag_title_tag_id= comedy_tag.tag_id, tag_title_title_id=title.title_id)

UserTitleModel.create(user_title_user_id=user.user_id, user_title_title_id=title.title_id)

    # Air
title = TitleModel.create(title_type=0, title_shikimori_id='101', title_rating=7.29)
TitleNameModel.create(title_name_title_id=title.title_id, title_name_name='Высь', titles_name_language=1)
TitleNameModel.create(title_name_title_id=title.title_id, title_name_name='Air', titles_name_language=2)

question = QuestionModel.create(question_lang=1, question_type=0, question_source=json.dumps(
    ['История повествует о путешествии Кунисаки Юкито, ищущего Крылатую Деву, привязанную к небесам много столетий '
     'назад. На поиски он отправился после того, как услышал от своей матери старую детскую сказку.'
     ], ensure_ascii=False))

QuestionAnswerModel.create(question_answer_question_id=question.question_id, question_answer_answer_id=title.title_id)


