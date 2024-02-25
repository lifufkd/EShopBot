#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import os
import platform
import random
import telebot
from threading import Lock
from config_parser import ConfigParser
from backend import DbAct, TempUserData
from db import DB
from frontend import Bot_inline_btns
#####################################
config_name = 'secrets.json'
####################################################################


def hello_msg(message, buttons):
    bot.send_message(message.chat.id, text='▶Для продолжения выбери нужную команду на клавиатуре👇\n'
                                           '🙋‍♂️Если есть дополнительные вопросы по поводу бота, обратитесь в '
                                           'Тех.Поддержку\n'
                                           '📊Курс: 0.66', reply_markup=buttons.main_chat_btns())


def broadcast_msg(user_id, type, money, msg_id=None):
    buttons = Bot_inline_btns()
    type_msg = {False: f'Запрос на пополнение баланса на сумму {money}', True: f'Запрос на вывод голды на сумму {money}'}
    if db_actions.get_request_by_user_id(user_id, type) is not None:
        personal_data = db_actions.get_user(user_id)
        admins = db_actions.get_admins()
        if not type:
            for admin in admins:
                bot.send_message(admin, f'{type_msg[type]}\nНикнейм: @{personal_data[0]}\nИмя: {personal_data[1]}\nФамилия: '
                                        f'{personal_data[2]}\nID Пользователя: {user_id}\nID обращения: '
                                        f'{db_actions.get_request_by_user_id(user_id, type)}\nПодтвердите верификацию ',
                                 reply_markup=buttons.accept_deny_btns(db_actions.get_request_by_user_id(user_id, type)))
                bot.forward_message(chat_id=admin, from_chat_id=user_id, message_id=msg_id)
        else:
            random_admin = random.choice(list(admins))
            db_actions.update_dialog_status(random_admin, db_actions.get_request_by_user_id(user_id, type))
            bot.send_message(random_admin,
                             f'{type_msg[type]}\nНикнейм: @{personal_data[0]}\nИмя: {personal_data[1]}\nФамилия: '
                             f'{personal_data[2]}\nID Пользователя: {user_id}\nID обращения: '
                             f'{db_actions.get_request_by_user_id(user_id, type)}\nПодтвердите верификацию ',
                             reply_markup=buttons.end_chat())

