import telebot
from config import keys, TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n' \
           '<название валюты, цену которой хотите узнать> ' \
           '<название валюты, в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты>.\n' \
           'Чтобы увидеть список доступных валют, введите команду: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for elem in keys.keys():
        text += f'\n{elem}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message):
    try:
        input_values = message.text.split()

        if len(input_values) != 3:
            raise APIException('Проверьте количество введенных параметров')

        base, quote, amount = input_values
        total = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
