import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()

bot = telebot.TeleBot("6220937558:AAGprv2siDZEwg_sONDtpwHMXSlxqYj355w",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = 'Попробуй нажать на эту заведомую кнопку'
text_button_1 = 'Ссылка на телеграмм канал Марафон по Python | Умскул'
text_button_2 = 'Ссылка на Youtube канал Умскул'
text_button_3 = 'Ссылка на телеграмм канал автора данного бота'

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state='*', commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Если ты видишь это сообщение, значит ты сделал все правильно и попал куда нужно!',
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Здорово! Назовитесь путник.')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Отлично! Сейчас назовите свой возраст и знайте, он не имеет значения)')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Ты успешно прошел этап регистрации! Потыкай по кнопкам ^-^',
                     reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     'Не забывай, что 17.10.23 нужно сдать домашку! [Марафон по Python | Умскул](https://t.me/+jjHK7mxBpMthZWFi)')


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     'Поздравляю! Ты получил ссылку, тыкай скорей! [umschool](https://www.youtube.com/@umschool')


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, 'Остались вопросы? Напиши! [flickxgood](https://t.me/flickxxgod')


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()




