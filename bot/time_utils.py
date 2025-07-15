import os
from datetime import datetime, timedelta, timezone
import requests
from dotenv import load_dotenv

load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")  # Вставьте свой API ключ


def get_current_time(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang=ru"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        timezone_shift = data.get('timezone')
        if timezone_shift is None:
            return f"Ошибка: не удалось определить часовой пояс для '{city}'."

        # Используем timezone-aware объект UTC
        utc_now = datetime.now(timezone.utc)
        local_time = utc_now + timedelta(seconds=timezone_shift)

        return f"Местное время в {city}: {local_time.strftime('%Y-%m-%d %H:%M:%S')}"
    except requests.RequestException as e:
        return f"Ошибка запроса: {e}"
    except Exception as e:
        return f"Ошибка: {e}"

# Пример использования
if __name__ == "__main__":
    user_input = input("Введите город: ").strip()
    print(get_current_time(user_input))



