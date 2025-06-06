# encoding: utf-8
import configparser
import logging
import logging.config
import time
from ctypes import *
from enum import Enum
import os
import sys
sys.path.append('E:\Pydemo\python_test\python_test')
import test_case.dispatchcenter.mysql_db

os.chdir('E:/Pydemo/python_test/python_test/')
#读取log文件的配置格式
logging.config.fileConfig('logging.conf')

# 读取配置文件的信
confile = 'sever.ini'
config = configparser.ConfigParser()
config.read(confile)
_dis_ip = config.get('disCenter', 'ip')    # 调度服务地址
_dis_port = config.getint('disCenter', 'port')  # 调度服务端口
os.chdir('E:/Pydemo/python_test/python_test/')
dllpath = './dll/'  # config.get('sdk', 'path')    # 调度sdk所在路径

# 加载需要用到的sdk信息
cdll.LoadLibrary(dllpath+'opus.dll')
cdll.LoadLibrary(dllpath+'avutil-52.dll')
cdll.LoadLibrary(dllpath+'libcurl.dll')
cdll.LoadLibrary(dllpath+'swresample-0.dll')
cdll.LoadLibrary(dllpath+'swscale-2.dll')
cdll.LoadLibrary(dllpath+'avcodec-54.dll')
cdll.LoadLibrary(dllpath+'avformat-54.dll')
cdll.LoadLibrary(dllpath+'pcav.dll')
cdll.LoadLibrary(dllpath+'ftcodec.dll')


# 医生回调的枚举类型
class PharmacistCallbackEvent(Enum):
    PE_MATCH_SUCCEED = 0  # 匹配成功	intValue:用户类型 0线下端 1移动端 stringValue:（线下端）药店ID jsonValue:(手机端)手机信息
    PE_AV_CONTROL = 1  # 音视频控制	stringValue:  jsonValue: 控制音视频信息
    PE_FILE_URL = 2  # 图片通知  stringValue:图片url
    PE_GPS_INFO = 3  # GPS信息   jsonValue:
    PE_CLIENT_END_TASK = 4  # 客户结束业务
    PE_CLIENT_OFFLINE = 5  # 客户掉线
    PE_CLIENT_EXCEPTION_END = 6  # 客户异常断开
    PE_DISCONNECTED = 7  # 与接入服务断开连接
    PE_UDP_ESTABLISH = 8  # UDP链接建立成功
    PE_LEAVE = 9
    PE_PUSH_MESSAGE = 10  # 图文消息信息
    PE_WAIT = 11  # 排队客户数


# 医生的状态的枚举
class Docstatus(Enum):
    DO_OFFLINE = 0  # 离线
    DO_MATCH_SUCESS = 1  # 已分配待接收业务
    DO_BUSY = 2  # 忙碌
    DO_FREE = 3  # 空闲
    DO_LEAVE = 4  # 离开
    DO_STORE_ENDCALL = 5  # 药店挂断业务


