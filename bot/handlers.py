import telebot.types
import re

import config
from bot import bot
from db_worker import register_monitored_app, register_user

from typing import Union


@bot.message_handler(commands=['start', 'help'])
def register_and_start(message: telebot.types.Message):
    user = register_user(
        telegram_id=message.from_user.id,
        login=message.from_user.username if message.from_user.username else '',
        first_name=message.from_user.first_name if message.from_user.first_name else '',
        last_name=message.from_user.last_name if message.from_user.last_name else '',
    )
    if isinstance(user, str):
        mes_text = f"Во время регистрации произошла ошибка:\n`{user}`"
    else:
        mes_text = 'Этот бот используется для уведомления о падении веб-приложений и ошибках в них.\n' \
                   'Работает это так:'\
                   'Приложение с заданной периодичностью отправляет боту сообщение, что всё в порядке. ' \
                   'Как только сообщения о состоянии перестают приходить, бот отправляет уведомление, ' \
                   'что приложение не активно. Как только приложение снова выходит на связь, ' \
                   'Бот также уведомляет об этом.\n' \
                   'Чтобы добавить приложение, введите команду:\n' \
                   '`/add_app <ИмяПриложения> <ИнтервалПроверкиВСек> <СостояниеОтслеживания:0/1>`'

    bot.send_message(message.from_user.id, mes_text)

#
# @bot.message_handler(commands=['my_id'])
# def registry_user(message: telebot.types.Message):
#     user_id = get_id_from_command_message(message.text, '/my_id')
#     if user_id is None:
#         bot.reply_to(message, text='Неверный формат!')
#     else:
#         user = register_user(message.from_user.id, user_id)
#         bot.reply_to(message, text=f'Привет, {user}', disable_web_page_preview=True)
#
#
# @bot.message_handler(commands=['stop'])
# def stop_alarm(message: telebot.types.Message):
#     users = unregister_user(message.from_user.id)
#     if len(users) > 0:
#         users_strs = [str(user) for user in users]
#         users_str = ', '.join(users_strs)
#         mes_text = f'Вы больше не {users_str}'
#     else:
#         mes_text = 'Вы уже отписаны'
#     bot.reply_to(message, text=mes_text, disable_web_page_preview=True)
#
#
# @bot.message_handler(commands=['subscribe_project'])
# def subsc_project(message: telebot.types.Message):
#     project_id = get_id_from_command_message(message.text, '/subscribe_project')
#     if project_id is None:
#         bot.reply_to(message, text='Неверный формат!')
#     else:
#         project = subscribe_project(message.from_user.id, project_id)
#         if project is None:
#             mes_text = f'Что-то пошло не так! Вы точно зарегистрировались?'
#         elif isinstance(project, ProjectToAdd):
#             mes_text = f'Проект с ID {project_id} пока что никем не добавлен. ' \
#                        f'Через несколько секунд он добавится и мы вас на него подпишем!'
#         else:
#             mes_text = f'Вы подписались на проект {project}'
#         bot.reply_to(message, text=mes_text, disable_web_page_preview=True)
#
#
# def get_id_from_command_message(message_text: str, command: str) -> Union[int, None]:
#     template = command + r' \d+'
#     res = re.search(template, message_text)
#     if res is not None:
#         s1, s2 = res.regs[0]
#         st = message_text[s1: s2]
#         st = st.replace(command + ' ', '')
#         if st.isdigit():
#             return int(st)
#     return None
#
#
# @bot.message_handler(commands=['unsubscribe_project'])
# def unsubsc_project(message: telebot.types.Message):
#     project_id = get_id_from_command_message(message.text, '/unsubscribe_project')
#     if project_id is None:
#         bot.reply_to(message, text='Неверный формат!')
#     else:
#         project = unsubscribe_project(message.from_user.id, project_id)
#         if project is None:
#             mes_text = f'Такой проект не найден, но вы от него успешно отписались! ;)'
#         else:
#             mes_text = f'Вы отписались от проекта {project}'
#         bot.reply_to(message, text=mes_text, disable_web_page_preview=True)
#
#
# @bot.message_handler(commands=['recreate_db'])
# def recreate_db(message: telebot.types.Message):
#     if message.from_user.id == config.telegram_admin_id:
#         recreated = recreate_database()
#         if recreated:
#             bot.reply_to(message=message, text='База данных пересоздана успешно')
#         else:
#             bot.reply_to(message=message, text='Не удалось пересоздать базу данных')
#     else:
#         bot.reply_to(message=message, text='Нет прав!')
