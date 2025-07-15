import requests
from bs4 import BeautifulSoup
import textwrap

ZODIAC_SIGNS = {
    "1": "aries", "2": "taurus", "3": "gemini", "4": "cancer", "5": "leo",
    "6": "virgo", "7": "libra", "8": "scorpio", "9": "sagittarius",
    "10": "capricorn", "11": "aquarius", "12": "pisces"
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://horo.mail.ru/',
    'Accept-Language': 'ru-RU,ru;q=0.9'
}


def get_horoscope(sign):
    sign = sign.lower()
    if sign not in ZODIAC_SIGNS.values():
        return "Неверный знак зодиака."

    url = f"https://horo.mail.ru/prediction/{sign}/today/"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")

        main = soup.find('main', itemprop='articleBody')
        if not main:
            return "Не удалось найти текст гороскопа."

        # Собираем и очищаем текст
        paras = main.find_all('p')
        text = ' '.join(p.get_text(strip=True) for p in paras)
        text = ' '.join(text.split())  # удаление лишних пробелов

        # Форматируем по 78 символов в строке
        wrapped = textwrap.fill(text, width=78)

        return f"Гороскоп для {sign.capitalize()} на сегодня:\n{wrapped}"
    except requests.RequestException as e:
        return f"Ошибка запроса: {e}"
