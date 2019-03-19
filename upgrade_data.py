#!coding:utf-8

from pickle import load
from pickle import dump
import tushare as ts
import logging
import time

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
		filer = logging.FileHandler(log_file, mode='w')
		filer.setLevel(logging.DEBUG)
		formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] -%(levelname)s:%(message)s")
		filer.setFormatter(formatter)
		self.logger.addHandler(filer)
		self.mes1 = "Compared with the last time has not change"
		self.mes2 = "The original data have change"
		
	def notall(self, serise):
		return (not all(serise))
	
	def upgrade(self):
		"""compare the stocklist file and upgrade"""
		with open(self.filename, mode='rb') as infile:
			basic = load(infile)
		basic.loc[3568, 'industry'] = "100"
		pro = ts.pro_api()
		new_basic = pro.stock_basic()
		b = (basic==new_basic).apply(self.notall, axis=1)
		print(b)
		if len(new_basic)==len(basic) and all(new_basic==basic):
			self.logger.debug(self.mes1)
		elif len(new_basic)==len(basic):
			print(self.mes2+" code: ")
		

def main():
	Up = Upgrade_list("stocklist.pkl")
	Up.loger()
	Up.upgrade()


if __name__ == "__main__":
	main()