class Doctor:
    def __init__(self, account):
        """初始化医生基本信息,当数据库中没有医生时则初始化不成功"""
        mydo = test_case.dispatchcenter.mysql_db.MyDao()
        self._docInfo = mydo.get_docinfo(account)

        if self._docInfo:
            self.__service_id = mydo.get_docservice(account)
            self.DcoStatus = Docstatus.DO_OFFLINE
            self.is_Pause = 0  # 是否暂离
            self.loginTime = None  # 医生登录时间
            self.PauseTime = None  # 医生暂离时间点
            self.waitNum = 0  # 等待人数
            logging.getLogger('doctor').info('init Doctor\'s information.')

            """初始化sdk并注册回调函数"""
            self.__DllObj = cdll.LoadLibrary(dllpath+'consult_client_sdk.dll')
            self.__DllObj.ConsultSdkInit()
            self.__CFUNC = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_int, c_char_p, c_int, c_void_p)
            # self.__CFUNB = WINFUNCTYPE(None, c_int, c_char_p, c_void_p)
            self.__CBE = self.__CFUNC(self.callbackevent)
            # self.__CBEB = self.__CFUNB(self.logcallback)
            # self.reglogcallback()
            logging.getLogger('doctor').info('init sdk and regdit the callback')
        else:
            print("The Doc's account is not correct!")

    def pres_check(self,result):
        '''发送处方审核结果'''
        if (self.__DllObj.PharmacistPrescriptionCheckResult(result.encode('utf-8'))==0):
            logging.getLogger('doctor').info("%s prescipition success" % (self._docInfo['account']))
        else:
            logging.getLogger('doctor').info("%s prescipition failed" % (self._docInfo['account']))

    def login(self):
        """医生登录调度服务"""
        if (self.__DllObj.PharmacistLogin(_dis_ip.encode('utf-8'), _dis_port,
                                          self._docInfo['full_name'].encode('utf-8'),
                                          self._docInfo['plat_name'].encode('utf-8'),
                                          self._docInfo['account'].encode('utf-8'),
                                          self._docInfo['type'], self._docInfo['server_type'], self.__CBE, None,
                                          1) == 0):
            self.loginTime = time.time()
            self.DcoStatus = Docstatus.DO_FREE
            logging.getLogger('doctor').warning(" %s has logined sucessfully." % (self._docInfo['account']))
            return 0
        else:
            logging.getLogger('doctor').error("%s LOGIN FAIL" % (self._docInfo['account']))
            return -1

    def logout(self):
        """登出调度服务"""
        if self.__DllObj.PharmacistLogout() == 0:
            logging.getLogger('doctor').warning("%s, has logouted sucessfully" % (self._docInfo['account']))
            self.DcoStatus = Docstatus.DO_OFFLINE
            return 0
        else:
            logging.getLogger('doctor').info("%s, logOUT FAIL") % (self._docInfo['account'])
            return -1

    # def reglogcallback(self):
    #     """注册回调函数"""
    #     self.__DllObj.ConsultSetLogMsgCallback(self.__CBEB, None)

    # @staticmethod
    # def logcallback(self, intval, charval, puser):
    #     """注册日志回调函数"""
    #     logging.getLogger('doctor').info(intval.__str__() + charval.decode("gb2312"))

    def leave(self):
        """暂时离开"""
        if self.__DllObj.PharmacistToLeave() == 0:
            logging.getLogger('doctor').warning("%s ,is leave.." % (self._docInfo['account']))
            self.DcoStatus = Docstatus.DO_LEAVE
        else:
            logging.getLogger('doctor').error("%s ,Leave FAIL" % (self._docInfo['account']))

    def free(self):
        if self.__DllObj.PharmacistFree() == 0:
            self.DcoStatus = Docstatus.DO_FREE
            logging.getLogger('doctor').warning("%s ,is free.." % (self._docInfo['account']))
        else:
            logging.getLogger('doctor').error("%s ,free fail." % (self._docInfo['account']))

    def recevice(self, busiid=b'100'):
        """接受业务"""
        if self.__DllObj.PharmacistReceiveTask(busiid) == 0:
            self.DcoStatus = Docstatus.DO_BUSY
            logging.getLogger('doctor').warning("%s ,is recevice task.." % (self._docInfo['account']))
        else:
            logging.getLogger('doctor').error("%s ,recevice task fail." % (self._docInfo['account']))

    def endtask(self):
        """停止业务"""
        if self.__DllObj.PharmacistEndTask() == 0:
            self.free()
            logging.getLogger('doctor').warning("%s ,is endTask.." % (self._docInfo['account']))
        else:
            logging.getLogger('doctor').error("%s ,endTask fail." % (self._docInfo['account']))

    # def printLog(self):
    #     # mySql.updateDocLog(self.logTime)
    #     logging.getLogger('doctor').info(self._docInfo['account'] + self.DcoStatus.__str__() + self.logTime.__str__())
    #     return self.logTime

    # 医生暂离
    def pause(self, val):
        if self.__DllObj.PharmacistPauseService(val) == 0:
            self.PauseTime = time.time()
            self.is_Pause = val
            logging.getLogger('doctor').info("%s ,is Pause..%d" % (self._docInfo['account'], int(val)))
        else:
            logging.getLogger('doctor').error("%s ,Pause fail." % (self._docInfo['account']))

    # 事件回调
    def callbackevent(self, event, intval, strvalue, strlen, jsonval, jsonlen, puser):
        if event == PharmacistCallbackEvent.PE_MATCH_SUCCEED.value:  # 匹配成功
            self.DcoStatus = Docstatus.DO_MATCH_SUCESS
            logging.getLogger('doctor').info("%s ,has be assign.." % (self._docInfo['account']))
        elif event == PharmacistCallbackEvent.PE_FILE_URL.value:
            pass
        elif event == PharmacistCallbackEvent.PE_GPS_INFO.value:
            pass
        elif event == PharmacistCallbackEvent.PE_CLIENT_END_TASK.value:  # 客户端结束业务
            self.free()
            logging.getLogger('doctor').info("%s ,has be clientEndTaskTime.." % (self._docInfo['account']))
        elif event == PharmacistCallbackEvent.PE_CLIENT_OFFLINE.value:  # 客户端掉线
            self.free()
            logging.getLogger('doctor').info("%s ,has be clientLogoutTime.." % (self._docInfo['account']))
        elif event == PharmacistCallbackEvent.PE_CLIENT_EXCEPTION_END.value:  # 客户端网络异常
            self.free()
            logging.getLogger('doctor').info("%s ,has be clientNetErrorTime.." % (self._docInfo['account']))
        elif event == PharmacistCallbackEvent.PE_LEAVE.value:  # 医生超时未接业务,暂时离线
            self.DcoStatus = Docstatus.DO_LEAVE
            logging.getLogger('doctor').info("%s ,has be leave.." % (self._docInfo['account']))
        elif event == PharmacistCallbackEvent.PE_WAIT.value:  # 排队人数变动回调
            self.waitNum = int(intval)
            logging.getLogger('doctor').info("%s ,has be waitchanged.." % (self._docInfo['account']))
        elif event == PharmacistCallbackEvent.PE_DISCONNECTED.value:  # 与调度服务断开
            self.DcoStatus = Docstatus.DO_OFFLINE
            logging.getLogger('doctor').warning("%s ,has be logout.." % (self._docInfo['account']))
        elif event == PharmacistCallbackEvent.PE_AV_CONTROL.value:
            pass
        elif event == PharmacistCallbackEvent.PE_PUSH_MESSAGE.value:
            pass
        else:
            pass


