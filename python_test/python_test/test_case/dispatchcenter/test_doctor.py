# encoding: utf-8

import time
import unittest
import nose
import logging
import python_test.test_case.dispatchcenter.disPacher as  dis

logger = logging.getLogger('test_doctor')


'''指定医生信息，药店信息'''
doc=dis.Doctor('lxq')
store = dis.Store('B8-97-5A-A5-B1-88')

def setUp():
    doc.login()

def tearDown():
    doc.logout()
    store.logout()

    # 测试医生在空闲时,暂时离开的情况
def test_docpause_free_fales():
    '''TEST测试用户暂停失败'''
    # 医生初始化登录时候的状态及排队数
    assert doc.DcoStatus == dis.Docstatus.DO_FREE
    assert doc.waitNum == 0

    # 当医生暂离的时候,业务请求无法分配
    doc.pause(True)
    store.store_login("lxq", 3)
    time.sleep(2)
    assert store.storestatus == dis.Storestatus.ST_MATCH_FAIL
    store.logout()

    # 当恢复暂时离开的时候,业务请求可以分配
    doc.pause(False)
    store.store_login("lxq", 3)
    time.sleep(2)
    assert store.storestatus ==  dis.Storestatus.ST_MATCH_SUCCESS

def test_doc_free():
    store.store_login("lxq",3)
    time.sleep(2)
    assert doc.DcoStatus == dis.Docstatus.DO_MATCH_SUCESS
    #医生接受业务
    doc.recevice('15425')
    # 再次咨询
    store.store_login('lxq',3)
    time.sleep(2)
    #医生状态忙碌
    assert doc.DcoStatus == dis.Docstatus.DO_BUSY
    assert doc.waitNum == 1

def test_doc_busi():
    pass







