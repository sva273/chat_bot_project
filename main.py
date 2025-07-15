import logging
from bot.telegram_bot import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Запускаем Telegram-бота.....")
    main()
