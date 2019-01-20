import pymysql
import time, re
from config import exch_base_info

class sql_db:
	def __init__(self):
		try:
			self.conn = pymysql.connect(*exch_base_info, use_unicode=True, charset='utf8')
		except pymysql.OperationalError: 
			print("can't find base")
		try:
			self.cursor = self.conn.cursor()
		except pymysql.OperationalError:
			print("can't get cursor")

	def select_all(self):
		try:
			self.cursor.execute("SELECT * FROM poloniex")
		except pymysql.Error:
			print("can't select poloniex")
		result = self.cursor.fetchall()
		if len(result) <= 0:
			return False
		else:
			data = {}
			for i in result:
				data.update({i[1]:i[2]})
			return data

	def insert_coin(self, coin, value):
		try:
			self.cursor.execute("INSERT INTO poloniex (name_coin, coin_value) values ('{0}', {1})".format(coin, value))
		except pymysql.Error:
			print("can't insert coins poloniex")
		self.conn.commit()

	def update_value(self, coin, value):
		try:
			self.cursor.execute("UPDATE poloniex set coin_value={1} where name_coin='{0}'".format(coin, value))
		except pymysql.Error:
			print("can't update poloniex value")
		self.conn.commit()				

def main():
	sql = sql_db()
	print(sql.select_all())
	b = sql.select_all()
	print(b.keys())
	if 'ETC1' in b.keys():
		print('da')

if __name__ == "__main__":
	main()