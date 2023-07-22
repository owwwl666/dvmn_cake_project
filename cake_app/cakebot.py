import telebot
import os

from telebot import types

from dotenv import load_dotenv
import os
import sqlite3
from cake_app.models import Client, ReadyCake, Order, CustomizedCake
from dvmn_cake_project.settings import STATIC_DIR, MEDIA_ROOT

load_dotenv()
bot = telebot.TeleBot(os.environ["TG_TOKEN"])
order = {}


@bot.message_handler(commands=['start'])
def url(message):
    agreement_path = os.path.join(STATIC_DIR, 'Согласие.doc')
    doc = open(agreement_path, 'rb')
    bot.send_document(message.from_user.id, doc)
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='✅')
    markup.add(btn)
    bot.send_message(message.from_user.id,
                     "Нажимая на кнопку ниже, Вы соглашаетесь с условиями Политики и даете согласие на обработку ваших персональных данных",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Вернуться в главное меню ⬅️'))
def get_text_messages(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='Заказать торт 🍰', text='Заказать торт 🍰')
    btn2 = types.InlineKeyboardButton(callback_data='Узнать сроки доставки 🕒', text='Узнать сроки доставки 🕒')
    # if :
    # btn4 = types.KeyboardButton('Детали заказа')
    # btn3 = types.KeyboardButton('Предыдущие заказы')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     '👋 Привет! Я бот пекарни CakeBake. Со мной вы можете собрать свой авторский торт, оформить заказ, а также узнать цены и сроки доставки. Чем могу помочь?',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Узнать сроки доставки 🕒'))
def find_out_delivery_time(call):
    if call.data == 'Узнать сроки доставки 🕒':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️',
                                          text='Вернуться в главное меню ⬅️')
        markup.add(btn1)
        bot.send_message(call.from_user.id, 'Центр - 12 часов\nВ пределах МКАДа - 1 день\nВ пределах области - 2 дня',
                         reply_markup=markup)
    elif call.data == 'Вернуться в главное меню ⬅️':
        bot.edit_message_text(chat_id=call.chat.id, message_id=call.message_id, text='вы вернулись в главное меню',
                              reply_markup=get_text_messages())


@bot.callback_query_handler(func=lambda call: call.data.startswith('Заказать торт 🍰'))
def choose_cake(call):
    readycakes = ReadyCake.objects.all()
    for readycake in readycakes.iterator():
        bot.send_photo(call.from_user.id, photo=readycake.cake_image)
        bot.send_message(call.from_user.id, f'{readycake.cake_name}\nЦена: {readycake.cake_price}р.')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='Выбрать из тортов выше', text='Выбрать из тортов выше')
    btn2 = types.InlineKeyboardButton(callback_data='Собрать свой', text='Собрать свой ')
    btn3 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3)
    bot.send_message(call.from_user.id, f'Какой понравился больше всего? Или хотите собрать свой?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Собрать свой'))
def custom_cake(call):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute(f'INSERT INTO Заказы (Клиент) VALUE ({call.from_user.id})')
    markup = types.InlineKeyboardMarkup()
    bot.send_photo(call.from_user.id, photo=open("media/уровни.jpg", 'rb'))
    btn1 = types.InlineKeyboardButton(callback_data=f'Форма 1 уровень ', text='1 уровень (+400 р.)')
    btn2 = types.InlineKeyboardButton(callback_data=f'Форма 2 уровня ', text='2 уровня (+750 р.)')
    btn3 = types.InlineKeyboardButton(callback_data=f'Форма 3 уровня ', text='3 уровня (+1100 р.)')
    btn4 = types.InlineKeyboardButton(callback_data=f'Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(call.from_user.id, 'Выберете количество уровней у торта', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Форма'))
def custom_cake(message):
    global order
    if '1 уровень' in message.data:
        order['price'] = 400
        order['description'] = ' Вы собрали 1-уровневый торт'
    if '2 уровня' in message.data:
        order['price'] = 750
        order['description'] = ' Вы собрали 2-уровневый торт'
    if '3 уровня' in message.data:
        order['price'] = 1100
        order['description'] = ' Вы собрали 3-уровневый торт'

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data=f'Выбрана форма квадрат ', text='Квадрат (+600 р.)')
    btn2 = types.InlineKeyboardButton(callback_data=f'Выбрана форма круг ', text='Круг (+400 р.)')
    btn3 = types.InlineKeyboardButton(callback_data=f'Выбрана форма прямоугольник ', text='Прямоугольник (+1000 р.)')
    btn4 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, 'Выберете форму торта', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Выбрана форма '))
