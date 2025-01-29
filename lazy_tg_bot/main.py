import os
import subprocess

import telebot
from telebot import types
from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"), parse_mode="MARKDOWN")
main_user_id = int(os.getenv("USER_ID"))


check_main_user = lambda message: message.from_user.id == main_user_id


@bot.message_handler(commands=["start"], func=check_main_user)
def send_welcome(message: types.Message):
    bot.reply_to(message, "Все в порядке, я работаю!")


def take_screenshot():
    screenshot_path = "/tmp/screenshot.png"
    try:
        subprocess.run(["import", "-window", "root", screenshot_path], check=True)
        return screenshot_path
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании скриншота: {e}")
        return None


@bot.message_handler(func=check_main_user)
@bot.message_handler(commands=["prtsc"])
def handle_prtsc(message: types.Message):
    # bot.reply_to(message, "Создание скриншота...")

    screenshot_path = take_screenshot()
    if screenshot_path and os.path.exists(screenshot_path):
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(message.chat.id, photo)
        os.remove(screenshot_path)  # Удаляем скриншот после отправки
    else:
        bot.reply_to(message, "Не удалось создать скриншот.")


if __name__ == "__main__":
    bot.infinity_polling()
