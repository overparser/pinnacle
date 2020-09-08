from Parser.parser import *
import unittest
import sys
import os
sys.path.append(os.getcwd())



class TestLeagueList(unittest.TestCase):
    sport_name = 'hockey'
    sport_id = sports_dict[sport_name]
    leagues_objects = leagues_list_obj(sport_name, sport_id)
    urls_price_list = [matchup_urls(i, 'price') for i in leagues_objects]  # кортежи (url_price, referer)
    urls_info_list = [matchup_urls(i, 'info') for i in leagues_objects]  # кортежи (url_info, referer)
    price_objects = get_htmls(urls_price_list)  # спислк объектов цен всех игр
    info_objects = get_htmls(urls_info_list)  # список объектов информации о матче всех игр
    price_objects = [i for i in price_objects if is_money_line(i)]  # фильтр по денежной линии
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
        self.assertIsInstance(matchup_urls(self.leagues_objects[0], 'price'), tuple)
        self.assertIsInstance(matchup_urls(self.leagues_objects[1], 'info'), tuple)
        self.assertIsInstance(matchup_urls({}, 'price'), tuple)
        self.assertIsInstance(matchup_urls(135, 'info'), tuple)
        self.assertIsInstance(matchup_urls('', 'price'), tuple)
        self.assertIsInstance(matchup_urls(None, ''), tuple)

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