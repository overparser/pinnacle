from get_html.async_get_html import async_get_objects  # type: ignore
from Parser.sport_dict import SPORTS_DICT  # type: ignore
from typing import Dict, List, Union, Tuple, Mapping


def leagues_url(sport_name: str, sport_id: int) -> Tuple[str, str]:
    """:returns a tuple of links to api (url, referer)"""
    referer = f"https://www.pinnacle.com/ru/{sport_name}/leagues"
    # referer - адрес с которого происходит запрос к апи в браузере
    url = f"https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/leagues?all=false"
    # url - api request to object
    return url, referer


def matchup_tuple_of_urls(
    league_object: Mapping[str, dict], type_: str
) -> Tuple[str, str]:
    """генерирует ссылки и возвращает кортеж ссылок для последующих запросов в async_get_objects (url, referer)

    type info - matchup info request link
    type price - matchup price request link
    referer - the page from which the request to the api occurs in the browser
    """
    league_object = league_object if isinstance(league_object, dict) else {}

    sport_name = league_object["sport"]["name"]
    league_id = league_object["id"]
    league_name = league_object["name"]
    referer = f"https://www.pinnacle.com/ru/{format_to_url(sport_name)}/{format_to_url(league_name)}/matchups"
    if type_ == "info":
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/matchups"
    else:
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/markets/straight"
    return url, referer


def format_to_url(string: str) -> str:
    """prepare string to url"""
    string = (
        string.replace(" ", "-")
        .replace("--", "-")
        .replace("--", "-")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "")
        .lower()
    )
    return string


def is_moneyline(obj: Dict[str, str]) -> bool:
    """return True if moneyline in object"""
    obj = obj if isinstance(obj, dict) else {}
    if not all([word in obj for word in ["key", "isAlternate", "type"]]):
        return False
    elif obj["key"] == "s;0;m" and obj["type"] == "moneyline":
        return True
    return False


def is_matchup(obj: Dict[str, dict]) -> bool:
    """:return True if object is not live and not set"""
    obj = obj if isinstance(obj, dict) else {}

    if not all([word in obj for word in ["id", "participants", "isLive"]]):
        return False
    if ")" in obj["participants"][0]["name"]:
        return False
    if "Set " in obj["participants"][0]["name"]:
        return False
    if obj["isLive"]:
        return False
    return True


def join_price_and_info(
    price_objects: List[dict], info_objects: List[dict]
) -> List[dict]:
    """объединяет объекты с разной информацией о матче если у них совпадает id
    (в одном объекте указаны ставки, в другом информация)
    """
    price_objects = price_objects if isinstance(price_objects, list) else []
    info_objects = info_objects if isinstance(info_objects, list) else []

    matchups_list = []
    for price_obj in price_objects:
        for info_obj in info_objects:
            if "id" not in info_obj or "matchupId" not in price_obj:
                continue
            if info_obj["id"] == price_obj["matchupId"]:
                price_obj.update(info_obj)
                matchups_list.append(price_obj)
                break
    return matchups_list


def get_leagues_objects(sport_name: str) -> List[dict]:
    """получает ссылку апи на объекты всех лиг в рамках спорта, возвращает список объектов лиг"""
    sport_id = SPORTS_DICT[sport_name]
    leagues_tuple_url = leagues_url(sport_name, sport_id)
    # url to api for league object
    return async_get_objects(leagues_tuple_url)


def get_matchups_objects_from_leagues(
    leagues_objects: List[dict], type_="price/info"
) -> List[dict]:
    """запрашивает объекты матчей

    price - указаны все виды ставок
    info - информация о матче, дата, имена команд итд

    генерирует список кортежей ссылок [(url, referer), ...] из объектов лиг
    делает асинхронные запросы из списка кортежей.
    фильтрует объекты матчей по параметрам
    """
    urls_price_list = [matchup_tuple_of_urls(obj, type_) for obj in leagues_objects]
    matchup_objects = async_get_objects(urls_price_list)
    if type_ == "price":
        return list(filter(is_moneyline, matchup_objects))  # filtering by param
    elif type_ == "info":
        return list(filter(is_matchup, matchup_objects))  # filtering by param
    return []


def find_matchups_with_moneyline(sport_name: str):
    """
    получает объекты всех лиг в рамках спорта,
    затем запрашивает объекты матчей price_objects и info_objects и объединяет их.
    """
    leagues_objects = get_leagues_objects(sport_name)
    matchups_price_objects = get_matchups_objects_from_leagues(leagues_objects, "price")
    matchups_info_objects = get_matchups_objects_from_leagues(leagues_objects, "info")
    full_objects = join_price_and_info(matchups_price_objects, matchups_info_objects)
    return full_objects


full_obj = find_matchups_with_moneyline("hockey")
print("матчей с денежной линией найдено: ", len(full_obj), full_obj)
