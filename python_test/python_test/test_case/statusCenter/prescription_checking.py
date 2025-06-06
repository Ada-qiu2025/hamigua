# -*- coding:utf-8 -*-
import sys,os
sys.path.append('E:\Pydemo\python_test\python_test')
import python_test.test_case.dispatchcenter.disPacher as dis
import time
from random import randint
from multiprocessing import Process


def pres_checking(docname):
    doc = dis.Doctor(docname)
    doc.login()
    doc.pres_check('1')
    time.sleep(10)
    doc.endtask()
    doc.logout()

def mutipres_checking():
    DocNum = int(input("Doctor Total Num:"))
    DocId = int(input("Doctor Id:"))
    for i in range(DocNum):
        docname = '%s'%(DocId+i)
        p = Process(target=pres_checking(docname))
        p.start()


if __name__ == '__main__':
    mutipres_checking()