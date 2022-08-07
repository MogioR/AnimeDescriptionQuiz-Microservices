import requests
import json
import time
import os
import sys
import re

from datetime import date
from mal import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\_Shared_modules')
print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\_Shared_modules')

from base_anime_aggregator import BaseAnimeAggregator
from _Models import TitleModel, TitleNameModel, TagTitleModel, QuestionModel, QuestionAnswerModel, \
    AggregatorTitleModel


class AnilistAnimeAggregator(BaseAnimeAggregator):
    def base_update(self):
        pass

    def get_user_titles(self):
        pass

    def get_title_data(self):
        pass


aggregator = AggregatorTitleModel.select().where(AggregatorTitleModel.aggregator_title_aggregator_id==3)

good = 0
bad = 0
all_ = 0

bad_list = []
good_list = []

for title in aggregator:
    all_ += 1
    try:
        Anime(int(title.aggregator_title_aggregator_bd_id)).title
        good += 1
        good_list.append(int(title.aggregator_title_aggregator_bd_id))
    except Exception as e:
        if e.args[0] == 'No such id on MyAnimeList':
            bad_list.append(int(title.aggregator_title_aggregator_bd_id))
            bad += 1
        else:
            print(all_)
            print(e)
            break
    time.sleep(1)
    if all_ % 100 == 0:
        print(bad/all_)
    if all_ % 1000 == 0:
        print(bad_list)

print(all_, good, good/all_, bad, bad/all_)

with open('good_anilist.json', "w", encoding='utf-8') as write_file:
    json.dump(good_list, write_file, ensure_ascii=False, indent=4)

with open('bad_anilist.json', "w", encoding='utf-8') as write_file:
    json.dump(bad_list, write_file, ensure_ascii=False, indent=4)
