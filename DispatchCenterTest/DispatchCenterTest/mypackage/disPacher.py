# encoding: utf-8
import ConfigParser
import logging
import time
from ctypes import *
from enum import Enum
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 读取配置文件的信息
os.chdir('E:\Pydemo\DispatchCenterTest\DispatchCenterTest')
confile = 'sever.ini'
config = ConfigParser.ConfigParser()
config.read(confile)
_dis_ip = config.get('disCenter', 'ip')    # 调度服务地址
_dis_port = config.getint('disCenter', 'port')  # 调度服务端口
dllpath = './dll/'  # config.get('sdk', 'path')    # 调度sdk所在路径

# # 加载需要用到的sdk信息
cdll.LoadLibrary(dllpath+'opus.dll')
cdll.LoadLibrary(dllpath+'avutil-52.dll')
cdll.LoadLibrary(dllpath+'libcurl.dll')
cdll.LoadLibrary(dllpath+'swresample-0.dll')
cdll.LoadLibrary(dllpath+'swscale-2.dll')
cdll.LoadLibrary(dllpath+'avcodec-54.dll')
cdll.LoadLibrary(dllpath+'avformat-54.dll')
cdll.LoadLibrary(dllpath+'pcav.dll')
cdll.LoadLibrary(dllpath+'ftcodec.dll')
cdll.LoadLibrary(dllpath+'fdfs_win_client')


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
    PE_CUSTOM_SEND_CUSTOM_MSG =12 #custome_senddrugmsg


# 医生的状态的枚举
class Docstatus(Enum):
    DO_OFFLINE = 0  # 离线
    DO_MATCH_SUCESS = 1  # 已分配待接收业务
    DO_BUSY = 2  # 忙碌
    DO_FREE = 3  # 空闲
    DO_LEAVE = 4  # 离开
    DO_STORE_ENDCALL = 5  # 药店挂断业务


# //druggist_type 医生或药师类型 0中药师 1西药师 2执业中药师 3执业西药师 4医生
class DocType(Enum):
    DO_TYPE_DRUGGIST = 1  # 药师
    DO_TYPE_DOCTOR = 4  # 医生


# //need_strategy 分配策略 1随机医生 2随机药师 3指定医生 4指定药师
class Need_Strategy(Enum):
    STRATEGY_RD_DOC = 1
    STRATEGY_RD_DRUGGIST = 2
    STRATEGY_FIXED_DOC = 3
    STRATEGY_FIXED_DRUGGIST = 4
    STRATEGY_RD_ZDRUGGIST=5
    STRATEGY_RD_WDRUGGIST=6
    ASSIGN_DRUGGIST_EX = 7


