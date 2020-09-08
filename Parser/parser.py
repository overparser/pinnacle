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


def leagues_url(sport_name: str, sport_id: int) -> tuple:
    """возвращает кортеж ссылок api (url, referer) на объекты лиги"""
    referer = f'https://www.pinnacle.com/ru/{sport_name}/leagues'
    # referer - страница с которой в браузере происходит запрос к апи
    url = f'https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/leagues?all=false'
    # url - запрос к апи
    return url, referer


def matchup_urls(league_object: dict, type_: str) -> tuple:
    """возвращает кортеж ссылок api на запросы объектов price/info всех игр (url_info/url_price, referer)"""
    league_object = league_object if isinstance(league_object, dict) else {}
    if not all([i in league_object for i in ['sport', 'id', 'name']]):
        return ()
    if type_ != 'price' and type_ != 'info':
        return ()

    sport_name = league_object['sport']['name']
    league_id = league_object['id']
    league_name = league_object['name']
    referer = f'https://www.pinnacle.com/ru/{format_to_url(sport_name)}/{format_to_url(league_name)}/matchups'
    # referer - страница с которой в браузере происходит запрос к апи}
    if type_ == 'info':
        url_info = f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/matchups'
        # url_info - ссылка запроса объекта с информацией о матче,
        return url_info, referer
    if type_ == 'price':
        url_price = f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/markets/straight'
        # url_price - ссылка запроса объекта с прайсом матча
        return url_price, referer

def format_to_url(string: str) -> str:
    """подгоняет текст под ссылку"""
    while '--' in string or ' ' in string or '(' in string:
        string = string.replace(' ', '-').replace('--', '-').lower()
        string = string.replace('(', '').replace(')', '')
    return string

def is_money_line(obj: dict) -> bool:
    """проверка что объект info является денежной линией"""
    obj = obj if isinstance(obj, dict) else {}
    if not all([i in obj for i in ['key', 'isAlternate', 'type']]):
        return False

    if obj['key'] == 's;0;m' and 'isAlternate' in obj:
        if obj['type'] == 'moneyline':
            return True

def is_match(obj: dict) -> bool:
    """проверка что объект info является объектом матча"""
    obj = obj if isinstance(obj, dict) else {}
    if not all([i in obj for i in ['id', 'participants', 'isLive']]):
        return False

    if obj['id'] and ')' not in obj['participants'][0]['name'] and 'Set ' not in obj['participants'][0]['name']\
            and not obj['isLive']:
        return True


def splice_price_info(price_objects: list, info_objects: list) -> list:
    """соединяет объекты price_obj и info_obj"""
    price_objects = price_objects if isinstance(price_objects, list) else []
    info_objects = info_objects if isinstance(info_objects, list) else []
    matchups_list = []
    for price_obj in price_objects:
            for info_obj in info_objects:
                if 'id' not in info_obj or 'matchupId' not in price_obj:
                    continue
                if info_obj['id'] == price_obj['matchupId']:
                    price_obj.update(info_obj)
                    matchups_list.append(price_obj)
                    break
    return matchups_list


def main():
    sport_name = 'hockey'
    sport_id = sports_dict[sport_name]
    leagues_url_tuple = leagues_url(sport_name, sport_id)  # ссылки на объекты лиг
    leagues_objects = get_htmls([leagues_url_tuple])  # получет объекты всех лиг
    urls_price_list = [matchup_urls(i, 'price') for i in leagues_objects]  # список кортежей (url_price, referer)
    urls_info_list = [matchup_urls(i, 'info') for i in leagues_objects]  # список кортежей (url_info, referer)
    price_objects = get_htmls(urls_price_list)  # получает список объектов цен всех игр
    info_objects = get_htmls(urls_info_list)  # получает список объектов информации о матче всех игр
    price_objects = [i for i in price_objects if is_money_line(i)]  # фильтр объектов price по денежной линии
    info_objects = [i for i in info_objects if is_match(i)]  # фильтр объектов info по актуальным матчам без лайва
    full_obj = splice_price_info(price_objects, info_objects)  # список объединеных объектов price и info всех игр
    print('матчей с денежной линией найдено: ', len(full_obj), full_obj)