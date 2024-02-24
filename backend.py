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
            self.__user_data.update({user_id: [None]})
        return self.__user_data


class DbAct:
    def __init__(self, db, config):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config

    def add_user(self, user_id, config_admins):
        if user_id in config_admins:
            role = True
        else:
            role = None
        self.__db.db_write('INSERT OR IGNORE INTO users (tg_id, money, gold, role) VALUES (?, ?, ?, ?)', (user_id, 0, 0, role))
