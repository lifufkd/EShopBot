#####################################
#            Created by             #
#                SBR                #
#               zzsxd               #
#####################################
import telebot
from frontend import Bot_inline_btns

#####################################
tg_api = '6628019426:AAEuM4jtTC0xvdZ8bbk6bwOOxQqkNBzxngQ'
bot = telebot.TeleBot(tg_api)
from frontend import Bot_inline_btns


####################################################################


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
            bot.send_message(message.chat.id, text='Сколько вы хотите вывести голды?',
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
            bot.send_message(message.chat.id, text='✍️ Введите сумму (в голде)')
        elif message.text == '🏠Главное меню':
            hello_msg(message, buttons)
        elif message.text == '👨‍💻Поддержка':
            bot.send_message(message.chat.id, text='https://t.me/YT_ADVICE')
        elif message.text == '🤖Профиль':
            bot.send_message(message.chat.id, text=f'📋Информация о {message.from_user.first_name}\n💸Денег: 0 '
                                                   f'руб\n🍯Золото: 0 G')

    bot.polling(none_stop=True)


if '__main__' == __name__:
    main()
