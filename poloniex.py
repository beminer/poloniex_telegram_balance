import requests, json
from config import poloniex_key, poloniex_sign, chat_id
import hmac, hashlib
import urllib
import time
from mysql import sql_db
from send_status import message_user

def api_query(command, req={}):
	req['command'] = command
	req['nonce'] = int(time.time()*1000)
	post_data = urllib.parse.urlencode(req)

	sign = hmac.new(poloniex_sign, post_data.encode('utf-8'), hashlib.sha512).hexdigest()
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
		'Key': poloniex_key,
		'Sign': sign	
	}

	with requests.Session() as s:
		api = s.post('https://poloniex.com/tradingApi', data=post_data, headers=headers)
		data = json.loads(api.text)
	return data

def public_method(command):
	url = 'https://poloniex.com/public?command={0}'.format(command)
	api = requests.post(url, data=command)
	data = json.loads(api.text)
	return data

def main():
	select_all_coins = sql_db().select_all()

	#возвращает связку USDT-BTC на  Poloniex
	last = public_method('returnTicker')
	for i in last.keys():
		if 'USDT_BTC' in i:
			print('Poloniex : ', last[i]['last'])

	#Возвращает баланс с Poloniex. (не забудьте добавить свой ключ и секрет в файле config.py)
	balance = api_query('returnBalances')
	
	# проверяем у нас новая база или нет, если да, то записываем значения	
	if select_all_coins == False:
		for i in balance.items():
			if i[1] != '0.00000000':
				sql_db().insert_coin(i[0], i[1])
				print(i[0], ': \n\t', i[1] )
	# если не пустая, то нужно проверить что у нас в базе
	else:
		for i in balance.items():							
			if i[1] != '0.00000000':								# проверяем баланс на нулевой
				if i[0] not in select_all_coins.keys():				# если имя монеты не найдено в базе, то добавляем запись
					sql_db().insert_coin(i[0], i[1])
				else:
					if float(select_all_coins[i[0]]) != float(i[1]):

						message_user("Изменение баланса по монете <b>{0}</b>".format(i[0]), chat_id)
						sql_db().update_value(i[0], i[1])


if __name__ == '__main__':
	main()