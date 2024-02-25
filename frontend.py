#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import telebot
from telebot import types


#####################################

class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=1)

    def start_btns(self):
        subscribe = types.InlineKeyboardButton('➕Подписаться', url='https://t.me/AdviceOTZIVI')
        self.__markup.add(subscribe)
        return self.__markup

    def main_chat_btns(self):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            replenish = types.KeyboardButton(text="💰Пополнить")
            withdrawal = types.KeyboardButton(text="📨Вывод")
            reviews = types.KeyboardButton(text="😄Отзывы")
            course = types.KeyboardButton(text="📉Курс")
            calculator = types.KeyboardButton(text="🔢Калькулятор")
            support = types.KeyboardButton(text="👨‍💻Поддержка")
            profile = types.KeyboardButton(text="🤖Профиль")
            keyboard.add(replenish, withdrawal, reviews, course, calculator, support, profile)
            return keyboard
    def calculator_btns(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rub_to_gold = types.KeyboardButton(text="✨Посчитать рубли в голде")
        gold_to_rub = types.KeyboardButton(text="✨Посчитать голду в рублях")
        main_menu = types.KeyboardButton(text="🏠Главное меню")
        keyboard.add(rub_to_gold, gold_to_rub, main_menu, row_width=2)
        return keyboard

    def replenish_btns(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_menu = types.KeyboardButton(text="🏠Главное меню")
        keyboard.add(main_menu)
        return keyboard

    def withdrawal_btns(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        main_menu = types.KeyboardButton(text="🏠Главное меню")
        keyboard.add(main_menu)
        return keyboard

    def accept_deny_btns(self, id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        accept = types.KeyboardButton(f'✅Подтвердить платеж {id}')
        deny = types.KeyboardButton(f'❌Отклонить платеж {id}')
        keyboard.add(accept, deny)
        return keyboard
