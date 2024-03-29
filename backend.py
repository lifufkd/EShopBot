#####################################
#            Created by             #
#                SBR                #
#####################################
import os
import time
#####################################


class TempUserData:
    def __init__(self):
        super(TempUserData, self).__init__()
        self.__user_data = {}

    def temp_data(self, user_id):
        if user_id not in self.__user_data.keys():
            self.__user_data.update({user_id: [None, None, None]})
        return self.__user_data


class DbAct:
    def __init__(self, db, config):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config

    def get_money(self, user_id):
        money = self.__db.db_read('SELECT money, gold FROM users WHERE tg_id =?', (user_id, ))
        if len(money) > 0:
            return money[0]

    def add_user(self, user_id, nickname, first_name, last_name):
        if user_id in self.__config['admins']:
            role = True
        else:
            role = None
        self.__db.db_write('INSERT OR IGNORE INTO users (tg_id, nickname, first_name, last_name, money, gold, role, dialog_open) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, nickname, first_name, last_name, 0, 0, role, False))

    def user_is_existed(self, user_id):
        data = self.__db.db_read('SELECT count(*) FROM users WHERE tg_id = ?', (user_id, ))
        if len(data) > 0:
            if data[0][0] > 0:
                status = True
            else:
                status = False
            return status

    def add_request(self, user_id, quanity, type):
        self.__db.db_write(f'INSERT INTO request (tg_id, quanity, type) VALUES (?, ?, ?)', (user_id, quanity, type))

    def update_dialog_status(self, user_id, request_id):
        self.__db.db_write('UPDATE users SET current_dialog = ? WHERE tg_id = ?', (request_id, user_id))

    def get_dialog_status(self, user_id):
        data = self.__db.db_read('SELECT current_dialog FROM users WHERE tg_id = ?', (user_id,))
        if len(data) > 0:
            return data[0][0]

    def update_dialog_open(self, user_id, status):
        self.__db.db_write('UPDATE users SET dialog_open = ? WHERE tg_id = ?', (status, user_id))

    def get_dialog_status_client(self, user_id):
        data = self.__db.db_read('SELECT dialog_open FROM users WHERE tg_id = ?', (user_id,))
        if len(data) > 0:
            return data[0][0]

    def get_request_by_user_id(self, user_id, type):
        request = self.__db.db_read('SELECT request_id FROM request WHERE tg_id = ? AND type = ?', (user_id, type))
        if len(request) > 0:
            return request[0][0]

    def get_admin_id_from_request_id(self, user_id, type):
        req_id = self.get_request_by_user_id(user_id, type)
        data = self.__db.db_read('SELECT tg_id FROM users WHERE current_dialog = ?', (req_id, ))
        if len(data) > 0:
            return data[0][0]

    def get_request_money_by_req_id(self, req_id):
        data = self.__db.db_read('SELECT quanity FROM request WHERE request_id = ?', (req_id, ))
        if len(data) > 0:
            return data[0][0]

    def get_user(self, user_id):
        user = self.__db.db_read('SELECT nickname, first_name, last_name FROM users WHERE tg_id = ?', (user_id, ))
        if len(user) > 0:
            return list(user[0])

    def get_admins(self):
        data = list()
        admins = self.__db.db_read('SELECT tg_id FROM users WHERE role = "1"', ())
        if len(admins) > 0:
            for i in admins:
                data.append(i[0])
        else:
            data = []
        return set(data)

    def get_admins_not_busy(self):
        data = list()
        admins = self.__db.db_read(f'SELECT tg_id, current_dialog FROM users WHERE role = "1"', ())
        if len(admins) > 0:
            for i in admins:
                print(i)
                if i[1] is None:
                    data.append(i[0])
        else:
            data = []
        return set(data)

    def get_request_by_request_id(self, request):
        request = self.__db.db_read('SELECT tg_id FROM request WHERE request_id = ?', (request, ))
        if len(request) > 0:
            return request[0][0]

    def flush_gold(self, user_id, quanity):
        gold = self.get_gold(user_id)
        self.__db.db_write('UPDATE users SET gold = ? WHERE tg_id = ?', (int(gold) - int(quanity), user_id))

    def get_money_from_request_id(self, request_id):
        request = self.__db.db_read('SELECT quanity FROM request WHERE request_id = ?', (request_id, ))
        if len(request) > 0:
            return request[0][0]

    def add_money(self, user_id, request_id):
        request = self.__db.db_read('SELECT money FROM users WHERE tg_id = ?', (user_id, ))[0][0]
        self.__db.db_write('UPDATE users SET money = ? WHERE tg_id = ?', (int(request) + int(self.get_money_from_request_id(request_id)), user_id))

    def convert_money_to_gold(self, user_id):
        pay = self.__db.db_read('SELECT money, gold FROM users WHERE tg_id = ?', (user_id, ))[0]
        self.__db.db_write('UPDATE users SET money = 0, gold = ? WHERE tg_id = ?', (int(pay[0]) + int(round(100 / 66 * int(pay[1]), 2)), user_id))

    def get_gold(self, user_id):
        request = self.__db.db_read('SELECT gold FROM users WHERE tg_id = ?', (user_id, ))
        if len(request) > 0:
            return request[0][0]

    def del_request_by_request_id(self, request_id):
        self.__db.db_write(f'DELETE FROM request WHERE request_id = ?', (request_id, ))
