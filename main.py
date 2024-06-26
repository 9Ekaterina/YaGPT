import requests

# Выполняем запрос к YandexGPT
def ask_gpt(text, sys_text, geo_text):
    iam_token = 't1.9euelZqdjo-RmsebyJTJmpHGmMqVi-3rnpWaisbGnJaRxo6dx5aTy5mazJ3l8_dhOHRP-e8gSjcT_d3z9yFncU_57yBKNxP9zef1656VmpedjI7JmJ2alYmRnJScnpiX7_zF656VmpedjI7JmJ2alYmRnJScnpiXveuelZqRy4qenMePisyXksjJxs2Qy7XehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.8FN1kGT8-QXnjSIJhwX1h3iPXrSNdKxVhwaKyiKGMSThIgKO-Q0cEhwyasQMuTkZslzRZ2s6U3pWLXmKDENwDQ'  # Токен для доступа к YandexGPT
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


