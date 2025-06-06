# encoding: utf-8
from ctypes import *
import time
import pymysql
from multiprocessing import *
from Doctor import *

def DoMySql(Number):
    conn = pymysql.connect(host='172.20.1.100', port=3306, user='root', passwd='Pass1234', db='hospital')  # db：库名
    cur = conn.cursor()

    cur.execute("select account,type from b_doctor where type = 1 order by account desc")
    ret1 = cur.fetchall()
    cur.close()
    conn.close()

    if (ret1.__len__() - Number) > 0 :
        return ret1[ret1.__len__() - Number]
    else:
        print("The Number is too large.")
        return 0

def get(name):
    d = Doctor()
    d.login(name,4)
    while True:
        time.sleep(10)
        if(d.DcoStatus == 1):
            d.recevice(b"101")
            d.DcoStatus = 2
            time.sleep(30)
        elif(d.DcoStatus == 2):
            d.endTask()
            d.free()
            d.DcoStatus = 3

if(__name__ == '__main__'):
    #get("bairuijie")
    for i in range(1,10):
        DocId = DoMySql(i)[0].encode("utf-8")
        p = Process(target=get, args=(DocId,))
        p.start()
        time.sleep(2)