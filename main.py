#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import os
import platform
import telebot
from threading import Lock
from config_parser import ConfigParser
from backend import DbAct, TempUserData
from db import DB
from frontend import Bot_inline_btns
#####################################
config_name = 'secrets.json'
####################################################################

def broadcast_msg(user_id):
    if db_actions.get_user(user_id) is not None and db_actions.get_request_by_user_id(user_id) is not None:
        personal_data = db_actions.get_user(user_id)
        for admin in db_actions.get_admins():
            bot.send_message(admin, f'Новый пользователь!\nНикнейм: @{personal_data[0]}\nИмя: {personal_data[1]}\nФамилия: '
                                    f'{personal_data[2]}\nID Пользователя: {user_id}\nID обращения: '
                                    f'{db_actions.get_request_by_user_id(user_id)}\nПодтвердите верификацию '
                                    f'(/accept "ID обращения") или отклоните (/reject "ID обращения")')


def main():
    @bot.message_handler(commands=['start'])
    def start_msg(message):
        buttons = Bot_inline_btns()
        bot.send_message(message.chat.id, text='Для использования бота, Вам необходимо подписаться на каналы ниже⬇️',
                         reply_markup=buttons.start_btns())
        hello_msg(message, buttons)

    def hello_msg(message, buttons):
        bot.send_message(message.chat.id, text='▶Для продолжения выбери нужную команду на клавиатуре👇\n'
                                               '🙋‍♂️Если есть дополнительные вопросы по поводу бота, обратитесь в '
                                               'Тех.Поддержку\n'
                                               '📊Курс: 0.70', reply_markup=buttons.main_chat_btns())

    @bot.message_handler(content_types=['text'])
    def text(message):
        buttons = Bot_inline_btns()
        if message.text == '💰Пополнить':
            bot.send_message(message.chat.id, text='✏ Введите сумму для пополнения баланса в рублях',
                             reply_markup=buttons.replenish_btns())
        elif message.text == '🍯Купить голду':
            bot.send_message(message.chat.id, text='Ваш баланс:\n')
        elif message.text == '📨Вывод':
            bot.send_message(message.chat.id, text='❗️Вывод работает от 100G❗️\nСколько вы хотите вывести голды?',
                             reply_markup=buttons.withdrawal_btns())
        elif message.text == '😄Отзывы':
            bot.send_message(message.chat.id, text='https://t.me/AdviceOTZIVI')
        elif message.text == '📉Курс':
            bot.send_message(message.chat.id, text='✅Курс: 0.7 | 70₽ = 100G')
        elif message.text == '🔢Калькулятор':
            bot.send_message(message.chat.id, text='Выберите действие⤵️', reply_markup=buttons.calculator_btns())
        elif message.text == '✨Посчитать рубли в голде':
            bot.send_message(message.chat.id, text='✍️Введите сумму (в RUB)')
        elif message.text == '✨Посчитать голду в рублях':
            bot.send_message(message.chat.id, text='✍️Введите сумму (в голде)')
        elif message.text == '🏠Главное меню':
            hello_msg(message, buttons)
        elif message.text == '👨‍💻Поддержка':
            bot.send_message(message.chat.id, text='https://t.me/YT_ADVICE')
        elif message.text == '🤖Профиль':
            bot.send_message(message.chat.id, text=f'📋Информация о {message.from_user.first_name}\n💸Денег: 0 '
                                                   f'руб\n🍯Золото: 0 G')

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
