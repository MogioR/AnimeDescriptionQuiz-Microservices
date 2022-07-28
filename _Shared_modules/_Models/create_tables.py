from _Models.user_model import UserModel
from _Models.user_stats_model import UserStatsModel
from _Models.user_config_model import UserConfigModel


# Users
UserConfigModel.drop_table()
UserStatsModel.drop_table()
UserModel.drop_table()

UserModel.create_table()
UserStatsModel.create_table()
UserConfigModel.create_table()


user = UserModel.create(users_login='Blackfan', users_pass_hash='precure==black')
UserConfigModel.create(users_global_configs_user_id=user.users_id)
UserStatsModel.create(users_global_stats_user_id=user.users_id)

user = UserModel.create(users_login='admin', users_pass_hash='admin')
UserConfigModel.create(users_global_configs_user_id=user.users_id)
UserStatsModel.create(users_global_stats_user_id=user.users_id)

user = UserModel.create(users_login='mogior', users_pass_hash='mogior')
UserConfigModel.create(users_global_configs_user_id=user.users_id)
UserStatsModel.create(users_global_stats_user_id=user.users_id, users_global_stats_special_points=1000)


