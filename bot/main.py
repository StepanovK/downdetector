import threading
from time import sleep

import config
from bot import bot
from config import logger
# from event_checker import get_all_events
import handlers


def main():
    if config.debug:
        _start_polling()
    else:
        polling = threading.Thread(target=_start_polling)
        # sending = threading.Thread(target=_start_notifications_sending)
        polling.start()
        # sending.start()
        logger.info('Bot started!')


# def _start_notifications_sending():
#     logger.info('notifications_sending started!')
#     while True:
#         if config.debug:
#             _send_notifications()
#         else:
#             try:
#                 _send_notifications()
#             except Exception as ex:
#                 logger.error(f' {ex}')
#                 reconnect_db()
#         sleep(15)


def _start_polling():
    while True:
        try:
            logger.info('polling started!')
            bot.polling()
        except Exception as ex:
            logger.error(f'Телеграм бот упал с ошибкой: {ex}')
            sleep(15)


# def _send_notifications():
#     events_by_user = get_all_events()
#     for tg_user, events in events_by_user:
#         for event in events:
#             if event.text != '':
#                 bot.send_message(tg_user.id, event.text,
#                                  disable_web_page_preview=True,
#                                  disable_notification=not event.notice)


if __name__ == '__main__':
    main()
