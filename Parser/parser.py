from get_html.async_get_html import get_htmls

sports_dict = {
    'badminton': 1, 'bandy': 2, 'baseball': 3, 'basketball': 4, 'beach-volleyball': 5, 'boxing': 6,
    'chess': 7, 'cricket': 8, 'curling': 9, 'darts': 10, 'esports': 12, 'field-hockey': 13,
    'floorball': 14, 'football': 15, 'futsal': 16, 'golf': 17, 'handball': 18, 'hockey': 19,
    'horse-racing': 20, 'mixed-martial-arts': 22, 'other-sports': 23, 'politics': 24, 'rugby-league': 26,
    'rugby-union': 27, 'snooker': 28, 'soccer': 29, 'softball': 30, 'squash': 31, 'table-tennis': 32,
    'tennis': 33, 'volleyball': 34, 'water-polo': 36, 'aussie-rules': 39, 'alpine-skiing': 40,
    'biathlon': 41, 'ski-jumping': 42, 'cross-country': 43, 'formula-1': 44, 'cycling': 45,
    'bobsleigh': 46, 'figure-skating': 47, 'freestyle-skiing': 48, 'luge': 49, 'nordic-combined': 50,
    'short-track': 51, 'skeleton': 52, 'snow-boarding': 53, 'speed-skating': 54, 'olympics': 55,
    'athletics': 56, 'crossfit': 57, 'entertainment': 58, 'drone-racing': 60, 'poker': 62,
    'motorsport': 63, 'simulated-games': 64
}


# def sports_list():
#     return get_htmls(('https://guest.api.arcadia.pinnacle.com/0.1/sports',  # url and referer
#                       'https://www.pinnacle.com/ru/sports/'))


def leagues_list_obj(sport_name: str, sport_id: int):
    """список объектов всех лиг в рамках sport_name"""
    referer = f'https://www.pinnacle.com/ru/{sport_name}/leagues'
    # referer - страница с которой в браузере происходит запрос к апи
    url = f'https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/leagues?all=false'
    # url - запрос к апи
    return get_htmls((url, referer))


def matchup_url_obj(league_object: dict):
    """ссылки на запросы api всех игр в рамках лиги"""
    league_object = league_object if isinstance(league_object, dict) else {}
    if not all([i in league_object for i in ['sport', 'id', 'name']]):
        return []

    sport_name = league_object['sport']['name']
    league_id = league_object['id']
    league_name = league_object['name']
    return {
        'url_info': f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/matchups',
        'url_price': f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/markets/straight',
        'referer': f'https://www.pinnacle.com/ru/{replace_space(sport_name)}/'f'{replace_space(league_name)}/matchups'
    }

    # info_url - ссылка запроса объекта с информацией о матче,
    # price_url - ссылка запроса объекта с прайсом матча
    # referer - страница с которой в браузере происходит запрос к апи}



def get_async_matchup_objs(objects: list, type):
    objects = objects if isinstance(objects, list) else []
    if type not in 'url_price' + 'url_info':
        return []
    info_urls = [(obj[type], obj['referer']) for obj in objects]
    return get_htmls(info_urls)

def replace_space(string: str):
    """подгоняет текст под ссылку"""
    while '--' in string or ' ' in string:
        string = string.replace(' ', '-').replace('--', '-').lower()
    return string

def is_money_line(obj: dict):
    """проверка что объект является денежной линией"""
    if obj['key'] == 's;0;m' and 'isAlternate' in obj:
        if obj['type'] == 'moneyline':
            return True

def is_match(obj: dict):
    """проверка что это объект матча"""
    if obj['id'] and ')' not in obj['participants'][0]['name'] and 'Set ' not in obj['participants'][0]['name']\
            and not obj['isLive']:
        return True


def splice_objs(price_objects, info_objects):
    """соединяет объекты info и прайс"""
    matchups_list = []
    for price_obj in price_objects:
            for info_obj in info_objects:
                if info_obj['id'] == price_obj['matchupId']:
                    price_obj.update(info_obj)
                    matchups_list.append(price_obj)
                    break
    return matchups_list


def main():
    sport_name = 'aussie-rules'
    sport_id = sports_dict[sport_name]
    leagues_objects = leagues_list_obj(sport_name, sport_id)
    print('всего лиг найдено:', len(leagues_objects), leagues_objects)
    list_of_urls_objects = list(map(matchup_url_obj, leagues_objects))
    price_objects = get_async_matchup_objs(list_of_urls_objects, 'url_price')
    price_objects = [i for i in price_objects if is_money_line(i)]
    info_objects = get_async_matchup_objs(list_of_urls_objects, 'url_info')
    info_objects = [i for i in info_objects if is_match(i)]
    full_obj = splice_objs(price_objects, info_objects)
    print('результат', len(full_obj), full_obj)