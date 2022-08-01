import os
import sys
import json
import re

from datetime import datetime, date

from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\_Shared_modules')
print(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\_Shared_modules')

from _Models import TagModel, TitleModel, TitleNameModel, TagTitleModel, QuestionModel, QuestionAnswerModel

month_str_to_int = {
    'янв': 1,
    'фев': 2,
    'мар': 3,
    'апр': 4,
    'май': 5,
    'мая': 5,
    'июн': 6,
    'июл': 7,
    'авг': 8,
    'сен': 9,
    'окт': 10,
    'ноя': 11,
    'дек': 12,
}

sub_type_to_int = {
    'TV Сериал': 0,
    'Фильм': 1,
    'Спешл': 2,
    'OVA': 3,
    'ONA': 4
}


def get_month(raw_month: str) -> int:
    for month in month_str_to_int.keys():
        if raw_month.find(month) != -1:
            return month_str_to_int[month]
    return None


def normalise_date(raw_date: str) -> date:
    if raw_date.find('г.') == -1:
        return date(1, 1, 1)
    else:
        raw_date = raw_date.replace(' ', '')
        split_date = raw_date.replace('-', ' ').split()

        day = 1
        month = 1
        year = 1

        if split_date[0] == 'с':
            if get_month(split_date[1]) is None:
                if int(split_date[1]) < 100:
                    day = int(split_date[1])
                    month = get_month(split_date[2])
                    year = int(split_date[3])
                else:
                    year = int(split_date[1])
            else:
                month = get_month(split_date[1])
                year = int(split_date[2])
        elif split_date[0] == 'в':
            if 1000 < int(split_date[1]) < 3000:
                year = int(split_date[1])
        elif get_month(split_date[0]) is not None:
            month = get_month(split_date[0])
            year = int(split_date[1])
        elif 0 < int(split_date[0]) < 40:
            day = int(split_date[0])
            month = get_month(split_date[1])
            year = int(split_date[2])
        elif 1000 < int(split_date[0]) < 3000:
            year = int(split_date[0])

        return date(year, month, day)


def get_name_lang(raw_name: str) -> int:
    buf = re.sub(r'[А-ЯЁа-яё]', '', raw_name)
    if len(buf) == len(raw_name):
        return 0
    else:
        return 1


def question_generator(raw_description) -> dict:
    question = raw_description
    while question.find('<sp>') != -1:
        pos_1 = question.find('<sp>')
        pos_2 = question.find('<sp>', pos_1+1)

        if min(pos_1, pos_2) == -1:
            return None

        question = (
                question[0:pos_1] + str('*' * (pos_2-pos_1-4)) +
                question[pos_2+4:len(question)]
        )

    question = question.strip()
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


with open("test_base.json", "r", encoding='utf-8') as f:
    test_base = json.load(f)


tags = set()
for title in tqdm(test_base['titles']):
    for tag in title['geners']:
        tags.add(tag)

# Tag upload
tag_to_tagID = dict()
for tag in tags:
    tag_to_tagID[tag] = TagModel.create(tag_name=str(tag)).tag_id

# Titles upload
for title in tqdm(test_base['titles']):
    title_model_id = TitleModel.create(
        title_type=0,
        title_sub_type=sub_type_to_int[title['subtype']],
        title_shikimori_id=title['id'],
        title_creation_date=normalise_date(title['relise-date']),
        title_rating=float(title['raiting'])
    ).title_id

    for name in title['names']:
        TitleNameModel.create(
            title_name_title_id=title_model_id,
            title_name_name=name,
            title_names_language=get_name_lang(name)
        )

    for tag in title['geners']:
        TagTitleModel.create(
            tag_title_tag_id=tag_to_tagID[tag],
            tag_title_title_id=title_model_id
        )

    question_source = question_generator(title['description'])
    if question_source is not None:
        question_id = QuestionModel.create(
            question_lang=1,
            question_type=0,
            question_source=json.dumps(question_source)
        )
        QuestionAnswerModel.create(
            question_answer_question_id=question_id,
            question_answer_answer_id=title_model_id
        )

