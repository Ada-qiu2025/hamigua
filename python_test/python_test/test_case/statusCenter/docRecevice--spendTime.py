# -*- coding:utf-8 -*-
import sys
from builtins import Exception
import os
sys.path.append('E:\Pydemo\python_test\python_test')
from urllib import request
import test_case.dispatchcenter.disPacher as dis
import multiprocessing
import logging
import json
import time

def parseDocBusy(docName,startTime):

    '''忙碌状态的解析--解析状态中心医生的状态从0到2'''

    if time.time()-startTime>3:
        print('error')
        # raise Exception('no store login  requst doctor')
    else:
        page = request.urlopen('http://114.55.2.253:8091/list')
        hjson = json.loads(page.read())
        if(hjson.__contains__(docName)):
            docinfo=hjson[docName]
            docStatus = docinfo['State']
            if docStatus==2:
                logging.getLogger('doctor').info('doctor state is {}'.format(docStatus))
            else:
                time.sleep(0.01)
                parseDocBusy(docName,startTime)

def parasDocFree(docName,starttime):

    '''医生状态中心状态0 的解析，状态中心有医生数据，并且等于0，药店请求医生业务，如果没有医生数据,也许转发服务还未转发，超时之后抛异常'''

    if time.time()-starttime>2:
        raise Exception('login failed ,state center no doctor')
    else:
        page = request.urlopen('http://114.55.2.253:8091/list')
        hjson = json.loads(page.read())
        if hjson.__contains__(docName):
            dic1 = hjson[docName]
            docstate = dic1['State']
            if docstate == 0:
                cus = dis.Store('00-30-18-03-E1-7D')
                cus.store_login(docName, 3)
                freetime = time.time()
                parseDocBusy(docName, time.time())
                busytime = time.time()
                logging.getLogger('receive').info('{}'.format(busytime-freetime))
                cus.logout()
                doc.logout()
        else:
                time.sleep(0.001)
                parasDocFree(docName,starttime)

def doctorLogIn(docName,starttime):
    '''逻辑：医生登录成功，状态中心获取到医生的状态0,药店向医生发起咨询，状态中心获取到医生状态2，解析时间，状态中心获取到状态2的时间'''
    doc = dis.Doctor(docName)
    if doc.login() ==0:
        parasDocFree(docName,starttime)
    else:
        raise Exception('doctor login failed')

if __name__== '__main__':
        while True:
            docfh = open("E:/Pydemo/python_test/python_test/log/docrecevAcct.dat", 'r').readlines()
            for name in docfh:
                name1 = name.rstrip()
                doc = dis.Doctor(name1)
                doctorLogIn(name1,time.time())