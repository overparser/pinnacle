from get_html.async_get_html import get_objects_from_list_of_tuples

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
    """:returns a tuple of links to api (url, referer)"""
    referer = f'https://www.pinnacle.com/ru/{sport_name}/leagues'
    # referer - the page from which the request to the api occurs in the browser
    url = f'https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/leagues?all=false'
    # url - api request to object
    return url, referer


def matchup_urls(league_object: dict, type_: str) -> tuple:
    """:returns api tuple request"""
    league_object = league_object if isinstance(league_object, dict) else {}
    if not all([word in league_object for word in ['sport', 'id', 'name']]):
        return ()
    if type_ != 'price' and type_ != 'info':
        return ()

    sport_name = league_object['sport']['name']
    league_id = league_object['id']
    league_name = league_object['name']
    referer = f'https://www.pinnacle.com/ru/{format_to_url(sport_name)}/{format_to_url(league_name)}/matchups'
    if type_ == 'info':
        url = f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/matchups'
    else:
        url = f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/markets/straight'
    return url, referer
    # type info - link for match info requests
    # type price - link for match price requests
    # referer - the page from which the request to the api occurs in the browser


def format_to_url(string: str) -> str:
    """prepare string to url"""
    while '--' in string or ' ' in string or '(' in string:
        string = string.replace(' ', '-').replace('--', '-').lower()
        string = string.replace('(', '').replace(')', '')
    return string


def is_moneyline(obj: dict) -> bool:
    """return True if moneyline in object"""
    obj = obj if isinstance(obj, dict) else {}
    if not all([word in obj for word in ['key', 'isAlternate', 'type']]):
        return False

    if obj['key'] == 's;0;m' and 'isAlternate' in obj:
        if obj['type'] == 'moneyline':
            return True


def is_match(obj: dict) -> bool:
    """:return True if object is matchup object"""
    obj = obj if isinstance(obj, dict) else {}
    if not all([word in obj for word in ['id', 'participants', 'isLive']]):
        return False

    if obj['id'] and ')' not in obj['participants'][0]['name'] and 'Set ' not in obj['participants'][0]['name']\
            and not obj['isLive']:
        return True


def join_price_info(price_objects: list, info_objects: list) -> list:
    """:returns joined price_obj and info_obj"""
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


def get_leagues_objects(sport_name):
    """:returns list of leagues objects from sport_name"""
    sport_id = sports_dict[sport_name]
    leagues_url_tuple = leagues_url(sport_name, sport_id)  # urls to league object
    return get_objects_from_list_of_tuples([leagues_url_tuple])  # fetch list of league objects


def get_price_objects_from_leagues(leagues_objects):
    """:returns price objects list"""
    urls_price_list = [matchup_urls(obj, 'price') for obj in leagues_objects]  # list of tuple [(url, referer)...]
    price_objects = get_objects_from_list_of_tuples(urls_price_list)  # list of matchups price objects [{}...]
    return [obj for obj in price_objects if is_moneyline(obj)]  # filter by moneyline in objects


def get_info_objects_from_leagues(leagues_objects):
    """:returns info objects list"""
    urls_info_list = [matchup_urls(obj, 'info') for obj in leagues_objects]  # список кортежей (url_info, referer)
    info_objects = get_objects_from_list_of_tuples(urls_info_list)  #  list of matchups info objects [{}...]
    return [obj for obj in info_objects if is_match(obj)]  # filter of info objects by actual matches without live


def find_matchups_with_moneyline(sport_name: str):
    """requests objects and connects them :returns joined price_objects and info objects"""
    leagues_objects = get_leagues_objects(sport_name)
    price_objects = get_price_objects_from_leagues(leagues_objects)
    info_objects = get_info_objects_from_leagues(leagues_objects)
    full_objects = join_price_info(price_objects, info_objects)
    print('матчей с денежной линией найдено: ', len(full_objects), full_objects)
    return full_objects

find_matchups_with_moneyline('hockey')