import telebot
import random
import datetime

TOKEN = "6846258813:AAG0z1DljUItnOCy68niTvNoWOauDRhgswI"

bot = telebot.TeleBot(TOKEN)

films1 = (("Мужчина к Новому году (Фильм 2023)", "https://www.ivi.ru/watch/muzhchina-k-novomu-godu"),
         ("Прямо перед глазами (Фильм 2021)","https://www.ivi.ru/watch/526053"),
         ("Он – дракон (Фильм 2015)", "https://www.ivi.ru/watch/133915"),
         ("Тайный санта (фильм 2022)","https://www.ivi.ru/watch/488068"),
         ("Во власти стихии (Фильм 2018)","https://www.ivi.ru/watch/186733"))

users1 = {}
class UserState(telebot.handler_backends.StatesGroup):
    change_timezone = telebot.handler_backends.State()
    chose = telebot.handler_backends.State()


@bot.message_handler(commands=["start", "Start"])
def welcome_message(message: telebot.types.Message):

    # time_check(message.chat.id)

    welcome = "Привет!\nХотите ли вы, чтобы я приветствовал вас относительно вашего времени ?"
    keyboard = telebot.util.quick_markup(

        {
            "Да": {"callback_data": "time_hello_yes"},
            "Нет": {"callback_data": "time_hello_no"}
        }

    )

    bot.send_message(message.chat.id, welcome, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == "time_hello_yes")
def time_hello_yes(callback: telebot.types.CallbackQuery):

    # time_check(callback.from_user.id)

    timezone_msk = telebot.util.quick_markup(

        {

            "-1 к мск": {"callback_data": "-1 к мск"},
            "+0 к мск": {"callback_data": "+0 к мск"},
            "+1 к мск": {"callback_data": "+1 к мск"},
            "+2 к мск": {"callback_data": "+2 к мск"},
            "+3 к мск": {"callback_data": "+3 к мск"},
            "+4 к мск": {"callback_data": "+4 к мск"},
            "+5 к мск": {"callback_data": "+5 к мск"},
            "+6 к мск": {"callback_data": "+6 к мск"},
            "+7 к мск": {"callback_data": "+7 к мск"},
            "+8 к мск": {"callback_data": "+8 к мск"},
            "+9 к мск": {"callback_data": "+9 к мск"}

        }

    )

    bot.send_message(callback.from_user.id, "Выберите свой часовой пояс относительно мск\n( вы всегда сможете его поменять )", reply_markup=timezone_msk)


@bot.callback_query_handler(func=lambda callback: callback.data in ["-1 к мск", "+0 к мск", "+1 к мск", "+2 к мск", "+3 к мск", "+4 к мск", "+5 к мск", "+6 к мск", "+7 к мск", "+8 к мск", "+9 к мск"])
def take_timezone(callback: telebot.types.CallbackQuery):

    # time_check(callback.from_user.id)

    with open("users_timezone.txt", "w") as file:
        file.write(callback.data[0:2])

    mainkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    mainkeyboard.add(telebot.types.KeyboardButton("Крестики нолики"))
    mainkeyboard.add(telebot.types.KeyboardButton("Подборка фильмов"))
    mainkeyboard.add(telebot.types.KeyboardButton("Поменять время относительно мск"))

    bot.send_message(callback.from_user.id, "Отлично!", reply_markup=mainkeyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == "time_hello_no")
def time_hello_no(callback: telebot.types.CallbackQuery):

    # time_check(callback.from_user.id)

    mainkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    mainkeyboard.add(telebot.types.KeyboardButton("Крестики нолики"))
    mainkeyboard.add(telebot.types.KeyboardButton("Подборка фильмов"))
    mainkeyboard.add(telebot.types.KeyboardButton("Установить время относительно мск"))

    bot.send_message(callback.from_user.id, "Окей. Но если передумаете - "
                                            "в будущем вы в любом случае выбрать эту функцию в главном меню "
                                            "и ввести свой часовой пояс относительно мск.", reply_markup=mainkeyboard)


