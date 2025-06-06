# -*- coding:utf-8 -*-
import sys,os
sys.path.append('E:\Pydemo\python_test\python_test')
import python_test.test_case.dispatchcenter.disPacher as dis
import time
import urllib
import json
from random import randint


headers={'Content-Type': 'text/html','charset':'utf-8','Connection': 'keep-alive'}


def store_heart():
    '''400药店发送心跳同时'''


def requst_doctor():
    # '''获取一次医生列表'''

    time.sleep(randint(5,10))
    # 获取三次医生状态
    time.sleep(1)
    #adsum 广告统计
    adId = 12503
    playNum = 5
    groupIp = 20
    param = {"tokenId":"tokenId","adInfos":[{"adId":adId,"playNum":playNum,"groupId":groupIp},{"adId":adId,"playNum":playNum,"groupId":groupIp}]}
    conn = urllib.request.Request('http://172.20.2.163:80/adSum/ad/sum',
                                  bytes(json.dumps(param), 'utf8'), headers, method='POST')
    response = urllib.request.urlopen(conn)
    page = response.read()
    page = page.decode('utf-8')
    print(page)
    #提交评价


def  request_drug_history():
    '''300 获取推药历史'''



def request_cunsult_history():
    '''200个用户不断访问咨询历史'''


def blind_prescipiton():
    '''100绑定处方'''



