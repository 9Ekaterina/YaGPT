import sqlite3
import requests
from datetime import datetime, date, time
from config import DATABASE, MAX_USERS, YATOKEN, MAX_MODEL_TOKENS, FID, MAX_TOKENS_IN_SESSION

print(datetime.now())

#Когда пользователь даёт команду /start проверяем и если нет, создаём базу
def sql_start(user_id_session):
    con = sqlite3.connect(DATABASE, check_same_thread=False)

    # Подключаем sqlite3.Row
    con.row_factory = sqlite3.Row


    # Создаём специальный объект cursor для работы с БД
    # Вся дальнейшая работа будет вестись через методы этого объекта: cur
    cur = con.cursor()

    # ЗДЕСЬ БУДЕТ ПРОИСХОДИТЬ САМА РАБОТА С БАЗОЙ: ОТПРАВКА ЗАПРОСОВ, ПОЛУЧЕНИЕ ОТВЕТОВ
    # Готовим SQL-запрос
    # Для читаемости запрос обрамлён в тройные кавычки и разбит построчно
    query = '''
    CREATE TABLE IF NOT EXISTS prompts(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        role TEXT,
        content TEXT,
        date DATATIME,
        tokens INTEGER,
        session_id INTEGER
        );
            '''
    cur.execute(query)
    con.commit()

    # Создаём специальный объект cursor для работы с БД
    # Вся дальнейшая работа будет вестись через методы этого объекта: cur
    cur = con.cursor()

    # ЗДЕСЬ БУДЕТ ПРОИСХОДИТЬ САМА РАБОТА С БАЗОЙ: ОТПРАВКА ЗАПРОСОВ, ПОЛУЧЕНИЕ ОТВЕТОВ
    # Готовим SQL-запрос
    # Для читаемости запрос обрамлён в тройные кавычки и разбит построчно
    query = '''
    CREATE TABLE IF NOT EXISTS user_sessions(
        user_id INTEGER PRIMARY KEY,
        genre TEXT,
        character TEXT,
        setting TEXT,
        user_text TEXT,
        gpt_responce TEXT
    );
    '''
    cur.execute(query)
    con.commit()

# Записываем значения в таблицу user_session
    cur = con.cursor()
    query = f'SELECT user_id FROM user_sessions WHERE user_id = {user_id_session}'
    print(query)
    results = cur.execute(query).fetchone()
    if results is None:
        query = f"INSERT INTO user_sessions VALUES ({user_id_session},NULL,NULL,NULL,NULL,NULL)"
        con.execute(query)
        print(query)
        con.commit()
        #ОТЛАДКА: сообщаем, что такого пользователя нет
        print("Такого пользователя нет")
    else:
        #ОТЛАДКА: сообщаем, что такая сессия уже есть в кэше
        print('Эта сессия уже есть')

    con.close()


#Update для кэша
def sql_update(user_id_session,genre,character,setting,user_text,gpt_responce):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cur = con.cursor()
    query = f'''
                  UPDATE user_sessions SET genre = "{str(genre)}", character="{str(character)}", setting="{str(setting)}", user_text="{str(user_text)}" WHERE user_id = {user_id_session};
               '''
    print(query)
    cur.execute(query)
    con.commit()

    con.close()


def sql_insert_data_prompts (user_id_session, role, content, tokens, session_id):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cur = con.cursor()
    now_data = datetime.now()
    query = f'''
                      INSERT INTO prompts VALUES (NULL, {user_id_session}, "{role}", "{content}", "{now_data}", "{tokens}", "{session_id}")
                   '''
    cur.execute(query)
    con.commit()
    con.close()
    #sql_select_data_prompts()







#Функция: подсчёт количества пользователей
def is_limit_users():
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cursor = con.cursor()
    result = cursor.execute('SELECT DISTINCT user_id FROM prompts')
    count = 0  # количество пользователей
    for i in result:  # считаем количество полученных строк
        count += 1  # одна строка == один пользователь
    con.close()
    return count >= MAX_USERS

#ОТЛАДКА: Лимит пользователей превышен?
    print(is_limit_users())

