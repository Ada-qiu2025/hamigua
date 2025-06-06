#coding=utf-8
from timeit import timeit
from timeit import Timer
import time
import urllib.request,json
import logging
import sys,os
import re
import multiprocessing
sys.path.append('E:\Pydemo\python_test\python_test')
import test_case.dispatchcenter.disPacher as dis

def parseUrl(docName,starttime):
    '''状态中心检测，如果没有，超时 抛异常'''
    if(time.time()-starttime)>3:
        raise Exception('not find Exception')
    else:
        page = urllib.request.urlopen("http://172.20.2.163:8091/list")
        hjson = json.loads(page.read())
        if (hjson.__contains__(docName)):
            Stateinfo = hjson[docName]
            logging.getLogger('login').info("doctor {} State is {}".format(docName, Stateinfo['State']))
        else:
            parseUrl(docName,starttime)

def docLogin(docName):
    '''医生登录，如果登录成功，状态中心解析状态'''
    time0 = time.time()
    if (doc.login()==0):
        parseUrl(docName,time.time())
        time1 = time.time()
        logging.getLogger('login').info('{}'.format(time1-time0))
        doc.logout()
    elif (doc.login() == -1):
        raise Exception('login failed')
    else:
        raise Exception('other exception')

if __name__ == '__main__':
    while True:
        docfh = open("E:/Pydemo/python_test/python_test/log/doclogAcct.dat", 'r').readlines()
        for name in docfh:
                name1 = name.rstrip()
                doc =dis.Doctor(name1)
                docLogin(name1)