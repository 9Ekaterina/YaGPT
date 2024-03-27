import telebot
from config import TOKEN
import sql_engine
import gptyandex

# токен
bot = telebot.TeleBot(TOKEN)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]

# пишем обработку /start
@bot.message_handler(commands=['start'])
def start_user(message):
    bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}, я бот сочинитель\n"
                                           "Помогу помочь написать рассказ\n"
                                           "Чтобы ознакомиться с командами напиши /help\n")
    sql_engine.sql_start(message.from_user.id)


# пишем обработку /help
@bot.message_handler(commands=['help'])
def help_message(message):
    # кнопочки для выбора жанра
    button_1 = telebot.types.KeyboardButton("/genre")
    bot.send_message(message.chat.id, text="Для того что бы начать\n"
                                           "Жми на кнопочки и выбирай\n"
                                           "/genre - начать\n",
                     reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_1))



@bot.message_handler(commands=['genre'])
def genre (message):
    global command_type
    command_type = "genre"
    button_2 = telebot.types.KeyboardButton("Сказка")
    button_3 = telebot.types.KeyboardButton("Комедия")
    button_4 = telebot.types.KeyboardButton("Фантастика")
    button_5 = telebot.types.KeyboardButton("Ужастики")

    bot.send_message(message.chat.id, text="Вбери жанр рассказа:\n"
                                           "1)Сказка\n"
                                           "2)Комедия\n"
                                           "3)Фантастика\n"
                                           "4)Ужастики\n",
                     reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_2, button_3, button_4, button_5,))

@bot.message_handler(commands=['character'])
def character (message):
    global command_type
    command_type = "character"
    button_18 = telebot.types.KeyboardButton("Доктор Стрэндж")
    button_19 = telebot.types.KeyboardButton("Гермиона Грейнджер")
    button_20 = telebot.types.KeyboardButton("Юлий (Три Богатыря)")
    button_21 = telebot.types.KeyboardButton("Золушка")
    bot.send_message(message.chat.id, text="Выбери  персонажа:\n"
                                           "1) Доктор Стрэнж\n"
                                           "2) Гермиона Грейнджер\n"
                                           "3) Юлий (Три Богатыря)\n"
                                           "4) Золушка\n"
                                            "Только тихо, что бы никто не заметил, ты можешь написать персонажа которого нету в списке 🤫.Если что я тебе ничего не говорил)\n",

                     reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_18, button_19,button_20, button_21))


@bot.message_handler(commands=['setting'])
def setting (message):
    global command_type
    command_type = "setting"
    button_18 = telebot.types.KeyboardButton("В городе")
    button_19 = telebot.types.KeyboardButton("В волшебном лесу")
    button_20 = telebot.types.KeyboardButton("В заброшеном задинии")
    button_21 = telebot.types.KeyboardButton("В школе")
    bot.send_message(message.chat.id, text="Выбери сеттинг (локацию где будут главный герой нашего рассказа):\n"
                                           "1) В городе - герой будет гулять по городу...\n"
                                           "2) В волшебном лесу - герой попадет в волшебный лес\n"
                                           "3)В заброшенном здании - герой окажется в заброшенном здании\n"
                                           "4) В школе - наш герой захочет поучиться в школе \n"
                                            ,

                     reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_18, button_19,button_20, button_21))


@bot.message_handler(commands=['do_it'])
def do_it(message):
    user_genre = sql_engine.sql_select_data(message.from_user.id, 1)
    user_character = sql_engine.sql_select_data(message.from_user.id, 2)
    user_setting = sql_engine.sql_select_data(message.from_user.id, 3)
    bot.send_message(message.chat.id, f"Был выбран такой жанр: {user_genre}")
    bot.send_message(message.chat.id, f"Был выбран такого персонажа: {user_character}")
    bot.send_message(message.chat.id, f"Был выбран такой сеттинг: {user_setting}")
    user_request = (
        f"Ты просишь нейросеть сделать это:\n"
        f"Напиши текст на русском языке, в жанре {user_genre} с главным героем {user_character}, действие происходит {user_setting}.")
    bot.send_message(message.chat.id, f"{user_request}")
    bot.send_message(message.chat.id, text= "Если хочешь что-то исправить, жми  /genre (жанр), или /character (главный герой), или /setting (место действия)\n"
                                            "Но, если все ок, жми -> /solve_task\n"
                    )

    # записываем выбор в кэш
    sql_engine.sql_update(message.from_user.id, f"{user_genre}", f"{user_character}", f"{user_setting}", f"{user_request}", "")

