# -*- coding:utf8 -*-
import numpy as np
import pymysql


class data_collect(object):

    def __init__(self, in_code,start_dt,end_dt):
        ans = self.collectDATA(in_code,start_dt,end_dt)

    def collectDATA(self,in_code,start_dt,end_dt):
        db = pymysql.connect(host='localhost', user='root', passwd='hanwei1', db='stock', charset='utf8')
        cursor = db.cursor()
        sql_done_set = "SELECT * FROM stock_all a where stock_code = '%s' and state_dt >= '%s' and state_dt <= '%s' order by state_dt asc" % (in_code, start_dt, end_dt)
        cursor.execute(sql_done_set)
        done_set = cursor.fetchall()
        if len(done_set) == 0:
            raise ValueError("Something Error!")
        self.date_seq = []
        self.open_list = []
        self.close_list = []
        self.high_list = []
        self.low_list = []
        self.vol_list = []
        self.amount_list = []
        for i in range(len(done_set)):
            self.date_seq.append(done_set[i][0])
            self.open_list.append(float(done_set[i][2]))
            self.close_list.append(float(done_set[i][3]))
            self.high_list.append(float(done_set[i][4]))
            self.low_list.append(float(done_set[i][5]))
            self.vol_list.append(float(done_set[i][6]))
            self.amount_list.append(float(done_set[i][7]))
        cursor.close()
        db.close()
        self.data_train = []
        self.data_target = []
        self.data_target_onehot = []
        self.cnt_pos = 0
        self.test_case = []
        self.abc = []

        for i in range(0,len(self.close_list)-1):
        #for i in range(0,int(len(self.close_list)/2)):
            train = [self.open_list[i],self.close_list[i],self.high_list[i],self.low_list[i],self.vol_list[i],self.amount_list[i]]
            self.data_train.append(np.array(train))

            if self.close_list[i+1]/self.close_list[i] > 1.0:
                self.data_target.append(float(1.00))
                self.data_target_onehot.append([1,0,0])
            else:
                self.data_target.append(float(0.00))
                self.data_target_onehot.append([0,1,0])
        for i in range(int(len(self.close_list)/2), len(self.close_list)-1):
            test = [self.open_list[i],self.close_list[i],self.high_list[i],self.low_list[i],self.vol_list[i],self.amount_list[i]]
            self.test_case.append(np.array(test)) 
            if self.close_list[i+1]/self.close_list[i] > 1.0:
                self.abc.append(float(1.00))
            else:
                self.abc.append(float(0.00))
        self.cnt_pos =len([x for x in self.data_target if x == 1.00])
        #self.test_case = np.array([self.open_list[-1],self.close_list[-1],self.high_list[-1],self.low_list[-1],self.vol_list[-1],self.amount_list[-1]])
        self.data_train = np.array(self.data_train)
        self.data_target = np.array(self.data_target)
        return 1
