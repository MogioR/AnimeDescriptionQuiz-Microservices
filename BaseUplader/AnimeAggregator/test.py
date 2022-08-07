import requests
import json
import time

from tqdm import tqdm

rawGetList = '''
query($userId:Int, $userName:String, $type:MediaType) {
    MediaListCollection(userId:$userId, userName:$userName, type:$type) {
        lists {
            name  
            entries {
                ...mediaListEntry
            }
        }
    }
}
fragment 
mediaListEntry 
on 
MediaList { 
    mediaId 
}
'''

variables = {
    'userName': 'mogior',
    'type': "ANIME"
}

url = 'https://graphql.anilist.co'

# Anilist list
# response = requests.post(url, json={'query': rawGetList, 'variables': variables})
# print(response.text)
# answer = response.json()
# for anime_list in answer['data']['MediaListCollection']['lists']:
#     print('Anime list: ', anime_list['name'])
#     for title in anime_list['entries']:
#         print(title)

# Anilist titles
testMedia = '''
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

variables3 = {
    'page': 1,
    'type': "ANIME",
    'sort': "POPULARITY_DESC"
}

response = requests.post(url, json={'query': testMedia, 'variables': variables3})
print(response.text)
genres = set()
titles = dict()
format_ = set()

num = 2
for title in response.json()['data']['Page']['media']:
    titles[title['id']] = title
    for genre in title['genres']:
        genres.add(genre)

while True:
    try:
        num += 1
        _len = len(titles)
        if response.json()['data']['Page']['pageInfo']['hasNextPage'] is False:
            break
        response = requests.post(url, json={'query': testMedia, 'variables': {
            'page': num,
            'type': "ANIME",
            'sort': "POPULARITY_DESC"
        }})
        time.sleep(0.25)
        for title in response.json()['data']['Page']['media']:
            titles[title['id']] = title
            format_.add(title['format'])
            for genre in title['genres']:
                genres.add(genre)

        if _len == len(titles):
            break
    except Exception as e:
        print(e)
        print(response)
        print(response.json())
        break

print(response.json())

print(len(titles))
print(genres)
print(format_)

with open('anilist.json', "w", encoding='utf-8') as write_file:
    json.dump(titles, write_file, ensure_ascii=False, indent=4)

# Shikimori titles
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
#                          'Chrome/41.0.2228.0 Safari/537.3'}
#
# response = requests.get(url='https://shikimori.one/animes/z5114-fullmetal-alchemist-brotherhood', headers=headers)
# print(response.text)

def test_valid_login():
    url = 'https://httpbin.org/post'
    headers = {'Content-Type': 'application/json'}
    payload = {'login': 'test_valid_login', 'password': 'test_dsdgffdgdgsdgd'}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))
    assert resp.status_code == 200
    resp_body = resp.json()

    assert resp_body['nodeId'] == 0
    assert resp_body['access_token'] is str
    assert resp_body['refresh_token'] is str
    assert resp_body['expires_time'] is int

