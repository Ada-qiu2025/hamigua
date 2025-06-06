# encoding: utf-8

from mypackage.disPacher import *
import time
import logging.config
import mypackage.stateCenter as SC
import logging.handlers
import unittest
from mypackage.D_other import *

# # # 加载日志的配置文件
logging.config.fileConfig('logging.conf')
mylogger = logging.getLogger('root')


class BasicTest(unittest.TestCase):
    def setUp(self):
        '''
        初始化,医生及药店的基本信息
        '''
        self.my_doc = Doctor()
        self.my_store = Store()

    def tearDown(self):
        if self.my_store.storestatus != Docstatus.DO_OFFLINE:
            self.my_store.logout()
            mylogger.info('药店登出')
        if self.my_doc.doc_status != Docstatus.DO_OFFLINE:
            self.my_doc.logout()
            mylogger.info('医生登出')

    def test_doc_offline(self):
        '''医生不在线 发起咨询 预期结果 不能发起请求'''
        self.my_store.store_login(mac='',docname='lxq',need_strategy=3)
        time.sleep(2)
        assert self.my_store.storestatus == self.my_store.storestatus.ST_MATCH_FAIL

    def test_doc_leave(self):
        '''医生暂离 发起咨询 预期结果 不能发起请求'''
        self.my_doc.login(account='lxq',doctype=4)
        time.sleep(1)
        self.my_doc.leave()
        time.sleep(1)
        self.my_store.store_login(mac='',docname='lxq',need_strategy=3)
        time.sleep(2)
        assert self.my_store.storestatus==self.my_store.storestatus.ST_MATCH_FAIL

    def test_receive_timeout(self):
        '''医生接受超时'''
        self.my_doc.login(account='lxq',doctype=4)
        time.sleep(5)
        self.my_store.store_login(mac='bgf',docname='lxq',need_strategy=3)
        time.sleep(5)
        assert self.my_store.storestatus==self.my_store.storestatus.ST_MATCH_SUCCESS
        time.sleep(35)#等待30s，医生没有接受业务
        print('doctor status %s' %self.my_doc.doc_status)
        print('store status %s'%self.my_store.storestatus)
        assert self.my_doc.doc_status==self.my_doc.doc_status.DO_LEAVE
        # assert self.my_store.storestatus == self.my_store.storestatus.ST_MATCH_FAIL

    def test_free_store_cancle(self):
        '''医生空闲--药店取消业务'''
        self.my_doc.login('lxq',4)
        time.sleep(2)
        self.my_store.store_login('lxq','100',3)
        time.sleep(2)
        self.my_store.endtask()
        time.sleep(2)
        assert self.my_doc.callback_Event==PharmacistCallbackEvent.PE_CLIENT_END_TASK.value

    def test_busy_store_cancle(self):
        '''医生忙碌--药店取消业务'''
        '''需要先开一个医生持续做业务,忙碌状态'''
        self.my_store.store_login('lxq','mac2',3)
        time.sleep(1)
        self.my_store.endtask()
        time.sleep(1)
        print('doc status %s' %self.my_doc.callback_Event)
        # assert self.my_doc.callback_Event==PharmacistCallbackEvent.PE_CLIENT_END_TASK.value


    def test_receive_pause(self):
        '''
        测试当随机分配药师的时候,药师的立即离开的逻辑
        此用例需要结合running
        '''
        sucess_times = 0
        fail_times = 0
        wait_times = 0

        for i in range(20):
            # running.mult_alays_busy_druggist()
            # time.sleep(30)
            self.my_doc.login('yzs', DocType.DO_TYPE_DOCTOR.DO_TYPE_DRUGGIST.value)
            # time.sleep(3)
            self.my_store.store_login(
                'yzs|yy',
                'test-mac', 7)
            self.my_doc.logout()

            # self.my_doc.pause(1)

            time.sleep(1)
            if self.my_store.storestatus == Storestatus.ST_MATCH_SUCCESS and self.my_store.doc_account == 'yzs':
                sucess_times += 1
            elif self.my_store.storestatus == Storestatus.ST_MATCH_FAIL:
                fail_times += 1
            elif self.my_store.storestatus == Storestatus.ST_WAIT:
                wait_times += 1
            else:
                print(self.my_store.storestatus)
            # assert self.my_doc.doc_status == Docstatus.DO_MATCH_SUCESS
            # assert self.my_store.storestatus == Storestatus.ST_MATCH_SUCCESS
            # time.sleep(3)
            self.my_store.logout()
            time.sleep(1)

        print('分配成功次数:%d' % sucess_times)
        print('分配失败次数:%d' % fail_times)
        print('分配等待次数:%d' % wait_times)

    def test_endtast_free(self):
        '''
        测试endtask、free命令同时过来,调度响应逻辑
        调度应该先处理endtask,再处理free命令
        测试流程:业务结束后,endtask和free一起发送
        1、计算状态中心恢复空闲状态的时间,小于10秒为正常.
        2、恢复空闲后,进行业务请求,测试是否能正常分配
        '''
        fail_times = 0
        sucess_times = 0
        for i in range(20):
            mylogger.info('开始进行第%d轮测试' % i)
            self.my_doc.login('test-1', DocType.DO_TYPE_DOCTOR.value)
            self.my_store.store_login('test-1', 'test-mac')
            time.sleep(1)
            self.my_doc.recevice('100b')
            time.sleep(5)
            self.my_doc.endtask()
            self.my_doc.free()
            self.my_store.logout()

            dur_time = SC.find_Doc('test-1', 0).__float__()

            unittest.TestCase.assertTrue(self, dur_time < 10)

            time.sleep(1)

            self.my_store.store_login('test-1', 'test-mac')
            time.sleep(2)
            unittest.TestCase.assertEqual(self, self.my_store.storestatus, Storestatus.ST_MATCH_SUCCESS)

            # unittest.TestCase.assertTrue(self, )
            self.my_doc.logout()
            self.my_store.logout()
            time.sleep(1)


def suite():
    suite_test = unittest.TestSuite()
    suite_test.addTest(BasicTest('test_endtast_free'))
    return suite_test


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
