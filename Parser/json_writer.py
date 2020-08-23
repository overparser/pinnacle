import json
import time


def jsonDB(data):
    with open('jsonDB.json', 'r') as file:
        json_file = json.load(file)

    for i in data:
        prices = [i['prices'][0]['price'], i['prices'][1]['price']]
        names = [i['participants'][0]['name'], i['participants'][1]['name']]
        obj = {
            'prices': prices,
            'names': names
        }

        matchup_id = str(i['matchupId'])
        if matchup_id not in json_file:
            json_file[matchup_id] = {}
        json_file[matchup_id][str(int(time.time()))] = obj

    with open('jsonDB.json', 'w') as f:
        json.dump(json_file, f)