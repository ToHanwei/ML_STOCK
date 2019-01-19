from sklearn import svm
import DC
import numpy as np

if __name__ == '__main__':
	stock = '603912.SH'
	dc = DC.data_collect(stock, '2010-01-01', '2018-12-12')
	train = dc.data_train
	target = dc.data_target
	#test_case = [dc.test_case]
	model = svm.SVC()               # 建模
	model.fit(train, target)        # 训练
	#for line in dc.test_case:
	#	ans2 = model.predict([line]) # 预测
	#	# 输出对2018-03-02的涨跌预测，1表示涨，0表示不涨。
	#	print(ans2[0])
	#print(type(line))
	print(dc.abc)
	ans2 = model.predict([np.array([0., 0., 0., 0., 0., 0.])]) # 预测
	# 输出对2018-03-02的涨跌预测，1表示涨，0表示不涨。
	print(ans2[0])