# 用户回调事件
class CustomCallbackEvent(Enum):
    CE_MATCH_FAILED = 0  # 匹配失败
    CE_MATCH_SUCCEED = 1  # 匹配成功
    CE_MATCH_WAIT = 2  # 排队等候中
    CE_DRUGGIST_RECV_TASK = 3  # 医药师已接受任务
    CE_DRUGGIST_END_TASK = 4  # 医药师结束业务
    CE_DRUGGIDO_OFFLINE = 5  # 医药师断线
    CE_DRUGGIST_EXCEPTION_END = 6  # 医药师异常断开
    CE_DISCONNECTED = 7  # 与接入服务断开连接
    CE_UDP_ESTABLISH = 8  # UDP链接建立成功
    CE_PUSH_DRUG = 9  # 推荐药品
    CE_LEAVE = 10
    CE_SCREENSHOT = 11  # 截图成功回调
    # CE_PRESCRIPT_CHECK = 12  # 处方审核结果
    CE_LOGIN_SUCCEED = 13  # 登录成功
    CE_PRESCRIPT_CHECK = 29  # 处方审核结果


# 药店的状态
class Storestatus(Enum):
    ST_OFFLINE = 0  # 药店离线
    ST_WAIT = 1   # 药店在等待状态
    ST_MATCH_SUCCESS = 2   # 等待接收业务
    ST_MATCH_FAIL = 3   # 匹配失败
    ST_BUSY = 4  # 忙碌,业务中
    ST_LEAVE = 5  # 医生离开
    ST_DOC_ENDCALL = 6  # 医生断线,挂断业务或者异常离开


