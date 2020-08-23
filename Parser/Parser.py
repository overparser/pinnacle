from get_html.async_get_html import get_htmls

class Parser:
    def __getattr__(self, name):
        """генерирует атрибуты из видов спорта с сайта"""
        sports_obj = self.get_attrs_names()
        for key, value in sports_obj:
            object = {}
            object[key] = lambda: None
            setattr(object[key], 'get', lambda key=key, value=value: self.get(key, value))  # без бинда ~key=key не работает
            self.__dict__.update(object)
        return self.__dict__[name]

    def get(self, sport_name, sport_id):
        """получить все действующие игры из лиг по указаному спорту"""  # например Parser().tennis.get()
        target = GetMatchups(sport_name, sport_id)
        matchups_list = target.get()
        print('объектов найдено:  ', len(matchups_list))
        return matchups_list

    @staticmethod
    def get_attrs_names():
        """парсит ссылки и имена для __getattr__"""
        target = GetJsonObject()
        objs = target.sports_list()
        result = []
        for obj in objs:
            if ')' not in obj['name'] and '(' not in obj['name']:
                result.append((obj['name'].lower().replace(' ', '_'), obj['id']))
        return result

class GetMatchups:
    def __init__(self, sport_name, sport_id):
        self.get_page_info = GetJsonObject()
        self.sport_id = sport_id
        self.sport_name = sport_name
        self.game_info_list = []
        self.price_list = []
        self.matchups_list = []

    def get(self):
        self.league_games_info()
        self.game_price()
        self.matchups()
        return self.matchups_list

    def league_games_info(self):
        """объекты цен/матчей всех игр лиги"""
        leagues_id_list = [(i['id'], i['name']) for i in self.get_page_info.leagues_list(self.sport_id, self.sport_name)]
        result = []
        for i in self.get_page_info.matchup_list(leagues_id_list, self.sport_name):
            if i['hasMarkets'] and i['type'] == 'matchup' and not i['parent'] and i['type'] == 'matchup':
                result.append(i)
        print(len(result))
        self.game_info_list = result
        self.price_list = self.game_price()

    def game_price(self):
        urls = []
        for i in self.game_info_list:
            match_id = i['id']
            urls.append([f'https://guest.api.arcadia.pinnacle.com/0.1/matchups/{match_id}/markets/related/straight',
                         f'https://www.pinnacle.com/ru/{self.sport_name.replace("_", "-")}/matchups'])
        result = get_htmls(urls)
        return result

    def matchups(self):
        """добавляет в объект actual_matchup названия команд"""
        matchups_list = []
        for actual_matchup in self.price_list:
            if actual_matchup['key'] == 's;0;m' and 'isAlternate' in actual_matchup:
                if actual_matchup['type'] == 'moneyline':
                    matchupId = actual_matchup['matchupId']
                    for i in self.game_info_list:
                        if i['id'] == matchupId and ')' not in i['participants'][0]['name'] \
                                and 'Set ' not in i['participants'][0]['name']:
                            actual_matchup['participants'] = i['participants']
                            matchups_list.append(actual_matchup)
                            break
        self.matchups_list = matchups_list

class GetJsonObject:
    """возвращает объекты api arcadia"""
    def sports_list(self):
        return get_htmls(('https://guest.api.arcadia.pinnacle.com/0.1/sports', 'https://www.pinnacle.com/ru/sports/'))

    def leagues_list(self, sport_id, sport_name):
        return get_htmls((f'https://guest.api.arcadia.pinnacle.com/0.1/sports/{sport_id}/leagues?all=false', f'https://www.pinnacle.com/ru/{sport_name.replace("_", "-")}/leagues'))

    def matchup_list(self, leagues_id_list, sport_name):
        urls = []
        for league_id, league_name, in leagues_id_list:
            urls.append([f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/matchups',
                         f'https://www.pinnacle.com/ru/{sport_name.replace("_", "-")}/'f'{league_name.replace(" ", "-").replace("--","-").replace("--","-").lower()}/matchups'])
        return get_htmls(urls)

    def matchup_price_list(self, leagues_id_list, sport_name):
        urls = []
        for league_id, league_name, in leagues_id_list:
            urls.append([f'https://guest.api.arcadia.pinnacle.com/0.1/leagues/{league_id}/markets/straight',
                         f'https://www.pinnacle.com/ru/{sport_name.replace("_", "-")}/'f'{league_name.replace(" ", "-").replace("--", "-").replace("--", "-").lower()}/matchups'])
        return get_htmls(urls)