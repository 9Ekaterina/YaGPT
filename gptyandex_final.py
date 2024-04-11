import requests
from config import YATOKEN, FID, MAX_SESSIONS, MAX_TOKENS_IN_SESSION, MAX_MODEL_TOKENS, MAX_USERS, MAX_PROJECT_TOKENS
import sql_engine



# Выполняем запрос к YandexGPT
def ask_gpt(text, sys_text, geo_text):
    iam_token = f'{YATOKEN}'  # Токен для доступа к YandexGPT
    folder_id = f'{FID}'  # Folder_id для доступа к YandexGPT


    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",  # модель для генерации текста
        "completionOptions": {
            "stream": False,  # потоковая передача частично сгенерированного текста выключена
            "temperature": 0.6,  # чем выше значение этого параметра, тем более креативными будут ответы модели (0-1)
            "maxTokens": MAX_MODEL_TOKENS  # максимальное число сгенерированных токенов, очень важный параметр для экономии токенов
        },
        "messages": [
            {
                "role": "system",
                "text": sys_text
            }
            ,
            {
                "role": "assistant",
                "text": geo_text
            }
            ,
            {
                "role": "user",  # пользователь спрашивает у модели
                "text": text # передаём текст, на который модель будет отвечать
            }
        ]
    }

    # Выполняем запрос к YandexGPT
    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                             headers=headers,
                             json=data)
    # Проверяем, не произошла ли ошибка при запросе
    print (response.status_code)
    if response.status_code == 200:
                # достаём ответ YandexGPT
        text = response.json()["result"]["alternatives"][0]["message"]["text"]
        print(text)
        return text
    else:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {response.status_code}, {response.text}
            )
        )







