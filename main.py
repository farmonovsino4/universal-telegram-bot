from telebot import TeleBot, types
import os
from googletrans import Translator
from deep_translator import GoogleTranslator
import pytesseract
from PIL import Image
from gtts import gTTS
from config import TOKEN
from time import sleep
import requests

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

bot = TeleBot(TOKEN)

translator = Translator()

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, f"Salom <b>{message.from_user.full_name}</b>\nmen universal tarjimon botman", parse_mode='html')

@bot.message_handler(func=lambda message: True)
def main(message: types.Message):
    lang = translator.detect(message.text).lang
    if lang == 'en':
        translated_uz = GoogleTranslator(source='en', target='uz').translate(message.text)
        translated_ru = GoogleTranslator(source='en', target='ru').translate(message.text)
        gTTS(text=translated_ru, lang='ru').save('voice.mp3')
        bot.send_message(message.chat.id, translated_uz)
        bot.send_message(message.chat.id, text=translated_ru)
        bot.send_voice(message.chat.id, open('voice.mp3', 'rb'))
    elif lang == 'uz':
        translated_en = GoogleTranslator(source='uz', target='en').translate(message.text)
        translated_ru = GoogleTranslator(source='uz', target='ru').translate(message.text)
        bot.send_message(message.chat.id, translated_en)
        gTTS(text=translated_en, lang='en').save('voice.mp3')
        bot.send_voice(message.chat.id, open('voice.mp3', 'rb'))
        bot.send_message(message.chat.id, translated_ru)
        gTTS(text=translated_ru, lang='ru').save('voice.mp3')
        bot.send_voice(message.chat.id, open('voice.mp3', 'rb'))
    elif lang == 'ru':
        translated_en = GoogleTranslator(source='ru', target='en').translate(message.text)
        translated_uz = GoogleTranslator(source='ru', target='uz').translate(message.text)
        bot.send_message(message.chat.id, translated_en)
        gTTS(text=translated_en, lang='ru').save('voice.mp3')
        bot.send_voice(message.chat.id, open('voice.mp3', 'rb'))
        bot.send_message(message.chat.id, translated_uz)
    sleep(0.5)
    os.remove("voice.mp3")

@bot.message_handler(content_types=['photo'])
def image_to_text(message: types.Message):
    bot.send_message(message.chat.id, "qabul qilindi")
    photo_id = message.photo[-1].file_id
    photo_info = bot.get_file(photo_id)
    photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{photo_info.file_path}"
    photo_data = requests.get(photo_url)
    with open("photo.jpg", "wb") as f:
        f.write(photo_data.content)
        f.close()
    img = Image.open("photo.jpg")
    text = pytesseract.image_to_string(img)
    lang = translator.detect(text).lang
    if lang == "en":
        translated_uz = GoogleTranslator(source='en', target='uz').translate(text[:5000])
        translated_ru = GoogleTranslator(source='en', target='ru').translate(text[:5000])
        bot.send_message(message.chat.id, translated_uz)
        bot.send_message(message.chat.id, translated_ru)
    elif lang == 'uz':
        translated_en = GoogleTranslator(source='uz', target='en').translate(text[:5000])
        translated_ru = GoogleTranslator(source='uz', target='ru').translate(text[:5000])
        bot.send_message(message.chat.id, translated_en)
        bot.send_message(message.chat.id, translated_ru)
    else:
        translated_en = GoogleTranslator(source='auto', target='en').translate(text[:5000])
        translated_uz = GoogleTranslator(source='auto', target='uz').translate(text[:5000])
        bot.send_message(message.chat.id, translated_en)
        bot.send_message(message.chat.id, translated_uz)
    os.remove("photo.jpg")


print(f"[{bot.get_me().username}] ishga tushdi")
bot.send_message(chat_id="5230484991", text="Bot ishga tushdi")
bot.polling(skip_pending=True, none_stop=True)