class Store:
    def __init__(self, mac, confile='../../sever.ini'):
        mydo = test_case.dispatchcenter.mysql_db.MyDao()
        self._storeinfo = mydo.get_stroreinfo(mac)
        self.__mac = mac
        self.waitNum = 0
        self.storestatus = Storestatus.ST_OFFLINE

        if self._storeinfo:
            # 加载动态库及注册回调函数
            self.__Objdll = cdll.LoadLibrary(dllpath+'consult_client_sdk.dll')
            self.__Objdll.ConsultSdkInit()
            self.__CFUNA = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_char_p, c_void_p)
            # self.__CFUNB = WINFUNCTYPE(None, c_int, c_char_p, c_void_p)
            self.__PA = self.__CFUNA(self.customercallback)
            # self.__PB = self.__CFUNB(logCallback)
        else:
            print("The mac \'%s\' info is not found." % mac)

    # //need_strategy 分配策略 1随机医生 2随机药师 3指定医生 4指定药师
    # //need_druggist_id 需要的医生和药师ID need_strategy需要为3或者4
    # //only_prescription_checking	请求电子审方,不是则为0
    def store_login(self, docname, need_strategy, busi_id=100, json_str="{}".encode('utf-8'),
                    device_type='pad', hospital_id=0, only_prescription_checking=0):
        if (self.__Objdll.CustomLogin(_dis_ip.encode('utf-8'), _dis_port,
                                      self._storeinfo['cn_name'].encode('utf-8'),
                                      self.__mac.encode('utf-8'), bytes(self._storeinfo['store_id']),
                                      need_strategy, docname.encode('utf-8'), hospital_id, only_prescription_checking,
                                      busi_id, json_str, device_type.encode('utf-8'),
                                      self.__PA, None, 1)==0):
            self.starttime = time.time()
            # logging.getLogger('root').info("store :%s is login ,request doctor :%s"%(self.__mac,docname))
            # self.reglogCallback()
        else:
            logging.getLogger('root').error("STORE: %s LOGIN FAIL"%(self.__mac,docname))

    def customHeart(self):
        '''药店发送心跳'''
        self.__Objdll.CustomHeartbeat()

    def reglogcallback(self):
        self.__Objdll.ConsultSetLogMsgCallback(self.__PB, None)

    def customercallback(self, event, intval, strvalue, jsonval, puser):
        if event == CustomCallbackEvent.CE_MATCH_FAILED.value:
            costtime = time.time() - self.starttime
            self.storestatus = Storestatus.ST_MATCH_FAIL
            if costtime > 2:
               logging.getLogger("root").error('match cost time %f', time.time() - self.starttime)
            else:
                logging.getLogger("root").info('login cost time %f', time.time() - self.starttime)
        elif event == CustomCallbackEvent.CE_MATCH_SUCCEED.value:  # 匹配成功
            costtime = time.time() - self.starttime
            self.storestatus = Storestatus.ST_MATCH_SUCCESS
            if costtime > 2:
              logging.getLogger("root").error('match cost time %f', time.time() - self.starttime)
            else:
                logging.getLogger("root").info('login cost time %f', time.time() - self.starttime)
        elif event == CustomCallbackEvent.CE_DRUGGIST_RECV_TASK.value:  # 医生接受业务
            self.storestatus = Storestatus.ST_BUSY
        elif event == CustomCallbackEvent.CE_MATCH_WAIT.value:  # 排队等待
            self.storestatus = Storestatus.ST_WAIT
            self.waitNum = int(intval)
        elif event == CustomCallbackEvent.CE_DRUGGIST_END_TASK.value or event == \
                CustomCallbackEvent.CE_DRUGGIST_EXCEPTION_END.value\
                or event == CustomCallbackEvent.CE_DRUGGIDO_OFFLINE.value:
            self.storestatus = Storestatus.ST_DOC_ENDCALL
        elif event == CustomCallbackEvent.CE_DISCONNECTED.value:
            self.storestatus = Storestatus.ST_OFFLINE
        elif event == CustomCallbackEvent.CE_LEAVE.value:
            self.storestatus = Storestatus.ST_LEAVE
        elif event==CustomCallbackEvent.CE_PRESCRIPT_CHECK.value:
            print('prescepition send sucess,event value is 29')
        # elif event == CustomCallbackEvent.CE_LOGIN_SUCCEED.value:
        #     logincosttime = time.time() - self.starttime
        #     if logincosttime > 2:
        #         logging.getLogger("root").error('%s ,login cost time %f', self.__mac, logincosttime)
        #     else:
        #         logging.getLogger("root").info('%s , login cost time %f', self.__mac, logincosttime)

    def endtask(self):
        self.__Objdll.CustomEndTask()

    def logout(self):
        self.__Objdll.CustomLogout()

    def endtask(self):
        self.__Objdll.CustomEndTask()


def getDoclist():
    mydo = test_case.dispatchcenter.mysql_db.MyDao()
    return mydo.get_doclist()


def getstorelist():
    mydo = test_case.dispatchcenter.mysql_db.MyDao()
    return mydo.get_storelist()
