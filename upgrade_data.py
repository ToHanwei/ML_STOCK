#!/home/hanwei/soft/anaconda3/bin/python3.7
#!coding:utf-8

import pandas as pd
from pickle import load
from pickle import dump
import tushare as ts
import logging
import datetime
import time
import copy
import pymysql
from download_data import StockData

class Upgrade_list():
	"""upgrade stock basic list"""
	def __init__(self, filename):
		self.filename = filename
	
	def loger(self):
		log_path = "./Logs/"
		file_path = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
		log_file = log_path + file_path + ".log"
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.INFO)
		filer = logging.FileHandler(log_file, mode='a')
		filer.setLevel(logging.DEBUG)
		formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] -%(levelname)s:%(message)s")
		filer.setFormatter(formatter)
		self.logger.addHandler(filer)
		self.mes1 = "The original data have add code: "
		self.mes2 = "The original data have reduce code: "
		
	def booler(self, row):
		return (not all(row))

	def login(self):
		db = pymysql.connect(host="localhost",
							 user="root",
							 db="stock",
							 password="hanwei1")
		self.cursor = db.cursor()
	
	def droptables(self, tables):
		self.login()
		cur = self.cursor
		cur.execute('use stock;')
		for name in tables:
			cur.execute('drop table	`'+name+'`;')

	def addtables(self, tables):
		Stock = StockData("stocklist.pkl", "stock", "root", "3306", "hanwei1", "localhost")
		Stock.codes = tables
		Stock.down_data(app=False)

	def upgrade(self):
		with open('date.pkl', 'rb') as infile:
			date = load(infile)
		last_date = date[-1]
		this_date = (datetime.datetime.now()+datetime.timedelta(days=+1)).strftime("%Y%m%d")
		date.append(this_date)
		with open('date.pkl', 'wb') as outfile:
			dump(date, outfile)
		Stock = StockData("stocklist.pkl", "stock", "root", "3306", "hanwei1", "localhost")
		Stock.date = last_date
		Stock.get_codes()
		Stock.down_data()

	def change(self):
		"""compare the stocklist file and upgrade"""
		with open(self.filename, mode='rb') as infile:
			basic = load(infile)
		#download new stock base date
		pro = ts.pro_api()
		new_basic = pro.stock_basic()
		add = set(new_basic['ts_code']) - set(basic['ts_code'])
		red = set(basic['ts_code']) - set(new_basic['ts_code'])
		if len(red) != 0:
			self.droptables(red)
			for name in add:
				mes = self.mes2 + name
				self.logger.info(mes)
		elif len(add) != 0:
			self.addtables(add)
			for name in red:
				mes = self.mes1 + name
				self.logger.info(mes)

def main():
	print(time.strftime("%Y%m%d"))
	Up = Upgrade_list("stocklist.pkl")
	Up.loger()
	Up.change()
	Up.upgrade()

if __name__ == "__main__":
	main()
