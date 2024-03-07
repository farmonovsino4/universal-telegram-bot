from environs import Env
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

env = Env()
env.read_env()

TOKEN = env.str("BOT_TOKEN")

def keyboards():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="Ovoz", callback_data="uz"),
    )