def main():
    @bot.message_handler(commands=['start'])
    def start_msg(message):
        buttons = Bot_inline_btns()
        user_id = message.chat.id
        db_actions.add_user(user_id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
        bot.send_message(message.chat.id, text='Для использования бота, Вам необходимо подписаться на каналы ниже⬇️',
                         reply_markup=buttons.start_btns())
        hello_msg(message, buttons)

    @bot.message_handler(content_types=['text', 'photo'])
    def text(message):
        user_id = message.chat.id
        if db_actions.user_is_existed(user_id):
            buttons = Bot_inline_btns()
            code = temp_user_data.temp_data(user_id)[user_id][0]
            if code is not None:
                if code == 0:
                    try:
                        bot.send_message(message.chat.id, text=f'📩Отправьте деньги на Сбербанк по реквизитам:\n'
                                                               f'79889676131 Сбербанк❤‍🩹\n'
                                                               f'5228600516931674 Сбербанк✌\n'
                                                               f'Получатель:Сергей Е.\n'
                                                               f'На ☕ тоже можно скинуть😉\n'
                                                               f'💲Сумма: {int(message.text)}₽\n'
                                                               f'📷Отправьте нам скриншот чека.')
                        temp_user_data.temp_data(user_id)[user_id][1] = int(message.text)
                        temp_user_data.temp_data(user_id)[user_id][0] = 1
                    except:
                        temp_user_data.temp_data(user_id)[user_id][0] = None
                        bot.send_message(message.chat.id, '❌Введена неверная сумма❌')
                elif code == 1:
                    db_actions.add_request(user_id, temp_user_data.temp_data(user_id)[user_id][1], False)
                    broadcast_msg(user_id, False, temp_user_data.temp_data(user_id)[user_id][1], message.id)
                    temp_user_data.temp_data(user_id)[user_id][0] = None
                elif code == 2:
                    try:
                        if 100 < int(message.text) <= int(db_actions.get_gold(user_id)):
                            db_actions.add_request(user_id, int(message.text), True)
                            broadcast_msg(user_id, True, int(message.text))
                        else:
                            raise
                    except:
                        bot.send_message(message.chat.id, '❌Введена неверная сумма❌')
                    finally:
                        temp_user_data.temp_data(user_id)[user_id][0] = None
            else:
                if db_actions.get_dialog_status_client(user_id):
                    admin_id = db_actions.get_admin_id_from_request_id(user_id, True)
                    bot.forward_message(chat_id=admin_id, from_chat_id=user_id, message_id=message.id)
                elif message.text == '💰Пополнить':
                    if db_actions.get_request_by_user_id(user_id, False) is None:
                        bot.send_message(message.chat.id, text='✏ Введите сумму для пополнения баланса в рублях',
                                         reply_markup=buttons.replenish_btns())
                        temp_user_data.temp_data(user_id)[user_id][0] = 0
                    else:
                        bot.send_message(message.chat.id, text='✅Заявка уже создана✅')
                elif message.text == '🍯Купить голду':
                    bot.send_message(message.chat.id, text='Ваш баланс:\n')
                elif message.text == '📨Вывод':
                    if db_actions.get_request_by_user_id(user_id, True) is None:
                        bot.send_message(message.chat.id,
                                         text='❗️Вывод работает от 100G❗️\nСколько вы хотите вывести голды?',
                                         reply_markup=buttons.withdrawal_btns())
                        temp_user_data.temp_data(user_id)[user_id][0] = 2
                    else:
                        bot.send_message(message.chat.id, text='✅Заявка уже создана✅')
                elif message.text == '😄Отзывы':
                    bot.send_message(message.chat.id, text='https://t.me/AdviceOTZIVI')
                elif message.text == '📉Курс':
                    bot.send_message(message.chat.id, text='✅Курс: 0.66 | 66₽ = 100G')
                elif message.text == '🔢Калькулятор':
                    bot.send_message(message.chat.id, text='Выберите действие⤵️',
                                     reply_markup=buttons.calculator_btns())
                elif message.text == '✨Посчитать рубли в голде':
                    bot.send_message(message.chat.id, text='✍️Введите сумму (в ₽)')
                elif message.text == '✨Посчитать голду в рублях':
                    bot.send_message(message.chat.id, text='✍️Введите сумму (в G)')
                elif message.text == '🏠Главное меню':
                    hello_msg(message, buttons)
                elif message.text == '👨‍💻Поддержка':
                    bot.send_message(message.chat.id, text='https://t.me/YT_ADVICE')
                elif message.text == '🤖Профиль':
                    bot.send_message(message.chat.id, text=f'📋Информация о {message.from_user.first_name}\n💸Денег: 0₽ '
                                                           f'руб\n🍯Золото: 0G')
                elif user_id in db_actions.get_admins():
                    candidate_id = db_actions.get_request_by_request_id(message.text[8:])
                    if candidate_id is not None:
                        if message.text[:7] == '✅accept':
                            db_actions.add_money(candidate_id, message.text[8:])
                            db_actions.convert_money_to_gold(candidate_id)
                            bot.send_message(candidate_id, '✅Заявка одобрена, баланс пополнен!✅')
                        elif message.text[:7] == '❌reject':
                            bot.send_message(candidate_id, '❌Заявка отклонена, чек неверный❌')
                        db_actions.del_request_by_request_id(message.text[8:])
                    elif db_actions.get_dialog_status(user_id) is not None:
                        client_id = db_actions.get_request_by_request_id(db_actions.get_dialog_status(user_id))
                        if message.text == "✅Закончить чат":
                            db_actions.del_request_by_request_id(db_actions.get_dialog_status(user_id))
                            db_actions.update_dialog_status(user_id, None)
                            db_actions.update_dialog_open(client_id, False)
                            bot.send_message(client_id, '❌Чат завершён❌')
                            bot.send_message(user_id, '❌Чат завершён❌')
                        else:
                            bot.forward_message(chat_id=client_id, from_chat_id=user_id, message_id=message.id)
                    else:
                        bot.send_message(user_id, '❌Нет доступных действий❌')

        else:
            bot.send_message(user_id, 'Введите /start для запуска бота')


    bot.polling(none_stop=True)


if '__main__' == __name__:
    os_type = platform.system()
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}', os_type)
    db = DB(f'{work_dir}/{config.get_config()["db_file_name"]}', Lock(), config.get_config())
    temp_user_data = TempUserData()
    db_actions = DbAct(db, config.get_config())
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
