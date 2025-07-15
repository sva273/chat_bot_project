import os

import requests
import time
from dotenv import load_dotenv

load_dotenv()
open_api_key = os.getenv('OPENTRIPMAP_API_KEY')  # Вставьте свой API ключ


def get_city_coords(city):
    url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    try:
        response = requests.get(url, headers={"User-Agent": "TelegramBot"}).json()
        if response:
            lat = response[0]["lat"]
            lon = response[0]["lon"]
            return float(lat), float(lon)
    except requests.RequestException as e:
        return None, None
    return None, None


def get_attractions(city):
    lat, lon = get_city_coords(city)
    if lat is None or lon is None:
        return "❌ Не удалось определить координаты города."

    url = (
        f"https://api.opentripmap.com/0.1/en/places/radius"
        f"?radius=5000&lon={lon}&lat={lat}&rate=2&format=json&limit=10&apikey={open_api_key}"
    )
    try:
        response = requests.get(url).json()
        if not response:
            return "😞 Не найдено достопримечательностей."
    except requests.RequestException as e:
        return f"Ошибка при получении достопримечательностей: {e}"

    output = f"🏛 Топ-10 достопримечательностей в {city.title()}:\n\n"

    for i, place in enumerate(response, 1):
        name = place.get("name", "Без названия")
        rate = place.get("rate", "")
        xid = place.get("xid", "")
        detail_url = f"https://api.opentripmap.com/0.1/en/places/xid/{xid}?apikey={open_api_key}"

        try:
            details = requests.get(detail_url).json()
            desc = details.get("wikipedia_extracts", {}).get("text", "")
            if desc:
                # Обрезаем описание, если оно слишком длинное
                desc = (desc[:200] + "...") if len(desc) > 200 else desc
            output += f"{i}. {name}\n"
            if desc:
                output += f"📖 {desc}\n"
            output += "\n"

            # Добавляем задержку, чтобы избежать перегрузки API
            time.sleep(0.5)

        except requests.RequestException as e:
            output += f"{i}. {name}\n📖 Не удалось получить описание. Ошибка: {e}\n\n"
        except Exception as e:
            output += f"{i}. {name}\n📖 Ошибка: {e}\n\n"

    return output.strip()
