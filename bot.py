import telebot
from config import TOKEN
from extensions import CryptoCurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    text = (
        "Чтобы получить цену на криптовалюту, введите сообщение в формате:\n"
        "<имя криптовалюты> <имя валюты, в которой надо узнать цену> <количество первой валюты>\n"
        "Например: 'BTC USD 10'\n\n"
        "Чтобы узнать доступные валюты, введите команду /values."
    )
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values_message(message):
    text = "Доступные валюты:\nBitcoin (BTC), Ethereum (ETH), Ripple (XRP), и другие."
    bot.reply_to(message, text)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверное количество параметров. Ожидается 3 параметра.')

        base, quote, amount = values
        amount = float(amount)

        price = CryptoCurrencyConverter.get_price(base.upper(), quote.upper(), amount)
        text = f'{amount} {base} = {price:.2f} {quote}'
        bot.reply_to(message, text)

    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except ValueError:
        bot.reply_to(message, 'Ошибка: неверно указано количество.')

if __name__ == '__main__':
    bot.polling(none_stop=True)