# отправляем запрос в YandexGPt
@bot.message_handler(commands=['solve_task'])
def solve_task(message):
    bot.send_message(message.chat.id, "Ушёл думать...")

    # Изменить, когда будем работать с подсчётом токенов
    user_genre =  sql_engine.sql_select_data(message.from_user.id, 1)
    user_character = sql_engine.sql_select_data(message.from_user.id, 2)
    user_setting =  sql_engine.sql_select_data(message.from_user.id, 3)
    user_request = sql_engine.sql_select_data(message.from_user.id, 4)

    # Проверяем ответ на наличие ошибок и парсим его
    responseya = gptyandex.ask_gpt(user_request, user_genre, f"Главный герой {user_character}, место действия  {user_setting}")

    #if not response[0]:
     #   bot.send_message(message.chat.id, "Не удалось выполнить запрос...")

        # Выводим ответ или сообщение об ошибке
   # bot.send_message(message.chat.id, response[1])
    bot.send_message(message.chat.id, responseya)
    button_20 = telebot.types.KeyboardButton("/continue")
    button_21 = telebot.types.KeyboardButton("/end")
    bot.send_message(message.chat.id, "Хочешь продолжить?\n"
                     "Если хочешь продолжить жми -> /continue\n"
                     "Если хочешь завершить жми -> /end\n"
                     , reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_20, button_21))


    # записываем ответ данной в базу

    return

@bot.message_handler(content_types=CONTENT_TYPES)
def mess_engine(message):
    global  command_type
    # print(command_type)

    user_genre =  sql_engine.sql_select_data(message.from_user.id, 1)
    user_character = sql_engine.sql_select_data(message.from_user.id, 2)
    user_setting =  sql_engine.sql_select_data(message.from_user.id, 3)

    if message.content_type != ("text"):
        bot.send_message(message.chat.id, "Необходимо отправить именно текстовое сообщение")
        bot.send_message(message.chat.id,
                         f"Мы остановились на команде /{command_type}. Если решишь продолжжить, просто нажми на команду!")
        return mess_engine
    else:

        if command_type == ("genre"):
            bot.send_message(message.chat.id, "Сейчас мы обрабатываем текст для команды /genre")
            user_genre = message.text
            bot.send_message(message.chat.id, f"Был выбран такой жанр: {user_genre}")
            bot.send_message(message.chat.id, text="Если определился с жанрм, напиши команду /character")
            command_type = ""
            # записываем выбор в кэш
            sql_engine.sql_update(message.from_user.id, f"{user_genre}", "", "", "", "")
            #ОТЛАДКА: выводим в консоль то, что у нас сейчас есть по пользователю
            #sql_engine.sql_select_data(message.from_user.id,1)


        elif command_type == ("character"):
            bot.send_message(message.chat.id, "Сейчас мы обрабатываем текст для команды /character")
            user_character = message.text
            bot.send_message(message.chat.id, f"Был выбран такой жанр: {user_genre}")
            bot.send_message(message.chat.id, f"Был выбран такого персонажа: {user_character}")
            bot.send_message(message.chat.id, text="После того как выберешь персонажа напиши /setting")
            command_type = ""

            # записываем выбор в кэш
            sql_engine.sql_update(message.from_user.id, f"{user_genre}", f"{user_character}", "", "", "")
            # ОТЛАДКА: выводим в консоль то, что у нас сейчас есть по пользователю
            #sql_engine.sql_select_data(message.from_user.id, 2)

        elif command_type == ("setting"):
            bot.send_message(message.chat.id, "Сейчас мы обрабатываем текст для команды /setting")
            user_setting = message.text
            bot.send_message(message.chat.id, f"Был выбран такой жанр: {user_genre}")
            bot.send_message(message.chat.id, f"Был выбран такого персонажа: {user_character}")
            bot.send_message(message.chat.id, f"Был выбран такой сеттинг: {user_setting}")
            bot.send_message(message.chat.id, text="После того как выберешь ссетинг напиши /do_it")
            command_type = ""

            # записываем выбор в кэш
            sql_engine.sql_update(message.from_user.id, f"{user_genre}", f"{user_character}", f"{user_setting}", "", "")
            # ОТЛАДКА: выводим в консоль то, что у нас сейчас есть по пользователю
            # sql_engine.sql_select_data(message.from_user.id, 3)

        else:
            bot.send_message(message.chat.id, f"Я всегда не против просто поболтать. Буду попугаем: {message.text}")
            bot.send_message(message.chat.id, "Если решишь заставить нейросеть думать за тебя, командуй /genre")


bot.polling()