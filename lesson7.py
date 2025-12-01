import os
import ptbot
import random
from dotenv import load_dotenv
from pytimeparse import parse


def wait(chat_id, message, bot):
    message_id = bot.send_message(chat_id, "Запускаю таймер...")
    timer = parse(message)
    bot.create_countdown(timer, notify_progress, chat_id=chat_id, message_id=message_id, total=timer, bot=bot)
    bot.create_timer(timer, choose, chat_id=chat_id, bot=bot)

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def notify_progress(secs_left, chat_id, message_id, total, bot):
    progress_bar = render_progressbar(total=total, iteration=total - secs_left)
    text_message = f'Осталось {secs_left} секунд\n{progress_bar}'
    bot.update_message(chat_id, message_id, text_message)

def choose(chat_id, bot):
    bot.send_message(chat_id, 'Время вышло!')


def main():
    load_dotenv()
    telegram_token = os.getenv('TG_TOKEN')
    telegram_chat_id = os.getenv('TG_CHAT_ID')
    bot = ptbot.Bot(telegram_token)
    bot.reply_on_message(lambda chat_id, message: wait(chat_id, message, bot=bot))
    bot.run_bot()

if __name__ == '__main__':
    main()