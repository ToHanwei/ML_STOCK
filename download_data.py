#!coding:utf-8

from pickle import load
import tushare as ts
import pandas as pd
import pymysql
import requests
from time import sleep
from sqlalchemy import create_engine

class StockData(object):
	def __init__(self, filename, database, user, port, passwd, host):
		self.filename = filename
		self.database = database
		self.user = user
		self.port = port
		self.passwd = passwd
		self.host = host
		
	def get_codes(self):
		"""Obtain stock code from pkl format file"""
		with open(self.filename, mode="rb") as infile:
			stock_base = load(infile)
		self.codes = stock_base['ts_code']

	def connect_db(self):
		"""Connect database"""
		self.db = pymysql.connect(host="localhost",
							 user="root",
							 passwd="hanwei1")
		self.cursor = self.db.cursor()

	def down_data(self):
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
					data = pro.daily(ts_code=code)
				except requests.exceptions.ReadTimeout as e:
					sleep(1)
					count += 1
					#Try too much will exist. less 100 times
					assert count<100, name+" try too much!"
				else:
					print("code "+name+" has done!"); break
			data.to_sql(name=name, con=engine, if_exists="replace", index=False)


def main():
	Stock = StockData("stocklist.pkl", "stock", "root", "3306", "hanwei1", "localhost")
	Stock.get_codes()
	Stock.down_data()


if __name__ == "__main__":
	main()
