#!coding:utf-8

"""
Download data from Tushare
"""

import tushare as ts
import pickle
from os.path import exists

class Download():
	def __init__(self, filename):
		self.filename = filename
		
	def download_base(self):
		licise = "2c93d403ebc9baab05d1754e951c52e59b14026435a644f717e58ee8"
		pro = ts.pro_api(licise)
		self.base = pro.stock_basic(exchange='', list_status='L')

	def dump_data(self):
		with open(self.filename, mode="wb") as outfile:
			pickle.dump(self.base, outfile)
		
	def load_data(self):
		assert exists(self.filename), self.filename + " is not exists"
		with open(self.filename, mode="rb") as infile:
			self.data = pickle.load(infile)

	def filter(self):
		self.code = self.data["ts_code"]


def main():
	Down = Download("stocklist.pkl")
	Down.download_base()
	Down.dump_data()
	

if __name__ == "__main__":
	main()
