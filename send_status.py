import requests
import time
from config import token

url = "https://api.telegram.org/bot{0}/sendMessage".format(token)

def message_user(message_text, chat_id):
	message_data = {
	'chat_id': chat_id,
	'text': message_text,
	'parse_mode':'HTML'
	}
	requests.post(url, data=message_data)

def main():
	message_dev('asdasd')

if __name__ == "__main__":
	main()