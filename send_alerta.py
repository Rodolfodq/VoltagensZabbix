import telegram
from credentials import telegram_key, chat_id
import time


def send_text(text):
    try:
        bot = telegram.Bot(token=telegram_key)
        bot.sendMessage(chat_id=chat_id, text=text)
        time.sleep(2)
    except:
        print('Erro ao encaminhar mensagem.')
    return
