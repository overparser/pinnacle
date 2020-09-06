from Parser.parser import *
import unittest
import sys
import os
sys.path.append(os.getcwd())



class TestLeagueList(unittest.TestCase):
    sport_name = 'hockey'
    sport_id = sports_dict[sport_name]
    leagues_objects = leagues_list_obj(sport_name, sport_id)
    list_of_urls_objects = list(map(matchup_url_obj, leagues_objects))
    price_objects = get_async_matchup_objs(list_of_urls_objects, 'url_price')
    info_objects = get_async_matchup_objs(list_of_urls_objects, 'url_info')
    price_objects = [i for i in price_objects if is_money_line(i)]  # оставляет только денежную линию
    info_objects = [i for i in info_objects if is_match(i)]  # фильтр актуальных матчей без лайва

    def test_league_list(self):
        self.assertNotEqual(leagues_list_obj('tennis', 33), ['detail', 'status', 'title', 'type'])
        self.assertNotEqual(leagues_list_obj('esports', 12), ['detail', 'status', 'title', 'type'])
        self.assertNotEqual(leagues_list_obj('hockey', 19), ['detail', 'status', 'title', 'type'])
        self.assertIsInstance(leagues_list_obj('tennis', 23), list)
        self.assertIsInstance(leagues_list_obj('tennisww', 23), list)
        self.assertIsInstance(leagues_list_obj(False, 23), list)
        self.assertIsInstance(leagues_list_obj(123, 23), list)
        self.assertIsInstance(leagues_list_obj(list, 23), list)
        self.assertIsInstance(leagues_list_obj(None, 23), list)


    def test_url_objs(self):
        self.assertIsInstance(matchup_url_obj(self.leagues_objects[0]), dict)
        self.assertIsInstance(matchup_url_obj(self.leagues_objects[1]), dict)
        self.assertIsInstance(matchup_url_obj({}), dict)
        self.assertIsInstance(matchup_url_obj(135), dict)
        self.assertIsInstance(matchup_url_obj(''), dict)
        self.assertIsInstance(matchup_url_obj(None), dict)


    def test_get_async_matchup_objs(self):
        self.assertIsInstance(get_async_matchup_objs(self.list_of_urls_objects, 'url_price'), list)
        self.assertIsInstance(get_async_matchup_objs(self.list_of_urls_objects, 'info'), list)
        self.assertIsInstance(get_async_matchup_objs(self.list_of_urls_objects[0], 'url_price'), list)
        self.assertIsInstance(get_async_matchup_objs(self.list_of_urls_objects[0], 'info'), list)
        self.assertIsInstance(get_async_matchup_objs([], 'url_price'), list)
        self.assertIsInstance(get_async_matchup_objs([], 'info'), list)
        self.assertIsInstance(get_async_matchup_objs(False, 'info'), list)
        self.assertIsInstance(get_async_matchup_objs(self.list_of_urls_objects, False), list)
        self.assertIsInstance(get_async_matchup_objs(144, 144), list)

    def test_is_money_line(self):
        self.assertTrue(is_money_line({'key': 's;0;m', 'isAlternate': True, 'type': 'moneyline'}))
        self.assertFalse(is_money_line({'isAlternate': True, 'type': 'moneyline'}))
        self.assertFalse(is_money_line({'key': 's;0;m', 'isAlternate': True, 'type': 12335}))
        self.assertFalse(is_money_line(1234356))
        self.assertFalse(is_money_line('string'))
        self.assertFalse(is_money_line(None))

    def test_is_match(self):
        self.assertTrue(is_match({
            'id': 12356,
            'participants':
                [{'alignment': 'neutral', 'id': 1167618336, 'name': 'Over', 'order': 0, 'rotation': 32}],
            'isLive': False}))
        self.assertFalse(is_match({'isAlternate': True, 'type': 'moneyline'}))
        self.assertFalse(is_match({'key': 's;0;m', 'isAlternate': True, 'type': 12335}))
        self.assertFalse(is_match(1234356))
        self.assertFalse(is_match('string'))
        self.assertFalse(is_match(None))

    def test_full_obj(self):
        self.assertIsInstance(splice_objs(self.price_objects, self.info_objects), list)
        self.assertIsInstance(splice_objs(self.price_objects[0], self.info_objects), list)
        self.assertIsInstance(splice_objs(self.price_objects, self.info_objects[0]), list)
        self.assertIsInstance(splice_objs(self.price_objects, None), list)
        self.assertIsInstance(splice_objs(None, self.info_objects), list)

if __name__ == '__main__':
    unittest.main()