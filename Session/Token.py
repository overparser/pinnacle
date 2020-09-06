from document.document import read_csv, write_csv_lines
import os.path
import time


class Token:
    def __init__(self):
        self.path = 'text_files/token.csv'
        self.check_path()
        self.user_headers_list = read_csv(self.path)

    def check_path(self):
        if not os.path.exists(self.path):
            self.path = '../' + self.path

    def get_token(self):
        self.get_older_token()
        self.update_token_csv()
        return self.older_user_header

    def get_older_token(self):
        older_user_header = [0, 0, 0, 999999999999999999]  # init
        for line in self.user_headers_list:
            if line[0] == 'X-API-Key':
                continue
            older_user_header = line if int(line[3]) < int(older_user_header[3]) else older_user_header

        older_user_header[3] = round(time.time())
        self.older_user_header = older_user_header



    def update_token_csv(self):
        write_csv_lines(self.path, self.user_headers_list, 'w')