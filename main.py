import requests

# Выполняем запрос к YandexGPT
def ask_gpt(text, sys_text, geo_text):
    iam_token = 't1.9euelZqczZPHkYmclpqZisySyMuNj-3rnpWaisbGnJaRxo6dx5aTy5mazJ3l8_duOXlP-e9JDEY2_d3z9y5odk_570kMRjb9zef1656Vms2ekJCPjI6Wjo2Lz8aQm8-Y7_zF656Vms2ekJCPjI6Wjo2Lz8aQm8-YveuelZqczI-Vzo_MlZCdzpjHmJnGjLXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.noEkH-f_BZmlJ1jnUif4NM9lh_Giw1az75Hs1Dbmwmf8GenG-LK1U6Op7c6fO0VeL6hfPY9NePSk9agONVDODg'  # Токен для доступа к YandexGPT
    folder_id = 'b1gfe8mbuq037jbemc92'  # Folder_id для доступа к YandexGPT


    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite",  # модель для генерации текста
        "completionOptions": {
            "stream": False,  # потоковая передача частично сгенерированного текста выключена
            "temperature": 0.6,  # чем выше значение этого параметра, тем более креативными будут ответы модели (0-1)
            "maxTokens": "200"  # максимальное число сгенерированных токенов, очень важный параметр для экономии токенов
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



prompt_gpt = input("Про что будем писать рассказ? ")
theme_gpt = input("В какой тематике должен быть рассказ? ")
location_gpt = input("Где будет происходить действие? ")

ask_gpt(prompt_gpt,theme_gpt, location_gpt)