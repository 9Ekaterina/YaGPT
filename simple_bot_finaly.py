# имотрируем нужные библиотеки и файлы
import telebot
from config import TOKEN, MAX_SESSIONS, MAX_TOKENS_IN_SESSION, MAX_MODEL_TOKENS
import sql_engine
import gptyandex


command_type = ""

# токен
bot = telebot.TeleBot(TOKEN)


# параметры для проверки на водд пользователя
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
    #запускаем функцию которая создает таблицу
    sql_engine.sql_start(message.from_user.id)


    #проверка на количество пользователей, доступных для одновременной работы с ботом
    # если оно привышает то мы говорим пользователю что тон не может сейчас пользоваться ботом и говорим что это бот попугай
    if sql_engine.is_limit_users() is True:
        bot.send_message(message.chat.id,"Прости, слишком много пользователей. Пока могу быть только ботом-попугаем")

        @bot.message_handler(content_types=['text'])
        def repeat_message(message):  # Функция для обработки сообщений
            bot.send_message(message.chat.id, message.text)  # Отправка ответ

    # Иначе если пользователь может пользоваться то мы начинаем работу с ботом
    elif sql_engine.is_limit_users() is not True:
        # записываем в БД
        #sql_engine.sql_insert_data_prompts(message.from_user.id, "", "", "", "")

        #current_session = sql_engine.max_users_session(message.from_user.id, "")


        current_session = sql_engine.max_users_session(message.from_user.id)
        if current_session > MAX_SESSIONS and current_session == 0:
                bot.send_message(message.chat.id, "Вы привысили количество допустимых сессий")

                @bot.message_handler(content_types=['text'])
                def repeat_message(message):  # Функция для обработки сообщений
                    bot.send_message(message.chat.id, message.text)  # Отправка ответ


        else:
            bot.send_message(message.chat.id, f"У тебя потрачено {MAX_SESSIONS - current_session} сессий")


        


            tokens = sql_engine.max_users_tocens(message.from_user.id)
            print(tokens)
            #считаем токены

            if tokens > MAX_TOKENS_IN_SESSION:
                    bot.send_message(message.chat.id, "ВЫ привысили количесво токенов")
            else:
                tokens_spend = MAX_TOKENS_IN_SESSION - tokens
                current_session = sql_engine.max_users_session(message.from_user.id)


                if tokens_spend / 2 < MAX_MODEL_TOKENS:
                        bot.send_message(message.chat.id,
                                         "Прости но токенов осталось мало тебе не хватит их на еще одну сессию")
                if tokens_spend > MAX_MODEL_TOKENS:
                        bot.send_message(message.chat.id, "Ты можешь начать еще одну сессию")



            # пишем обработку /help
                @bot.message_handler(commands=['help'])

                def help_message(message):
                                    # кнопочки для выбора жанра
                                button_1 = telebot.types.KeyboardButton("/genre")
                                bot.send_message(message.chat.id, text="Для того что бы начать\n"
                                                                               "Жми на кнопочки и выбирай\n"
                                                                               "/genre - начать\n",
                                                         reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_1))
                                #sql_engine.max_users_session(message.from_user.id)



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
                                                                                "Только тихо, что бы никто не заметил, ты можешь написать персонажа которого нету в списке 🤫.Если что, я тебе ничего не говорил)\n",

                                                         reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_18, button_19,button_20, button_21))


                @bot.message_handler(commands=['setting'])
                def setting (message):

                                global command_type
                                command_type = "setting"
                                button_18 = telebot.types.KeyboardButton("В городе")
                                button_19 = telebot.types.KeyboardButton("В волшебном лесу")
                                button_20 = telebot.types.KeyboardButton("В заброшеном здании")
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
                                            f"Напиши текст на русском языке, в жанре {user_genre} с главным героем {user_character}, действие происходит {user_setting}.")
                                bot.send_message(message.chat.id, f"{user_request}")
                                bot.send_message(message.chat.id, text= "Если хочешь что-то исправить, жми  /genre (жанр), или /character (главный герой), или /setting (место действия)\n"
                                                                                "Но, если все ок, жми -> /solve_task\n"
                                                        )

                                        # записываем выбор в кэш
                                sql_engine.sql_update(message.from_user.id, f"{user_genre}", f"{user_character}", f"{user_setting}", f"{user_request}", "")



                                # отправляем запрос в YandexGPt
                @bot.message_handler(commands=['solve_task'])
                def solve_task(message, session_id=None):
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
                                responseya  = responseya.replace ('"', ':')
                                responseya = responseya.replace("'", ":")
                                user_prompt = f"Главный герой {user_character}, место действия  {user_setting}"

                                sql_engine.sql_insert_data_prompts(message.from_user.id, "assistant_prompt", responseya, sql_engine.count_tokens(responseya) + sql_engine.count_tokens(user_prompt) + sql_engine.count_tokens(user_genre), 1 )

                                return

                @bot.message_handler(commands=['continue'])
                def continue_text(message):
                            bot.send_message(message.chat.id, "Как скажешь, будем продолжать\n"
                                                              "Отправил запрос в нейросеть. Жди...\n")

                            global user_genre, user_prompt
                            # Направляю запрос в нейросеть
                            system_prompt = sql_engine.genre_read(message.from_user.id)
                            print(system_prompt)
                            geo_text =  sql_engine.select_data_prompts(message.from_user.id)
                            print(geo_text)



                            responseya_con= gptyandex.ask_gpt("Продолжи", system_prompt, geo_text )
                            bot.send_message(message.chat.id, responseya_con)


                            sql_engine.sql_insert_data_prompts(message.from_user.id, "assistant_prompt", f"{ responseya_con}", "", current_session)




                                # команда конец
                @bot.message_handler(commands=['end'])
                def end (message):
                                bot.send_message(message.chat.id, "Окей, продолжать не будем\n"
                                                 "Если захочешь еще раз что-то спросить, жми -> /genre\n"
                                                 "А пока я бот-попугай\n")

                                current_session = sql_engine.max_users_session(message.from_user.id)
                                current_session += 1
                                print(current_session)

                                sql_engine.sql_insert_data_prompts(message.from_user.id, "system_prompt", "", "", current_session)
                                if current_session == 2:
                                    bot.send_message(message.chat.id, f"У тебя осталось {tokens_spend - tokens} токенов ")

                @bot.message_handler(content_types=CONTENT_TYPES)
                def mess_engine(message):
                                global  command_type, user_genre
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
                                        # записываем промпт жанра в базу
                                        sql_engine.sql_insert_data_prompts(message.from_user.id, "system_prompt", user_genre, sql_engine.count_tokens(user_genre), 1)


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
                                        bot.send_message(message.chat.id, text="После того как выберешь сеттиг напиши /do_it")
                                        command_type = ""

                                                # записываем выбор в кэш
                                        sql_engine.sql_update(message.from_user.id, f"{user_genre}", f"{user_character}", f"{user_setting}", "", "")
                                                # ОТЛАДКА: выводим в консоль то, что у нас сейчас есть по пользователю
                                        # sql_engine.sql_select_data(message.from_user.id, 3)

                                        # пишем пользовательский промпт в базу
                                        user_prompt = f"Главный герой {user_character}, место действия  {user_setting}"
                                        sql_engine.sql_insert_data_prompts(message.from_user.id, "user_prompt", user_prompt,  sql_engine.count_tokens(user_prompt) + sql_engine.count_tokens(user_genre), 1)

                                    else:
                                        bot.send_message(message.chat.id, f"Я всегда не против просто поболтать. Буду попугаем: {message.text}")
                                        bot.send_message(message.chat.id, "Если решишь заставить нейросеть думать за тебя, командуй /genre")


bot.polling()