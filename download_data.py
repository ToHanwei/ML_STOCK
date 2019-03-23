#!coding:utf-8

"""
Download all history data of stock
This time the end date is March 15,2019
"""
from pickle import load
import tushare as ts
import pandas as pd
import logging
import pymysql
import requests
from time import sleep
from sqlalchemy import create_engine

class StockData(object):
	"""
	Arguments:
	filename -- stock code list file
	database -- save data database name
	user     -- database's user
	port     -- database's port
	passwd   -- user's passwd of database
	host     -- database's host
	"""
	def __init__(self, filename, database, user, port, passwd, host):
		self.filename = filename
		self.database = database
		self.user = user
		self.port = port
		self.passwd = passwd
		self.host = host
		self.date = "20190315"

	def get_codes(self):
		"""Obtain stock code from pkl format file"""
		with open(self.filename, mode="rb") as infile:
			stock_base = load(infile)
		self.codes = stock_base['ts_code']

	def connect_db(self):
		"""Connect database"""
		self.db = pymysql.connect(host=self.host,
							 user=self.user,
							 password=self.passwd,
							 db=self.database,)
		self.cursor = self.db.cursor()

	def down_data(self, append=True):
		"""
		Download stock daily data and save to MySQL
		Database name is root
		Table name is stock
		"""
		site = "mysql+pymysql://"+self.user+":"+self.passwd+"@"+self.host+\
				":"+self.port+"/"+self.database
		engine = create_engine(site)
		pro = ts.pro_api()
		for code in self.codes:
			name = code.split(".")[0]
			count = 0
			while True:
				try:
					if append:
						data = pro.daily(ts_code=code, start_date=self.date)
					else:
						data = pro.daily(ts_code=code)
				except requests.exceptions.ReadTimeout as e:
					sleep(1)
					count += 1
					if count == 1: print("Try:")
					print(count, end="->")
					#Try too much will exist. less 100 times
					assert count<100, name+" try too much!"
				#connetion too fast
				except requests.exceptions.ConnectionError as r:
					print("ConnectionError, now sleep 5s")
					sleep(5)
				except Exception as x:
					print("sleep 5s and try again!")
					sleep(5)
				else:
					print("code "+name+" has done!"); break
			data.to_sql(name=name, con=engine, if_exists="append", index=False)

	def writelog(self, logname):
		logging.basicConfig(level=logging.DEBUG,
			format='%(asctime)s-%(filename)s[line:%(lineno)d] - %(levename)s:%(message)s')
		

def main():
	Stock = StockData("stocklist.pkl", "stock", "root", "3306", "hanwei1", "localhost")
	Stock.get_codes()
	Stock.down_data()


if __name__ == "__main__":
	main()