def default_cake(message):
    '''order = ast.literal_eval(message.data.split("-")[1])'''
    global order
    if 'квадрат' in message.data:
        order['price'] += 600
        order['description'] = f"{order['description']} квадратной формы "
    if 'круг' in message.data:
        order['price'] += 400
        order['description'] = f"{order['description']} круглой формы "
    if 'прямоугольник' in message.data:
        order['price'] += 1000
        order['description'] = f"{order['description']} прямоугольной формы "

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data=f'Выбран сироп Без топинга ', text='Без топинга (0 р.)')
    btn2 = types.InlineKeyboardButton(callback_data=f'Выбран сироп Белый соус ', text='Белый соус (+200 р.)')
    btn3 = types.InlineKeyboardButton(callback_data=f'Выбран сироп Карамельный сироп',
                                      text='Карамельный сироп (+180 р.)')
    btn4 = types.InlineKeyboardButton(callback_data=f'Выбран сироп Кленовый сироп', text='Кленовый сироп (+200 р.)')
    btn5 = types.InlineKeyboardButton(callback_data=f'Выбран сироп Клубничный сироп', text='Клубничный сироп (+300 р.)')
    btn6 = types.InlineKeyboardButton(callback_data=f'Выбран сироп Черничный сироп', text='Черничный сироп (+350 р.)')
    btn7 = types.InlineKeyboardButton(callback_data=f'Выбран сироп Молочный шоколад', text='Молочный шоколад (+200 р.)')
    btn8 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    bot.send_message(message.from_user.id, f'Какой топинг выберете?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Выбран сироп'))
def default_cake(message):
    global order
    if 'Белый соус' in message.data:
        order['price'] += 200
        order['description'] = f'{order["description"]} с белым соусом'
    if 'Кленовый сироп' in message.data:
        order['price'] += 200
        order['description'] = f'{order["description"]} с кленовым сиропом'
    if 'Молочный шоколад' in message.data:
        order['price'] += 200
        order['description'] = f'{order["description"]} с молочным шоколадом'
    if 'Карамельный' in message.data:
        order['price'] += 180
        order['description'] = f'{order["description"]} с карамельным сиропом'
    if 'Клубничный' in message.data:
        order['price'] += 300
        order['description'] = f'{order["description"]} с клубничным сиропом'
    if 'Черничный' in message.data:
        order['price'] += 350
        order['description'] = f'{order["description"]} с черничным сиропом'
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data=f'Выбраны ягоды Ежевика', text='Ежевика (+400)')
    btn2 = types.InlineKeyboardButton(callback_data=f'Выбраны ягоды Малина', text='Малина (+300)')
    btn3 = types.InlineKeyboardButton(callback_data=f'Выбраны ягоды Голубика', text='Голубика (+450)')
    btn4 = types.InlineKeyboardButton(callback_data=f'Выбраны ягоды Клубника', text='Клубника (+500)')
    btn5 = types.InlineKeyboardButton(callback_data=f'Выбраны ягоды Пропустить', text='Пропустить')
    btn8 = types.InlineKeyboardButton(callback_data=f'Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn8)
    bot.send_message(message.from_user.id, f'Какими ягодами украсить?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Выбраны ягоды'))
def default_cake(message):
    global order
    '''order = ast.literal_eval(message.data.split("-")[1])'''
    if 'Ежевика' in message.data:
        order['price'] += 400
        order['description'] = f"{order['description']} и с ежевикой."
    if 'Малина' in message.data:
        order['price'] += 300
        order['description'] = f"{order['description']} и с малиной."
    if 'Голубика' in message.data:
        order['price'] += 450
        order['description'] = f"{order['description']} и с голубикой."
    if 'Клубника' in message.data:
        order['price'] += 500
        order['description'] = f"{order['description']} и с клубникой."
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data=f'Выбран декор Фисташки (+300)', text='Фисташки (+300 р.)')
    btn2 = types.InlineKeyboardButton(callback_data=f'Выбран декор Безе (+400)', text='Безе (+400 р.)')
    btn3 = types.InlineKeyboardButton(callback_data=f'Выбран декор Фундук (+350)', text='Фундук (+350 р.)')
    btn4 = types.InlineKeyboardButton(callback_data=f'Выбран декор Пекан (+300)', text='Пекан (+300 р.)')
    btn5 = types.InlineKeyboardButton(callback_data=f'Выбран декор Маршмеллоу (+200)', text='Маршмеллоу (+200 р.)')
    btn6 = types.InlineKeyboardButton(callback_data=f'Выбран декор Марципан (+280)', text='Марципан (+280 р.)')
    btn7 = types.InlineKeyboardButton(callback_data=f'Выбран декор Молочный шоколад', text='Молочный шоколад (+200 р.)')
    btn8 = types.InlineKeyboardButton(callback_data='Выбран декор Пропустить', text='Пропустить')
    btn9 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    bot.send_message(message.from_user.id, f'Какой декор предпочтёте?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Выбран декор'))