@bot.message_handler(func=lambda x: x.text in ["Поменять время относительно мск", "Установить время относительно мск"])
def change_timezone(message: telebot.types.Message):

    # time_check(message.chat.id)

    bot.set_state(message.from_user.id, UserState.change_timezone, message.chat.id)

    secondkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    secondkeyboard.add(telebot.types.KeyboardButton("Меню"))

    bot.send_message(message.chat.id, "Введите ваше новое время относительно мск\n\n"
                                      "Пример:\n\n+5 - если у вас +5 от мск\n\n"
                                      "-5 - если у вас -5 от мск\n\n"
                                      "0 - если вы живете по мск времени:", reply_markup=secondkeyboard)


@bot.message_handler(state=UserState.change_timezone)
def change_timezone(message: telebot.types.Message):
    # time_check(message.chat.id)

    if message.text in ["-1","0","+1","+2","+3","+4","+5","+6","+7","+8","+9"]:
        with open("users_timezone.txt", "w") as file:
            file.write(str(message.text))
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Вы успешно изменили время!")



    elif message.text == "Меню":
        main_menu(message)

    else:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Вы ввели неверное значение.\n\n Повторите команду повторно")

@bot.message_handler(func=lambda x: x.text == "Подборка фильмов")
def films(message: telebot.types.Message):
    # time_check(message.chat.id)

    text = ""
    k = 0
    for i in range(0,5):

        a = random.randint(0, 4)

        if k == 0:
            text += (films1[a])[0] + " - " + (films1[a])[1] + "\n\n"
            k = 1

        text += (films1[a])[0] + "\n\n"

    k = 0

    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda x: x.text == "Меню")
def main_menu(message: telebot.types.Message):
    # time_check(message.chat.id)

    mainkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    mainkeyboard.add(telebot.types.KeyboardButton("Крестики нолики"))
    mainkeyboard.add(telebot.types.KeyboardButton("Подборка фильмов"))
    mainkeyboard.add(telebot.types.KeyboardButton("Поменять время относительно мск"))

    bot.send_message(message.chat.id, "Переход в главное меню", reply_markup=mainkeyboard)

# def time_check(id):
#
#     time = datetime.datetime.now()
#     time = time.hour
#
#     with open("users_messages_time.txt", "a+") as file:
#         file.write(str(id) + " " + str(time) + "\n")
#
#     with open("users_messages_time.txt", "r") as file:
#         schit = file.readlines()
#         print(schit)
#         nach = len(schit) - 1
#
#         i = 0
#
#         while i != 8:

@bot.message_handler(func=lambda x: x.text == "Крестики нолики")
def krestiki_noliki(message):
    bot.set_state(message.from_user.id, UserState.chose, message.chat.id)
    bot.send_message(message.chat.id, "Кем вы будете ходить? Крестики/Нолики")

@bot.message_handler(state = UserState.chose)
def game(message):

    if message.text.lower() == "крестики":
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Отлично! Вы играете крестиками")
        gamekeyboard = telebot.util.quick_markup({

            "1" : {"callback_data" : "1"},
            "2" : {"callback_data" : "2"},
            "3" : {"callback_data" : "3"},
            "4" : {"callback_data" : "4"},
            "5" : {"callback_data" : "5"},
            "6" : {"callback_data" : "6"},
            "7" : {"callback_data" : "7"},
            "8" : {"callback_data" : "8"},
            "9" : {"callback_data" : "9"},

        }, row_width=3)

        bot.send_message(message.chat.id, ".",reply_markup=gamekeyboard)
    elif message.text.lower() == "нолики":
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, "Отлично! Вы играете ноликами.")

        def get_keyboard(n):
            markup = telebot.types.InlineKeyboardMarkup(row_width=n)
            buttons = [
                telebot.types.InlineKeyboardButton(text=' ', {'callback_data': i})
                for i in range(1, n ** 2 + 1)
            ]
            markup.add(*buttons)
            return markup

        gamekeyboard = get_keyboard(3)

        bot.send_message(message.chat.id, "..", reply_markup=gamekeyboard)



bot.add_custom_filter(telebot.custom_filters.StateFilter(bot))
bot.infinity_polling()
