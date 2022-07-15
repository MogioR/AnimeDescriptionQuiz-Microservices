from peewee import *
from base_model import BaseModel
from User.users_model import UsersModel
from User.users_global_stats_model import UsersGlobalStatsModel
from User.users_global_config_model import UsersGlobalConfigsModel


UsersGlobalConfigsModel.drop_table()
UsersGlobalStatsModel.drop_table()
UsersModel.drop_table()

UsersModel.create_table()
UsersGlobalStatsModel.create_table()
UsersGlobalConfigsModel.create_table()


user = UsersModel.create(users_login='Blackfan', users_pass_hash='precure==black')
UsersGlobalConfigsModel.create(users_global_configs_user_id=user.users_id)
UsersGlobalStatsModel.create(users_global_stats_user_id=user.users_id)

user = UsersModel.create(users_login='admin', users_pass_hash='admin')
UsersGlobalConfigsModel.create(users_global_configs_user_id=user.users_id)
UsersGlobalStatsModel.create(users_global_stats_user_id=user.users_id)

user = UsersModel.create(users_login='mogior', users_pass_hash='mogior')
UsersGlobalConfigsModel.create(users_global_configs_user_id=user.users_id)
UsersGlobalStatsModel.create(users_global_stats_user_id=user.users_id, users_global_stats_special_points=1000)