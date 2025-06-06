import sys
from builtins import Exception
import os

sys.path.append('E:\Pydemo\python_test\python_test')
from urllib import request
import test_case.dispatchcenter.disPacher as dis
import multiprocessing
from timeit import Timer
from timeit import timeit
import logging
import json
import time

def parselogout(docName,starttime):
    '''状态中心，检验，是否还有医生信息，如果没有,logout成功，并且状态解析不到，写入日志，如果有，等待时间不超过三秒，超时之后抛异常'''
    if time.time()-starttime>3:
        raise Exception('other process doctor login doctor')
    else:
        page = request.urlopen('http://172.20.2.163:8091/list')
        hjson = json.loads(page.read())
        if (not hjson.__contains__(docName)):
            logging.getLogger('logout').info('logout success,center no doc information')
        else:
            parselogout(docName,starttime)

def parseDocFree(docName,starttime):
    '''状态中心校验，如果状态空闲，调用登出，再次状态中心检测';如果没有检测到状态也许是转发服务还为转发,超时抛异常,解析的时间：登出之后的时间'''
    if time.time()-starttime>1:
        raise Exception('time out')
    else:
        page = request.urlopen('http://172.20.2.163:8091/list')
        hjson = json.loads(page.read())
        if hjson.__contains__(docName):
            docinfo = hjson[docName]
            logging.getLogger('logout').info('{} state is {}'.format((docName),docinfo['State']))
            t0 = time.time()
            if doc.logout()==0:
                    parselogout(docName,time.time())
                    t1 = time.time()
                    logging.getLogger('logout').info('{}'.format(t1-t0))
            elif doc.logout()==-1:
                    raise Exception('logout failed')
            else:
                    raise Exception('other exception')
        else:
                time.sleep(0.001)
                parseDocFree(docName,starttime)

def docLogout(docName):
    '''医生登录，'''
    if doc.login()==0:
        parseDocFree(docName,time.time())
    else:
        raise Exception('doctor login failed')

if __name__ == '__main__':
    while True:
        docfh = open("E:/Pydemo/python_test/python_test/log/docloutAcct.dat", 'r').readlines()
        for name in docfh:
            name1 = name.rstrip()
            doc = dis.Doctor(name1)
            docLogout(name1)