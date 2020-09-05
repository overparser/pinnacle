from Parser.Parser import Parser
import time
from Parser.json_writer import jsonDB
from Parser.draw import draw
from Session.Session import save_token
# _ = [save_token() for i in range(20)]
matchup_id = input('введите id матча:  ')
target = Parser()
try:
    with open('jsonDB.json', 'r') as file:
        pass
except:
    with open('jsonDB.json', 'w') as file:
        file.write('{}')

while True:
    start = time.time()
    result = target.e_sports.get()
    jsonDB(result)
    draw(matchup_id)
    print('заняло времени на парсинг:', time.time() - start)
    time.sleep(10)


# https://guest.api.arcadia.pinnacle.com/0.1/sessions/mWURECh1NmfJJhkY9UDcqBDlIc3M0cuF