# функция подсчета сессий
def max_users_session(user_id_session):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cursor = con.cursor()
    query = f"SELECT session_id FROM prompts WHERE user_id = {user_id_session} ORDER BY date DESC LIMIT 1"

    result = cursor.execute(query).fetchall()
    #ОТЛАДКА: печать максимального номера сессии пользователя
    #print(result[0][0])
    con.close()
    result = result[0][0]
    return result

# функция подсчета токенов
def max_users_tocens(user_id_session):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cursor = con.cursor()
    query = f"SELECT DISTINCT tokens FROM  prompts where user_id = {user_id_session} ORDER BY date DESC LIMIT 1"
    tokens = cursor.execute(query).fetchall()
    #ОТЛАДКА: печать максимального номера сессии пользователя
    #print(result[0][0])
    con.close()
    tokens = tokens[0][0]
    return tokens


def  continue_responseya (user_id_session):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cursor = con.cursor()
    query = f'SELECT gpt_responce FROM user_sessions WHERE user_id = {user_id_session}'
    results = cursor.execute(query).fetchone()
    con.close()


def select_data_prompts (user_id_session):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cur = con.cursor()
    query = f'''
                     SELECT content FROM prompts WHERE user_id ={user_id_session} and role = "assistant_prompt" ORDER BY date LIMIT 1
                   '''
    result = cur.execute(query).fetchone()
    result = result[0]
    con.close()
    return result



def genre_read (user_id_session):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cursor = con.cursor()
    query = f'SELECT content FROM prompts WHERE user_id = {user_id_session} and role = "system_prompt" ORDER BY date DESC LIMIT 1'
    result= cursor.execute(query).fetchone()
    result = result[0]
    con.close()
    return result


#Функция: подсчёт количества токенов в тексте от пользоватея
def count_tokens(text):
    headers = {
        'Authorization': f'Bearer {YATOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{FID}/yandexgpt/latest",
        "maxTokens": MAX_MODEL_TOKENS,
        "text": text
    }
    return len(
        requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
            json=data,
            headers=headers
        ).json()['tokens']
    )  # здесь, после выполнения запроса, функция возвращает количество токенов в text

    #ОТЛАДКА: сколько токенов в запросе пользователя
    print(count_tokens("сюда будем передавать запрос пользователя"))


"""
# Функция получает идентификатор пользователя, чата и самого бота, чтобы иметь возможность отправлять сообщения
def is_tokens_limit(user_id, chat_id, bot):
    if count_tokens >= MAX_TOKENS_IN_SESSION:

        bot.send_message(chat_id,
              f'Вы израсходовали все токены в этой сессии. Вы можете начать новую, введя help_with')

    elif count_tokens() + 50 >= MAX_TOKENS_IN_SESSION:# Если осталось меньше 50 токенов
          bot.send_message(
              chat_id,
              f'Вы приближаетесь к лимиту в {MAX_TOKENS_IN_SESSION} токенов в этой сессии. '
              f'Ваш запрос содержит суммарно {count_tokens()} токенов.')

    elif count_tokens() / 2 >= MAX_TOKENS_IN_SESSION: # Если осталось меньше половины
          bot.send_message(
              chat_id,
              f'Вы использовали больше половины токенов в этой сессии. '
              f'Ваш запрос содержит суммарно {count_tokens} токенов.'
          )


"""

#ОТЛАДКА: просто выводим на экран то, что по пользователю есть в кэше в данный момент
def sql_select_data(user_id_session, param):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cur = con.cursor()
    query = f'SELECT * FROM user_sessions WHERE user_id = {user_id_session}'
    results = cur.execute(query).fetchone()
    print (results)
    print(results[param])
    con.close()
    return results[param]

"""
def session_select (user_id_session, session):
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cur = con.cursor()
    query = f"SELECT session_id FROM prompts WHERE user_id = {user_id_session}"
    results = cur.execute(query).fetchone()
    print(results)
    con.close()
"""

#ОТЛАДКА:
def sql_select_data_prompts():
    con = sqlite3.connect(DATABASE, check_same_thread=False)
    cur = con.cursor()
    query = f'SELECT * FROM prompts'
    results = cur.execute(query).fetchone()
    print (results)
    con.close()
    return

#sql_select_data_prompts()