class Doctor:
    def __init__(self, isprintlog=False):   # False 屏蔽回调日志打印信息
        # self.__service_id = mydo.get_docservice(account)
        self.doc_status = Docstatus.DO_OFFLINE
        self.is_Pause = None  # 是否暂离
        self.loginTime = None  # 医生登录时间
        self.PauseTime = None  # 医生暂离时间点
        self.waitNum = None  # 等待人数
        self.Account = None  # 医生的账号
        self.callback_Event = None  # 医生的回调事件
        self.callbackEnd_Time = None  # 最后一次回调事件的时间 客户端结束业务
        self.startwort_time = None # 开始业务时间
        self.leave_time = None # 离开的时间
        self.callback_Time =None #最后一次回调事件的时间

   #     """初始化sdk并注册回调函数"""
        self.__DllObj = cdll.LoadLibrary(dllpath+'consult_client_sdk.dll')
        self.__DllObj.ConsultSdkInit()
        self.__CFUNC = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_int, c_char_p, c_int, c_void_p)
        self.__CBE = self.__CFUNC(self.callbackevent)

        # 为True则会注册日志回调函数,默认不注册日志回调
        if not isprintlog:
            self.__CFUNB = WINFUNCTYPE(None, c_int, c_char_p, c_void_p)
            self.__CBEB = self.__CFUNB(self.nologCallback)
            # self.reglogcallback()

    def login(self,account,doctype=DocType.DO_TYPE_DRUGGIST,fullname='ft_Test',platname='FT',servertype=1):
  #      """医生登录调度服务"""
        self.Account = account  # 医生账号初始化
        rs = self.__DllObj.PharmacistLogin(_dis_ip.encode('utf-8'), _dis_port,
                                           fullname.encode('utf-8'),
                                           platname.encode('utf-8'),
                                           account.encode('utf-8'),
                                           doctype, servertype, self.__CBE, None, 1)
        if rs == 0:
            self.loginTime = time.time()
            self.is_Pause = False
            self.doc_status = Docstatus.DO_FREE
            self.waitNum = 0
            logging.getLogger('root').info("Doctor %s has logined sucessfully."%(self.Account))
            return True
        else:
            logging.getLogger('root').error("Doctor %s LOGIN FAIL,code:%d" % (self.Account,rs))
            return False

    def logout(self):
    #    """登出调度服务"""
        rs = self.__DllObj.PharmacistLogout()
        if rs == 0:
            logging.getLogger('root').info("Doctor:%s has logouted sucessfully" % (self.Account))
            self.doc_status = Docstatus.DO_OFFLINE
            return True
        else:
            logging.getLogger('root').info("Doctor:%s logOUT FAIL..,code:%d") % (self.Account,rs)
            return False

    # 注册日志回调
    def reglogcallback(self):
    #    """注册回调函数"""
        rs = self.__DllObj.ConsultSetLogMsgCallback(self.__CBEB, None)
        if rs == 0:
            logging.getLogger('root').info("reglogcallback suceessful")
            return True
        else:
            logging.getLogger('root').error("reglogcallback fail ,code:%d")
            return False

    # @staticmethod
    # def logcallback(self, intval, charval, puser):
    #     """注册日志回调函数"""
    #     logging.getLogger('root').info(intval.__str__() + charval.decode("gb2312"))

    def leave(self):
    #    """暂时离开"""
        rs = self.__DllObj.PharmacistToLeave()
        if rs == 0:
            logging.getLogger('root').info("Doctor:%s ,is leave.." % (self.Account))
            self.doc_status = Docstatus.DO_LEAVE
            self.leave_time = time.time()
            return True
        else:
            logging.getLogger('root').error("Doctor:%s ,Leave FAIL,code:%d"% (self.Account,rs))
            return False

    def free(self):
    #    '''空闲通知'''
        rs = self.__DllObj.PharmacistFree()
        if rs == 0:
            self.doc_status = Docstatus.DO_FREE
            logging.getLogger('root').info("Doc:%s ,is free.." % (self.Account))
            return True
        else:
            logging.getLogger('root').error("Doc:%s ,free fail.code:%d" % (self.Account,rs))
            return False

    def recevice(self, busiid=b'100'):
    #    """接受业务"""
        rs = self.__DllObj.PharmacistReceiveTask(busiid)
        if rs == 0:
            self.doc_status = Docstatus.DO_BUSY
            self.startwort_time = time.time()
            logging.getLogger('root').info("Doctor:%s ,is recevice task.." % (self.Account))
            return True
        else:
            logging.getLogger('root').error("Doctor:%s ,recevice task fail..code:%d" % (self.Account,rs))
            return False

    def endtask(self):
    #    """停止业务"""
        rs = self.__DllObj.PharmacistEndTask()
        if rs == 0:
            logging.getLogger('root').info("Doctor:%s ,is endTask.." % (self.Account))
            return True
        else:
            logging.getLogger('root').error("Doctor:%s ,endTask fail..code:%d" % (self.Account,rs))
            return False

    def pres_check(self, result):
     #       '''发送处方审核结果'''
            if (self.__DllObj.PharmacistPrescriptionCheckResult(result.encode('utf-8')) == 0):
                logging.getLogger('doctor').info("%s prescipition success" % (self.Account))
                return 0
            else:
                logging.getLogger('doctor').info("%s prescipition failed" % (self.Account))
                return -1
    # 医生暂离
    def pause(self, val):
        rs = self.__DllObj.PharmacistPauseService(val)
        if rs == 0:
            self.PauseTime = time.time()
            self.is_Pause = val
            logging.getLogger('root').info("Doctor:%s ,is Pause..%d" % (self.Account, int(val)))
            return True
        else:
            logging.getLogger('root').error("Doctor:%s ,Pause fail..%d" % (self.Account,rs))
            return False

    # 不打印日志
    def nologCallback(self, intval, charval, pUser):
     #   '''不打印日志'''
        pass

    def callbackevent(self, event, intval, strvalue, strlen, jsonval, jsonlen, puser):
    #    '''事件回调函数'''

        # 记录事件及时间
        self.callback_Event = event

        if event == PharmacistCallbackEvent.PE_MATCH_SUCCEED.value:  # 匹配成功
            self.doc_status = Docstatus.DO_MATCH_SUCESS
        elif event == PharmacistCallbackEvent.PE_FILE_URL.value:
            pass
        elif event == PharmacistCallbackEvent.PE_GPS_INFO.value:
            pass
        elif event == PharmacistCallbackEvent.PE_CLIENT_END_TASK.value:  # 客户端结束业务
            self.free()
            self.callbackEnd_Time=time.time()
            logging.getLogger('root').info("%s ,has be clientEndTask.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_CLIENT_OFFLINE.value:  # 客户端掉线
            self.free()
            logging.getLogger('root').info("%s ,has be clientLogout.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_CLIENT_EXCEPTION_END.value:  # 客户端网络异常
            self.free()
            logging.getLogger('root').info("%s ,has be clientNetError.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_LEAVE.value:  # 医生超时未接业务,暂时离线
            self.doc_status = Docstatus.DO_LEAVE
            self.leave_time = time.time()
            logging.getLogger('root').info("%s ,has be leave.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_WAIT.value:  # 排队人数变动回调
            self.waitNum = int(intval)
            # logging.getLogger('root').info("%s ,has be waitchanged.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_DISCONNECTED.value:  # 与调度服务断开
            self.doc_status = Docstatus.DO_OFFLINE
            logging.getLogger('root').debug("%s ,has be logout.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_AV_CONTROL.value:
            pass
        elif event == PharmacistCallbackEvent.PE_PUSH_MESSAGE.value:
            pass
        elif event ==12: #接收业务
            self.callback_Time=time.time()
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
    CE_LEAVE = 10  # 医生离开
    CE_SCREENSHOT = 11  # 截图成功回调
    CE_PRESCRIPT_CHECK = 12  # 处方审核结果
    CE_LOGIN_SUCCEED = 13  # 登录成功


# 药店的状态
class Storestatus(Enum):
    ST_OFFLINE = 0  # 药店离线
    ST_WAIT = 1   # 药店在等待状态
    ST_MATCH_SUCCESS = 2   # 等待接收业务
    ST_MATCH_FAIL = 3   # 匹配失败
    ST_BUSY = 4  # 忙碌,业务中
    ST_LEAVE = 5  # 医生离开
    ST_DOC_ENDCALL = 6  # 医生断线,挂断业务或者异常离开
    ST_LOGIN_DISPATCH = 7 # 药店登录调度服务


class Store:
    callback_Time = None
    def __init__(self, isprintlog=False):
        # mydo = test_case.dispatchcenter.mysql_db.MyDao()
        # self._storeinfo = mydo.get_stroreinfo(mac)
        self.__mac = None
        self.waitNum = None
        self.storestatus = Storestatus.ST_OFFLINE
        self.loginTime = None
        self.callback_Event = None  # 回调的类型
        self.callback_Time=None  # 回调的时间

        # 加载动态库及注册回调函数
        self.__Objdll = cdll.LoadLibrary(dllpath+'consult_client_sdk.dll')
        self.__Objdll.ConsultSdkInit()
        self.__CFUNA = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_char_p, c_void_p)
        self.__PA = self.__CFUNA(self.customercallback)

        # 不打印回调日志
        if not isprintlog:
            self.__CFUNB = WINFUNCTYPE(None, c_int, c_char_p, c_void_p)
            self.__PB = self.__CFUNB(self.nologCallback)
            self.reglogcallback()

    # //need_strategy 分配策略 1随机医生 2随机药师 3指定医生 4指定药师
    # //need_druggist_id 需要的医生和药师ID need_strategy需要为3或者4
    # //only_prescription_checking	请求电子审方,不是则为0
    def store_login(self, docname, mac, need_strategy=Need_Strategy.STRATEGY_FIXED_DRUGGIST
                    , busi_id=322820509, json_str="{}".encode('utf-8'),cn_name='test_store',store_id='72465',
                    device_type='pad', hospital_id=0, only_prescription_checking=0):
        self.__mac = mac
        rs = self.__Objdll.CustomLogin(_dis_ip, _dis_port, cn_name,
                                      self.__mac, store_id,
                                      need_strategy, docname, hospital_id, only_prescription_checking,
                                      busi_id, json_str, device_type,
                                      self.__PA, None, 1)
        if rs == 0:
            self.loginTime = time.time()
            self.storestatus = Storestatus.ST_LOGIN_DISPATCH
            logging.getLogger('root').info("store:%s,LOGIN SUCESSFUL,NEED DOCTOR :%s"%(self.__mac,docname))
            return True
        else:
            print("failure code 2")
            logging.getLogger('root').error("store:%s,LOGIN FAIL,Need Doctor:%s,Error Code:%d"%(self.__mac, docname, rs))
            return False

    def custome_sendmsg(json):
        self.json = json
        rs== self.___Objdll.CustomSendCustomMsg(json)
        if not (rs == 0):
            return False
			
    def reglogcallback(self):
        rs = self.__Objdll.ConsultSetLogMsgCallback(self.__PB, None)
        if not (rs == 0):
            logging.getLogger('root').error('reglogcallback Fail,code:%d' % rs)
            return False
        return True

    def customercallback(self, event, intval, strvalue, jsonval, puser):
     #   '''回调事件处理函数'''
        # 记录事件及时间
        self.callback_Time = time.time()
        self.callback_Event = event
        print(event)
        # 事件处理
        if event == CustomCallbackEvent.CE_MATCH_FAILED:    # 匹配失败
            self.storestatus = Storestatus.ST_MATCH_FAIL
            logging.debug('match fail,%d' % intval)
        elif event == CustomCallbackEvent.CE_MATCH_SUCCEED:  # 匹配成功
            self.storestatus = Storestatus.ST_MATCH_SUCCESS
            print('match sucess')
            logging.debug('match sucess')
        elif event == CustomCallbackEvent.CE_DRUGGIST_RECV_TASK:  # 医生接受业务
            self.storestatus = Storestatus.ST_BUSY
            print('doctor receive task')
        elif event == CustomCallbackEvent.CE_MATCH_WAIT:  # 排队等待
            self.storestatus = Storestatus.ST_WAIT
            self.waitNum = int(intval)
            logging.debug('store:%s,waiting in the %d place'%(self.__mac,self.waitNum))
        elif event == CustomCallbackEvent.CE_DRUGGIST_END_TASK or event == \
                CustomCallbackEvent.CE_DRUGGIST_EXCEPTION_END\
                or event == CustomCallbackEvent.CE_DRUGGIDO_OFFLINE:
            self.storestatus = Storestatus.ST_DOC_ENDCALL
            print('doctor end task')
        elif event == CustomCallbackEvent.CE_DISCONNECTED:  # 药店断线
            self.storestatus = Storestatus.ST_OFFLINE
            print('store offline')
        elif event == CustomCallbackEvent.CE_LEAVE:   # 医生离开
            self.storestatus = Storestatus.ST_LEAVE
        elif event == CustomCallbackEvent.CE_PRESCRIPT_CHECK:  # 审方结果
            print('precepition success ')
            self.callback_Time = time.time()
        elif event == CustomCallbackEvent.CE_LOGIN_SUCCEED:  # 登录成功
            print('store login suceess')
			
    def endtask(self):
        rs = self.__Objdll.CustomEndTask()
        if not (rs == 0):
            logging.getLogger('root').error('EndTask Fail,code:%d'%rs)
            return False
        return True

    def logout(self):
        rs = self.__Objdll.CustomLogout()
        if not (rs == 0):
            logging.getLogger('root').error('logout Fail,code:%d'%rs)
            return False
        return True

    def nologCallback(self, intval, charval, pUser):
     #   '''不打印日志'''
        pass

    def logCallback(self, intval, charval, pUser):
     #   '''日志回调函数'''
        logging.debug(intval.__str__() + charval.decode('utf-8'))
