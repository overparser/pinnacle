from Parser.parser import *
import unittest
import sys
import os
sys.path.append(os.getcwd())



# class TestLeagueList(unittest.TestCase):
#     def test_league_list_not_default(self):
#         self.assertNotEqual(leagues_list_obj('tennis', 33), ['detail', 'status', 'title', 'type'])
#         self.assertNotEqual(leagues_list_obj('esports', 12), ['detail', 'status', 'title', 'type'])
#         self.assertNotEqual(leagues_list_obj('hockey', 19), ['detail', 'status', 'title', 'type'])
#
#     def test_league_list_return_list(self):
#         self.assertIsInstance(leagues_list_obj('tennis', 23), list)
#         self.assertIsInstance(leagues_list_obj('tennisww', 23), list)
#         self.assertIsInstance(leagues_list_obj(False, 23), list)
#         self.assertIsInstance(leagues_list_obj(123, 23), list)
#         self.assertIsInstance(leagues_list_obj(list, 23), list)


class Test_matchup_url_obj(unittest.TestCase):
    sport_name = 'hockey'
    sport_id = sports_dict[sport_name]
    leagues_objects = leagues_list_obj(sport_name, sport_id)
    print('всего лиг найдено:', len(leagues_objects), leagues_objects)
    list_of_urls_objects = list(map(matchup_url_obj, leagues_objects))

    def test_matchup_obj_return_list(self):
        self.assertEqual(matchup_url_obj(self.leagues_objects[0]), [])
        self.assertEqual(matchup_url_obj(self.leagues_objects[1]), [])
        self.assertEqual(matchup_url_obj({}), [])
        self.assertEqual(matchup_url_obj(135), [])
        self.assertEqual(matchup_url_obj(''), [])
        self.assertEqual(matchup_url_obj(False), [])


if __name__ == '__main__':
    unittest.main()