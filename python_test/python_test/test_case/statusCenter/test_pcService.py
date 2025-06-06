# encoding: utf-8

import logging.config
import configparser,urllib.request
import http.client ,json
import os

# 参数设定
headers = {'Content-Type': 'application/json'}
conn = None

# 日志配置初始化
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')

# 参数配置初始化
confile = 'sever.ini'
config = configparser.ConfigParser()
config.read(confile)
pc_ip = config.get('pcservice', 'ip')
pc_port = config.getint('pcservice', 'port')

def setup():
    global conn
    try:
        conn = http.client.HTTPConnection(pc_ip, pc_port)
    except Exception as e:
        print(e)

def test_login():
    '''药店登录'''
    logger.info('store login')
    print(u'Store Login\\n')
    param = ({"userAcct": "jinke", "password": "222222"})
    conn.request('POST', '/pcService/pc!pcDevicesLogin.ft', json.JSONEncoder().encode(param), headers)
    response = conn.getresponse()
    data = response.read()
    print(data)

def test_updateSoftVersion():
    '''测试上传版本号接口'''
    param = ({"macId": "00-30-18-04-E8-FF", "softVersion": "2.6.22.323"})
    conn.request('POST', '/pcService/pc!pcGetOnlineDoc.ft', json.JSONEncoder().encode(param), headers)
    response = conn.getresponse()
    data = response.read()

def test_pcUpdateStatus():
    '''测试上传端口的'''
    param = ({"tokenId": "00-30-18-04-E8-FF", "status": 1, "macId":"94-A1-A2-EB-EC-9F"})
    conn.request('POST', '/pcService/pc!pcUpdateStatus.ft', json.JSONEncoder().encode(param), headers)
    response = conn.getresponse()
    data = response.read()

def tear_down():
    print('teadafda')

if __name__=='__main__':
    test_pcUpdateStatus()