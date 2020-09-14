from Parser.parser import *
import unittest
import sys
import os
from Parser.sport_dict import SPORTS_DICT

sys.path.append(os.getcwd())


class TestLeagueList(unittest.TestCase):
    def setUp(self) -> None:
        sport_name = "hockey"
        sport_id = SPORTS_DICT[sport_name]
        leagues_url_tuple = leagues_url(sport_name, sport_id)
        leagues_objects = async_get_objects([leagues_url_tuple])
        urls_price_list = [matchup_tuple_of_urls(i, "price") for i in leagues_objects]
        urls_info_list = [matchup_tuple_of_urls(i, "info") for i in leagues_objects]
        price_objects = async_get_objects(urls_price_list)
        info_objects = async_get_objects(urls_info_list)
        price_objects = [i for i in price_objects if is_moneyline(i)]
        info_objects = [i for i in info_objects if is_matchup(i)]
        full_obj = join_price_and_info(price_objects, info_objects)

    def test_leagues_url(self):
        self.assertIsInstance(leagues_url("tennis", 23), tuple)
        self.assertIsInstance(leagues_url("tennisww", 23), tuple)
        self.assertIsInstance(leagues_url(False, 23), tuple)
        self.assertIsInstance(leagues_url(123, 23), tuple)
        self.assertIsInstance(leagues_url(list, 23), tuple)
        self.assertIsInstance(leagues_url(None, 23), tuple)

    def test_matchup_urls(self):
        self.assertIsInstance(matchup_tuple_of_urls(None, ""), tuple)
        self.assertIsInstance(
            matchup_tuple_of_urls(self.leagues_objects[0], "info"), tuple
        )
        self.assertIsInstance(
            matchup_tuple_of_urls(self.leagues_objects[1], "info"), tuple
        )
        self.assertIsInstance(matchup_tuple_of_urls({}, "info"), tuple)
        self.assertIsInstance(matchup_tuple_of_urls(135, "info"), tuple)
        self.assertIsInstance(matchup_tuple_of_urls("", "info"), tuple)
        self.assertIsInstance(
            matchup_tuple_of_urls(self.leagues_objects[0], "price"), tuple
        )
        self.assertIsInstance(
            matchup_tuple_of_urls(self.leagues_objects[1], "price"), tuple
        )
        self.assertIsInstance(matchup_tuple_of_urls({}, "price"), tuple)
        self.assertIsInstance(matchup_tuple_of_urls(135, "price"), tuple)
        self.assertIsInstance(matchup_tuple_of_urls("", "price"), tuple)

    def test_is_money_line(self):
        self.assertTrue(
            is_moneyline({"key": "s;0;m", "isAlternate": True, "type": "moneyline"})
        )
        self.assertFalse(is_moneyline({"isAlternate": True, "type": "moneyline"}))
        self.assertFalse(
            is_moneyline({"key": "s;0;m", "isAlternate": True, "type": 12335})
        )
        self.assertFalse(is_moneyline(1234356))
        self.assertFalse(is_moneyline("string"))
        self.assertFalse(is_moneyline(None))

    def testis_matchup(self):
        self.assertTrue(
            is_matchup(
                {
                    "id": 12356,
                    "participants": [
                        {
                            "alignment": "neutral",
                            "id": 1167618336,
                            "name": "Over",
                            "order": 0,
                            "rotation": 32,
                        }
                    ],
                    "isLive": False,
                }
            )
        )
        self.assertFalse(is_matchup({"isAlternate": True, "type": "moneyline"}))
        self.assertFalse(
            is_matchup({"key": "s;0;m", "isAlternate": True, "type": 12335})
        )
        self.assertFalse(is_matchup(1234356))
        self.assertFalse(is_matchup("string"))
        self.assertFalse(is_matchup(None))

    def test_full_obj(self):
        self.assertIsInstance(
            join_price_and_info(self.price_objects, self.info_objects), list
        )
        self.assertIsInstance(
            join_price_and_info(self.price_objects[0], self.info_objects), list
        )
        self.assertIsInstance(
            join_price_and_info(self.price_objects, self.info_objects[0]), list
        )
        self.assertIsInstance(join_price_and_info(self.price_objects, None), list)
        self.assertIsInstance(join_price_and_info(None, self.info_objects), list)


if __name__ == "__main__":
    unittest.main()
