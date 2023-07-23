import telebot
import os

from dotenv import load_dotenv
from cake_app.models import Order, Baker


load_dotenv()
bot = telebot.TeleBot(os.environ["BAKER_TG_TOKEN"])


@bot.message_handler(commands=['start'])
def start_handler(message):
    baker, _ = Baker.objects.get_or_create(tg_id=message.from_user.id,
                                           tg_username=message.from_user.username)

    bot.send_message(message.from_user.id, "В этот чат будут приходить новые заказы")


def send_order(order: Order):
    bakers = Baker.objects.all()
    for baker in bakers:
        if order.readycake:
            cake = order.readycake
            bot.send_message(baker.tg_id, f'Новый заказ. Номер заказа: {order.pk}\n\n'
                                          f'Готовый торт: {cake}. Топпинг: {cake.topping}\n'
                                          f'Надпись: {order.inscription}\n'
                                          f'Комментарий: {order.comment}\n\n'
                                          f'Адрес: {order.address}')
        elif order.customizedcake:
            cake = order.customizedcake
            bot.send_message(baker.tg_id, f'Новый заказ. Номер заказа: {order.pk}\n\n'
                                          f'Кастомищированный торт.'
                                          f'Уровни: {cake.levels}\n'
                                          f'Форма: {cake.shape}\n'
                                          f'Начинка: {cake.filling}\n'
                                          f'Топпинг: {cake.toping}\n'
                                          f'Ягоды: {cake.berries}\n'
                                          f'Декор: {cake.decore}\n'
                                          f'Надпись: {order.inscription}\n'
                                          f'Комментарий: {order.comment}\n\n'
                                          f'Адрес: {order.address}')
        else:
            bot.send_message(baker.tg_id, f'Новый заказ. Номер заказа: {order.pk}\n'
                                          f'Посмотрите в базу')


def run_baker():
    bot.polling(none_stop=True, interval=0)
