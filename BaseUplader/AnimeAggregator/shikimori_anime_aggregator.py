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


class ShikimoriAnimeAggregator(BaseAnimeAggregator):
    def base_update(self):
        pass

    def get_user_titles(self):
        pass

    def get_title_data(self):
        pass
