import sqlite3
import requests
from config import DATABASE

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
        date TEXT,
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
