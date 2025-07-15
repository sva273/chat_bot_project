def greet_user():
    print('Привет!  Я чат-бот. Что ты хочешь узнать? ')
    print("1 - Текущая дата и время")
    print("2 - Погода")
    print("3 - Цитата")
    print("4 - Гороскоп на день")
    print("5 - Достопримечательности")
    print("q - Выход")


def get_user_choice():
    return input("Выберите опцию: ")


def ask_city():
    return input("Введите название города: ")


ZODIAC_SIGNS = {
    "1": "aries", "2": "taurus", "3": "gemini", "4": "cancer", "5": "leo",
    "6": "virgo", "7": "libra", "8": "scorpio", "9": "sagittarius",
    "10": "capricorn", "11": "aquarius", "12": "pisces"}


def ask_sign_by_number():
    print("Выберите свой знак зодиака:")
    for number, sign in ZODIAC_SIGNS.items():
        print(f"{number}. {sign.capitalize()}")
    choice = input("Введите номер знака (1–12): ").strip()
    return ZODIAC_SIGNS.get(choice, None)
