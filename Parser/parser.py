from get_html.async_get_html import async_get_objects  # type: ignore
from Parser.sport_dict import SPORTS_DICT  # type: ignore

# def sports_list():
#     return get_htmls(('https://guest.api.arcadia.pinnacle.com/0.1/sports',  # url and referer
#                       'https://www.pinnacle.com/ru/sports/'))


def leagues_url(sport_name: str, sport_id: int) -> tuple:
    """:returns a tuple of links to api (url, referer)"""
    referer = f"https://www.pinnacle.com/ru/{sport_name}/leagues"
    # referer - the page from which the request to the api occurs in the browser
    url = f"https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/leagues?all=false"
    # url - api request to object
    return url, referer


def matchup_tuple_of_urls(league_object: dict, type_: str) -> tuple:
    """:returns tuple of requests api

    get attributes from object and return tuple of links
    """
    league_object = league_object if isinstance(league_object, dict) else {}
    if not all([word in league_object for word in ["sport", "id", "name"]]):
        return ()

    sport_name = league_object["sport"]["name"]
    league_id = league_object["id"]
    league_name = league_object["name"]
    referer = f"https://www.pinnacle.com/ru/{format_to_url(sport_name)}/{format_to_url(league_name)}/matchups"
    if type_ == "info":
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/matchups"
    else:
        url = f"https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/markets/straight"
    return url, referer
    # type info - matchup info request link
    # type price - matchup price request link
    # referer - the page from which the request to the api occurs in the browser


def format_to_url(string: str) -> str:
    """prepare string to url"""
    string = string.replace(" ", "-").replace("--", "-")
    string = string.replace("--", "-")
    string = string.replace("(", "").replace(")", "")
    return string


def is_moneyline(obj: dict) -> bool:
    """return True if moneyline in object"""
    obj = obj if isinstance(obj, dict) else {}

    if not all([word in obj for word in ["key", "isAlternate", "type"]]):
        return False
    if obj["key"] == "s;0;m" and "isAlternate" in obj:
        if obj["type"] == "moneyline":
            return True
    return False


def is_matchup(obj: dict) -> bool:
    """:return True if object is matchup object"""
    obj = obj if isinstance(obj, dict) else {}

    if not all([word in obj for word in ["id", "participants", "isLive"]]):
        return False
    if (
        ")" not in obj["participants"][0]["name"]
        and "Set " not in obj["participants"][0]["name"]
        and not obj["isLive"]
    ):
        return True
    return False


def join_price_info(price_objects: list, info_objects: list) -> list:
    """:returns joined price_obj and info_obj"""
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


def get_leagues_objects(sport_name) -> list:
    """:returns list of leagues objects from sport_name"""
    sport_id = SPORTS_DICT[sport_name]
    leagues_url_tuple = leagues_url(sport_name, sport_id)  # urls to league object
    return async_get_objects(leagues_url_tuple)


def get_price_objects_from_leagues(leagues_objects):
    """:returns price objects list

    generate links and does async requests
    """
    urls_price_list = [matchup_tuple_of_urls(obj, "price") for obj in leagues_objects]
    price_objects = async_get_objects(urls_price_list)
    # send list of tuples for async requests
    return [obj for obj in price_objects if is_moneyline(obj)]  # filter by param


def get_info_objects_from_leagues(leagues_objects):
    """:returns info objects list"""
    urls_info_list = [matchup_tuple_of_urls(obj, "info") for obj in leagues_objects]
    info_objects = async_get_objects(urls_info_list)
    # send list of tuples for async requests
    return [obj for obj in info_objects if is_matchup(obj)]  # filter by param


def find_matchups_with_moneyline(sport_name: str):
    """requests objects and connects them

    Requests and generates a list of objects with rates and information about sports"""
    leagues_objects = get_leagues_objects(sport_name)
    matchups_price_objects = get_price_objects_from_leagues(leagues_objects)
    matchups_info_objects = get_info_objects_from_leagues(leagues_objects)
    full_objects = join_price_info(matchups_price_objects, matchups_info_objects)
    print("матчей с денежной линией найдено: ", len(full_objects), full_objects)
    return full_objects


find_matchups_with_moneyline("hockey")
