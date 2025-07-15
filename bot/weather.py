import os

import requests
from dotenv import load_dotenv

load_dotenv()
weather_api_key = os.getenv('WEATHER_API_KEY')  # Вставьте свой API ключ


def get_weather(city):
    try:
        # Строим URL для запроса к API OpenWeather
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=ru"
        response = requests.get(url).json()

        # Проверяем статус ответа от API
        if response.get("cod") != 200:
            return "❌ Город не найден."

        # Извлекаем нужные данные
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"].capitalize()
        wind = response["wind"]["speed"]
        rain = response.get("rain", {}).get("1h", 0)

        # Рекомендации по погоде
        advice = ""
        if rain >= 1:
            advice += "☔ Возьми зонт — возможен дождь.\n"
        if wind >= 10:
            advice += "💨 Ветер сильный, будь осторожен.\n"

        # Формируем результат
        return (
            f"📍 Погода в {city.title()}:\n"
            f"{description}\n"
            f"🌡 Температура: {temp}°C\n"
            f"💨 Ветер: {wind} м/с\n"
            f"🌧 Осадки: {rain} мм за час\n"
            f"{advice or '✅ Погода отличная!'}"
        )

    except requests.RequestException as e:
        return f"Ошибка при подключении к API: {e}"
    except KeyError:
        return "Ошибка обработки данных: неожиданный формат ответа"
    except Exception as e:
        return f"Другая ошибка: {e}"

# Пример использования:
# print(get_weather("Франкфурт"))
