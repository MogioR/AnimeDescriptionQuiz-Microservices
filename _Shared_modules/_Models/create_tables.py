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