def inscription_cake(message):
    global order
    if 'Фисташки' in message.data:
        order['price'] += 300
        order['description'] = f"{order['description']} Кроме этого мы украсим Ваш торт фисташками."
    if 'Пекан' in message.data:
        order['price'] += 300
        order['description'] = f"{order['description']} Кроме этого мы украсим Ваш торт пеканом."
    if 'Безе' in message.data:
        order['price'] += 400
        order['description'] = f"{order['description']} Кроме этого мы украсим Ваш торт безе."
    if 'Маршмеллоу' in message.data:
        order['price'] += 200
        order['description'] = f"{order['description']} Кроме этого мы украсим Ваш торт маршмеллоу."
    if 'Молочный шоколад' in message.data:
        order['price'] += 200
        order['description'] = f"{order['description']} Кроме этого мы украсим Ваш торт молочным шоколадом."
    if 'Марципан' in message.data:
        order['price'] += 280
        order['description'] = f"{order['description']} Кроме этого мы украсим Ваш торт марципаном."
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data=f'Перейти к выбору доставки', text='Пропустить')
    btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2)
    message = bot.send_message(message.from_user.id,
                               'Хотите сделать надпись на торте?   Мы можем разместить на торте любую надпись, например: «С днем рождения!» Введите текст надписи',
                               reply_markup=markup)
    bot.register_next_step_handler(message, address)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Выбрать из тортов выше'))
def default_cake(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data=f'Выбран торт Наполеон', text='Наполеон')
    btn2 = types.InlineKeyboardButton(callback_data=f'Выбран торт Прага', text='Прага')
    btn3 = types.InlineKeyboardButton(callback_data=f'Выбран торт Муравейник', text='Муравейник')
    btn4 = types.InlineKeyboardButton(callback_data=f'Выбран торт Тирамису', text='Тирамису')
    btn5 = types.InlineKeyboardButton(callback_data=f'Выбран торт Медовик', text='Медовик')
    btn6 = types.InlineKeyboardButton(callback_data=f'Выбран торт Бисквитный', text='Бисквитный')
    btn7 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.from_user.id, f'Какой торт вы выбираете?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Выбран торт '))
def inscription_cake(message):
    global order
    if 'Наполеон' in message.data:
        order['price'] = 1400
        order['description'] = 'Наполеон'
    if 'Прага' in message.data:
        order['price'] = 1400
        order['description'] = 'Прага'
    if 'Муравейник' in message.data:
        order['price'] = 1400
        order['description'] = 'Муравейник'
    if 'Тирамису' in message.data:
        order['price'] = 1400
        order['description'] = 'Тирамису'
    if 'Медовик' in message.data:
        order['price'] = 1400
        order['description'] = 'Медовик'
    if 'Бисквитный' in message.data:
        order['price'] = 1400
        order['description'] = 'Бисквитный'
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='Перейти к выбору доставки', text='Пропустить')
    btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     'Хотите сделать надпись на торте?   Мы можем разместить на торте любую надпись, например: «С днем рождения!» Введите текст надписи',
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Перейти к выбору доставки'))
def address(message):
    if message.data == "Перейти к выбору доставки":
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(callback_data=f'к комм в центре', text='Ваш адрес в центре города')
        btn2 = types.InlineKeyboardButton(callback_data=f'к комм МКАДа', text='Ваш адрес в пределах МКАДа')
        btn3 = types.InlineKeyboardButton(callback_data=f'к комм обл', text='В пределах области')
        btn4 = types.InlineKeyboardButton(callback_data=f'к комм самовывоз', text='Самовывоз')
        btn5 = types.InlineKeyboardButton(callback_data=f'Вернуться в главное меню ⬅️',
                                          text='Вернуться в главное меню ⬅️')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.from_user.id,
                         f'Введите адрес доставки\nСамовывоз возможен с завтрашнего дня с 9:00 до 17:00.',
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('к комм'))
def address(message):
    global order
    if 'в центре' in message.data or 'МКАДа' in message.data:
        order['delivery'] = 'завтра'
    if 'обл' in message.data:
        order['delivery'] = 'послезавтра'
    if 'самовывоз' in message.data:
        order['delivery'] = 'самовывоз'
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data=f'Детали заказа', text='Пропустить')
    btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, f'Вы можете добавить комментарий к заказу', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Детали заказа'))
def address(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(callback_data='Узнать дату доставки', text='Узнать дату доставки')
    btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id,
                     f"Ваш заказ сохранён.\nДетали заказа: {order['description']}\nЦена: {order['price']} р.",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('Узнать дату доставки'))
def address(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton(callback_data='Вернуться в главное меню ⬅️', text='Вернуться в главное меню ⬅️')
    markup.add(btn2)
    if order['delivery'] == "самовывоз":
        bot.send_message(message.from_user.id, f"Вы можете забрать заказ завтра c 9:00 до 17:00.", reply_markup=markup)

    bot.send_message(message.from_user.id, f"Торт будет доставлен {order['delivery']} c 9:00 до 17:00.",
                     reply_markup=markup)


def run_bot():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    run_bot()
