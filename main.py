import requests
import uuid
import urllib3

# Authorization Key из личного кабинета
AUTHORIZATION_KEY = "your_key"

# Тип доступа
SCOPE = "GIGACHAT_API_PERS"

# Выбранная модель
MODEL = "GigaChat-3-Ultra"

# Отключение SSL для тестирования
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_access_token():

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {AUTHORIZATION_KEY}"
    }

    data = {
        "scope": SCOPE
    }

    response = requests.post(
        url,
        headers=headers,
        data=data,
        verify=False,
        timeout=30
    )

    response.raise_for_status()

    token_data = response.json()

    return token_data["access_token"]


def ask_gigachat(question):

    token = get_access_token()

    url = "https://api.giga.chat/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        verify=False,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]

def main():

    print("=" * 55)
    print("GIGACHAT CONSOLE")
    print("Модель:", MODEL)
    print("Для выхода напишите: exit")
    print("=" * 55)

    while True:

        question = input("\nВы: ").strip()

        if question.lower() in ["exit", "quit", "выход"]:
            print("Завершение работы.")
            break

        if not question:
            continue

        try:

            print("\nGigaChat генерирует ответ...")

            answer = ask_gigachat(question)

            print("\nGigaChat:")
            print(answer)

        except requests.exceptions.HTTPError as error:

            print("\nОшибка HTTP:")
            print(error.response.status_code)
            print(error.response.text)

        except requests.exceptions.RequestException as error:

            print("\nОшибка соединения:")
            print(error)

        except Exception as error:

            print("\nОшибка:")
            print(error)


if __name__ == "__main__":
    main()