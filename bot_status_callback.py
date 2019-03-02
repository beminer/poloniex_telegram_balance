import telebot
from telebot import types
from config import token
from poloniex import api_query

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(
		message.chat.id,
		'''Добро пожаловать. ✌
		''',
		reply_markup=keyboard())

@bot.message_handler(content_types=["text"])
def send_anytext(message):    
    chat_id = message.chat.id
    if message.text == '📖 Баланс':
        text = 'Для запроса баланса нажмите на интересующую монету ⬇ \n\n'
        bot.send_message(chat_id, text,parse_mode='HTML',reply_markup=balance_key(chat_id))

@bot.callback_query_handler(func=lambda message:True)
def ans(message):
	chat_id = message.message.chat.id
	if "balance_key" in message.data:
		coin = message.data.split('_')[2]
		coins = api_query('returnBalances')
		for i in coins.items():
			if i[0] == coin:
				bot.send_message(chat_id, '''====================\n\n <b>Ваш баланс {0} {1}</b>\n\n===================='''.format(coin, i[1]), parse_mode='HTML')	
	if message.data == 'wallet_return':
		bot.send_message(chat_id, '''\n\n✅ Вы в главном меню\n\n''', parse_mode='HTML', reply_markup=keyboard())

def keyboard():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	btn1 = types.KeyboardButton('📖 Баланс')
	markup.add(btn1)
	return markup  

def balance_key(chat_id):
	keyboard = types.InlineKeyboardMarkup()
	coins = api_query('returnBalances')
	wallet = []
	for i in coins.items():
		if i[1] != '0.00000000':
			wallet.append(i[0])
	for i in wallet:
		keyboard.add(types.InlineKeyboardButton(text=i,callback_data="balance_key_{0}".format(i)))
	keyboard.add(types.InlineKeyboardButton(text='⬅ Вернуться в главное меню',callback_data="wallet_return"))
	return keyboard

if __name__ == "__main__":
	bot.polling(none_stop=True)