import datetime

import requests
import json
import time
import os
import sys
import re

from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\_Shared_modules')
print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\_Shared_modules')

from base_anime_aggregator import BaseAnimeAggregator
from _Models import TitleModel, TitleNameModel, TagTitleModel, QuestionModel, QuestionAnswerModel, \
    AggregatorTitleModel

FORMAT_TO_INT = {
    None: 0,
    'TV': 1,
    'MOVIE': 2,
    'SPECIAL': 3,
    'OVA': 4,
    'ONA': 5,
    'TV_SHORT': 6,
    'MUSIC': 7
}

TAG_TO_INT = {
    'Sports': 1,
    'Mecha': 2,
    'Psychological': 3,
    'Drama': 4,
    'Horror': 5,
    'Slice of Life': 6,
    'Comedy': 7,
    'Romance': 8,
    'Sci-Fi': 9,
    'Mystery': 10,
    'Mahou Shoujo': 11,
    'Music': 12,
    'Action': 13,
    'Fantasy': 14,
    'Supernatural': 15,
    'Hentai': 16,
    'Ecchi': 17,
    'Adventure': 18,
    'Thriller': 19
}


class AnilistAnimeAggregator(BaseAnimeAggregator):
    def base_update(self):
        get_titles_query = '''
        query($page:Int = 1 $id:Int $type:MediaType $isAdult:Boolean $search:String 
        $format:[MediaFormat]$status:MediaStatus $countryOfOrigin:CountryCode $source:MediaSource $season:MediaSeason 
        $seasonYear:Int $year:String $onList:Boolean $yearLesser:FuzzyDateInt $yearGreater:FuzzyDateInt $episodeLesser:Int 
        $episodeGreater:Int $durationLesser:Int $durationGreater:Int $chapterLesser:Int $chapterGreater:Int $volumeLesser:Int 
        $volumeGreater:Int $licensedBy:[String]$isLicensed:Boolean $genres:[String]$excludedGenres:[String]$tags:[String]
        $excludedTags:[String]$minimumTagRank:Int $sort:[MediaSort]=[POPULARITY_DESC,SCORE_DESC]){Page(page:$page,perPage:20) {
            pageInfo { 
                total 
                perPage 
                currentPage 
                lastPage 
                hasNextPage    
            }
            media(id:$id type:$type season:$season format_in:$format status:$status countryOfOrigin:$countryOfOrigin 
            source:$source search:$search onList:$onList seasonYear:$seasonYear startDate_like:$year 
            startDate_lesser:$yearLesser startDate_greater:$yearGreater episodes_lesser:$episodeLesser 
            episodes_greater:$episodeGreater duration_lesser:$durationLesser duration_greater:$durationGreater 
            chapters_lesser:$chapterLesser chapters_greater:$chapterGreater volumes_lesser:$volumeLesser 
            volumes_greater:$volumeGreater licensedBy_in:$licensedBy isLicensed:$isLicensed genre_in:$genres 
            genre_not_in:$excludedGenres tag_in:$tags tag_not_in:$excludedTags minimumTagRank:$minimumTagRank sort:$sort 
            isAdult:$isAdult) { 
                id title {english, romaji, native}
                startDate{year month day}
                endDate{year month day}
                season 
                seasonYear 
                description 
                type 
                format 
                status(version:2)
                episodes 
                duration 
                chapters
                idMal 
                volumes 
                genres 
                isAdult
                averageScore 
                popularity 
                nextAiringEpisode{airingAt timeUntilAiring episode}
                mediaListEntry{id status}
                studios(isMain:true) {
                    edges {
                        isMain 
                        node {
                            id 
                            name
                        }
                    }
                }
            }
        }
        }
        '''
        vars = {
            'page': 1,
            'type': "ANIME",
            'sort': "POPULARITY_DESC"
        }
        url = 'https://graphql.anilist.co'
        response = requests.post(url, json={'query': get_titles_query, 'variables': vars})

        for title in response.json()['data']['Page']['media']:
            self.add_title_data(title)

        num = 1
        while True:
            num += 1
            if response.json()['data']['Page']['pageInfo']['hasNextPage'] is False:
                break

            vars['page'] = num
            response = requests.post(url, json={'query': get_titles_query, 'variables': vars})
            time.sleep(0.25)
            for title in response.json()['data']['Page']['media']:
                self.add_title_data(title)


    def get_user_titles(self):
        pass

    def add_title_data(self, title):
        creation_date = date(1, 1, 1)
        if title['startDate'] is not None:
            if title['startDate']['year'] is not None:
                year = title['startDate']['year']
            else:
                year = 1

            if title['startDate']['month'] is not None:
                month = title['startDate']['month']
            else:
                month = 1

            if title['startDate']['day'] is not None:
                day = title['startDate']['day']
            else:
                day = 1

            creation_date = date(
                year,
                month,
                day
            )

        if title['averageScore'] is None:
            score = 0
        else:
            score = float(title['averageScore']) / 10

        title_model_id = TitleModel.create(
            title_type=0,
            title_sub_type=FORMAT_TO_INT[title['format']],
            title_creation_date=creation_date,
            title_rating=score
        ).title_id

        for language in title['title'].keys():
            if language == 'english':
                title_names_language = 2
            elif language == 'romaji':
                title_names_language = 1
            else:
                title_names_language = 0

            if title['title'][language] is not None:
                TitleNameModel.create(
                    title_name_title_id=title_model_id,
                    title_name_name=title['title'][language],
                    title_names_language=title_names_language
                )

        for tag in title["genres"]:
            TagTitleModel.create(
                tag_title_tag_id=TAG_TO_INT[tag],
                tag_title_title_id=title_model_id
            )

        AggregatorTitleModel.create(
            aggregator_title_aggregator_id=3,
            aggregator_title_title_id=title_model_id,
            aggregator_title_aggregator_bd_id=str(title['id'])
        )

        if title["idMal"] is not None:
            AggregatorTitleModel.create(
                aggregator_title_aggregator_id=1,
                aggregator_title_title_id=title_model_id,
                aggregator_title_aggregator_bd_id=str(title["idMal"])
            )

        question_source = self.question_generator(title['description'])
        if question_source is not None:
            question_id = QuestionModel.create(
                question_lang=2,
                question_type=0,
                question_source=json.dumps(question_source)
            )
            QuestionAnswerModel.create(
                question_answer_question_id=question_id,
                question_answer_answer_id=title_model_id
            )

    def question_generator(self, raw_description) -> dict:
        if raw_description is None:
            return None

        question = raw_description.replace('<br>', '\n')
        question = re.sub(r'(Source: [^)]*)', '', question).strip()

        if len(question) > 0:
            return {
                'question': {
                    'hosts': [
                        {
                            'host': 'self',
                            'source': question
                        }
                    ]
                },
                'answer': {
                    'hosts': [
                        {
                            'host': 'self',
                            'source': re.sub('<sp>', '', raw_description)
                        }
                    ]
                }
            }
        else:
            return None


aaa = AnilistAnimeAggregator()
aaa.base_update()
