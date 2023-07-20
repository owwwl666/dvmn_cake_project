import telebot
from telebot import types

bot = telebot.TeleBot('6398010979:AAFxPibC3gWVnLSOT9eiujMk2SirpYRyAOo')

""""""

@bot.message_handler(commands = ['start'])
def url(message):
    doc = open('Согласие.doc', 'rb')
    bot.send_document(message.from_user.id, doc)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('✅')
    markup.add(btn)
    bot.send_message(message.from_user.id, "Нажимая на кнопку ниже, Вы соглашаетесь с условиями Политики и даете согласие на обработку ваших персональных данных", reply_markup = markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '✅':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        btn1 = types.KeyboardButton('Заказать торт 🍰')
        btn2 = types.KeyboardButton('Узнать сроки доставки 🕒')
        #if :
        #btn4 = types.KeyboardButton('Детали заказа')
        #btn3 = types.KeyboardButton('Предыдущие заказы')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, '👋 Привет! Я бот пекарни CakeBake. Со мной вы можете собрать свой авторский торт, оформить заказ, а также узнать цены и сроки доставки. Чем могу помочь?', reply_markup=markup)
    elif message.text == 'Вернуться в главное меню ⬅️':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
        btn1 = types.KeyboardButton('Заказать торт 🍰')
        btn2 = types.KeyboardButton('Узнать сроки доставки 🕒')
        #if :
        #btn3 = types.KeyboardButton('Советы по оформлению публикации')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Чем могу помочь?', reply_markup=markup) 
    elif message.text == 'Узнать сроки доставки 🕒':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Вернуться в главное меню ⬅️')
        markup.add(btn1)
        bot.send_message(message.from_user.id, 'Центр - 12 часов\nВ пределах МКАДа - 1 день\nВ пределах области - 2 дня', reply_markup=markup)
    elif message.text == 'Заказать торт 🍰':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Торт A (1000 р.)')
        btn2 = types.KeyboardButton('Торт B (1400 р.)')
        btn3 = types.KeyboardButton('Торт C (3000 р.)')
        btn4 = types.KeyboardButton('Вернуться в главное меню ⬅️')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id, 'Выберите цену', reply_markup=markup)
        bot.register_next_step_handler(message, lambda message: choose_cake(message))
def choose_cake(message):
    order = {}
    if message.text == 'Торт A (1000 р.)':
        order['price'] = 1000
    if message.text == 'Торт B (1400 р.)':
        order['price'] = 1400
    if message.text == 'Торт C (3000 р.)':
        order['price'] = 3000
    bot.send_message(message.from_user.id, 'Предлагаю ознакомиться с нашими тортами ')
    bot.send_photo(message.chat.id, photo=open('media/napoleon.jpg', 'rb'))
    bot.send_message(message.from_user.id, 'Наполеон. Описание')
    bot.send_photo(message.chat.id, photo=open("media/praga.jpg", 'rb'))
    bot.send_message(message.from_user.id, 'Прага. Описание')
    bot.send_photo(message.chat.id, photo=open("media/murav.jpg", 'rb'))
    bot.send_message(message.from_user.id, 'Муравейник. Описание')
    bot.send_photo(message.chat.id, photo=open("media/tiramisu.jpg", 'rb'))
    bot.send_message(message.from_user.id, 'Торт Тирамису. Описание')
    bot.send_photo(message.chat.id, photo=open("media/medovik.png", 'rb'))
    bot.send_message(message.from_user.id, 'Медовик. Описание')
    bot.send_photo(message.chat.id, photo=open("media/bisquit.jpg", 'rb'))
    bot.send_message(message.from_user.id, 'Бисквитный. Описание')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Выбрать торт из предложенных')
    btn2 = types.KeyboardButton('Собрать свой ')
    btn3 = types.KeyboardButton('Вернуться в главное меню ⬅️')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, f'Какой понравился больше всего? Или хотите собрать свой?', reply_markup=markup)
    bot.register_next_step_handler(message, lambda message: inscription_cake(message, order))

def inscription_cake(message, order):
    if message.text == 'Выбрать торт из предложенных':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Пропустить')
        btn2 = types.KeyboardButton('Вернуться в главное меню ⬅️')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Хотите сделать надпись на торте?   Мы можем разместить на торте любую надпись, например: «С днем рождения!» Введите текст надписи')
        if message.text == 'Пропустить':
            bot.register_next_step_handler(message, lambda message: delivery(order, message))
    if message.text == 'Собрать свой ': 
        bot.register_next_step_handler(message, lambda message: custom_cake(message, order))
    if message.text == 'Вернуться в главное меню ⬅️':
        bot.register_next_step_handler(message, get_text_messages(message))
'''
    if message.text == 'Пропустить':
        bot.register_next_step_handler(message, lambda message: delivery(order, message))
    if message.text == 'Вернуться в главное меню ⬅️':
        bot.register_next_step_handler(message, get_text_messages(message))
    if message.text == '':
        bot.send_message(message.from_user.id, 'Вы ввели пустое сообщение, попробуйте ещё раз')
        bot.register_next_step_handler(message, lambda message: inscription_cake(order, message))
    if len(message.text) > 30:
        bot.send_message(message.from_user.id, 'Вы ввели слишком длинный текст, попробуйте ещё раз')
        bot.register_next_step_handler(message, lambda message: inscription_cake(order, message))'''
def custom_cake(order, message):
    pass

def delivery(order, message):
    pass


bot.polling(none_stop=True, interval=0)