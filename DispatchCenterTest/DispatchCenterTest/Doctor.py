# encoding: utf-8
import logging
import logging.config
import random
import time
from ctypes import *
from multiprocessing import *

from mypackage import comm

# 定义一些变量
dispatch = b'114.215.253.88'  #
port  = 25001
statt_center = 'http://172.20.13.249:8091/list'


# 定义一些时间变量
Workduring = 60 # 每次工作时间为1分钟
sleepTime = 1  # 每次循环的时间
leaseTime = random.randint(1, 3) * 60  # 每次休息1-5分钟
workTime = random.randint(10, 30) * 60  # 每次工作10-30分钟
loginDur = random.randint(2, 5) * 60   # 每次登陆3-5分钟


# 加载日志的配置文件
logging.config.fileConfig('logging.conf')
logging = logging.getLogger('root')

def logCallback(intval, charval, pUser):
    pass
    # logging.info('callback '+charval.decode('utf-8')+intval.__str__())
    # (('callback ,%d ,%s'%(intval,charval)))

# 医生会随机做业务
def Running(docname):
    d = Doctor()
    if(d.login(docname, 4)):
        while True:
            # comm.verfydocstatus(d)
            time.sleep(sleepTime)
            if (d.DcoStatus == 1):
                d.recevice(b"101")
                # for i in range(10):
                #     time.sleep(15)
                #     d.closeudp()
                # time.sleep(5)
            elif (d.DcoStatus == 2):
                d.endTask()
            elif (d.DcoStatus == 4):
                d.free()
            elif (d.DcoStatus == 0):
                d.login(docname, 4)

            if ((d.DcoStatus == 1 or d.DcoStatus == 2 or d.DcoStatus == 3 or d.DcoStatus == 4) and (
                        d.is_Pause == False) and (
                        (time.time() - d.PauseTime) > workTime)):
                d.pause(True)
            elif ((d.DcoStatus == 1 or d.DcoStatus == 2 or d.DcoStatus == 3 or d.DcoStatus == 4) and (
                        d.is_Pause == True) and (
                        (time.time() - d.PauseTime) > leaseTime)):
                d.pause(False)

            if ((time.time() - d.loginTime) > loginDur):
                d.logout()

# 医生会一直保持做业务,持续999*60*60秒.
def working(docname):
    d = Doctor()
    if (d.login(docname, 2)):
        while True:
            time.sleep(0.1)
            if (d.DcoStatus == 1):
                d.recevice(b"101")
                time.sleep(999*60*60)

def MultDocWoring():
    DocLi = comm.getDocList()
    DocNum = int(input("Doctor Total Num:"))
    DocId = int(input("Doctor Id:"))

    for i in range(DocNum):
        p = Process(target=working, args=(DocLi[DocId - 1][0].encode("utf-8"),))
        DocId += 1
        p.start()

class Doctor:
    DcoStatus = 0  # 0 - 离线, 1:等待接业务 ,2:业务中 , 3:空闲 ,4:离开
    is_Pause = 0  # 是否暂离
    loginTime = None  # 医生登录时间
    PauseTime = None  # 医生暂离时间点
    waitNum = 0  # 等待人数

    __DllObj = None
    __CFUNC = None
    __CBE = None
    __CFUNB = None
    __CBEB = None
    docAccout = ""

    # 统计数据
    logTime = {"docName": "", "freeTimes": 0, "pauseTimes": 0, "receviceTimes": 0, "loginTimes": 0, "logoutTimes": 0,
               "endTaskTimes": 0, "waitChangeTimes": 0, "beAssignTimes": 0, "beLeaveTimes": 0, "beLogoutTimes": 0,
               "clientEndTaskTime": 0 ,"clientLogoutTime":0,"clientNetErrorTime":0}

    def __init__(self):
        self.__DllObj = cdll.LoadLibrary("consult_client_sdk.dll")
        self.__DllObj.ConsultSdkInit()
        # callback fun define
        self.__CFUNC = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_int, c_char_p, c_int, c_void_p)
        self.__CFUNB = WINFUNCTYPE(None, c_int, c_char_p, c_void_p)
        self.__CBE = self.__CFUNC(self.callbackEvent)
        self.__CBEB = self.__CFUNB(logCallback)
        self.reglogCallback()

    def login(self, DocId, DocType):
        self.docAccout = DocId.decode()
        if (self.__DllObj.PharmacistLogin(dispatch, port, DocId, b"ft", DocId, DocType, 1, self.__CBE, None,1) == 0):
            self.PauseTime = time.time()
            self.loginTime = time.time()
            self.DcoStatus = 3

            # costTime = getChangedTime(DocId.decode('utf-8'),0) - self.loginTime
            # logging.info('LogincostTime:'+costTime.__str__())
            return True
        else:
            logging.error(self.docAccout+"IS LOGIN FAIL")

    def logout(self):
        if (self.__DllObj.PharmacistLogout() == 0):
            logging.info(self.docAccout+"+is logout..")
            self.DcoStatus = 0
        else:
            logging.error(self.docAccout+"LOGOUT FAIL")

    def reglogCallback(self):
        self.__DllObj.ConsultSetLogMsgCallback(self.__CBEB, None)

    def leave(self):
        if (self.__DllObj.PharmacistToLeave() == 0):
            logging.info(self.docAccout+"is leave..")
            self.DcoStatus = 4
        else:
            logging.error(self.docAccout+"Leave FAIL")

    def free(self):
        if (self.__DllObj.PharmacistFree() == 0):
            logging.info(self.docAccout+" is free..")
            self.DcoStatus = 3
        else:
            logging.error(self.docAccout+"free Fail")

    def recevice(self, busiId):
        if (self.__DllObj.PharmacistReceiveTask(busiId) == 0):
            logging.info(self.docAccout+" recive the call..")
            self.createudp()
            time.sleep(Workduring)
            self.DcoStatus = 2
        else:
            logging.error(self.docAccout+"recevice FAIL")

    def endTask(self):
        if (self.__DllObj.PharmacistEndTask() == 0):
            self.free()
            logging.info(self.docAccout+" is end the call..")
        else:
            logging.error(self.docAccout+"endTask FAIL")

    def printLog(self):
        pass
        # mySql.updateDocLog(self.logTime)
        # logging.info(self.docAccout+self.DcoStatus, self.logTime)
        # return self.logTime

    def closeudp(self):
        if (self.__DllObj.PharmacistCloseUdpConnectionImmediate() == 0):
            logging.info(self.docAccout+" closeUdp sucessful")
        else:
            logging.error(self.docAccout+"closeUdp FAIL")

    def createudp(self):
        rs = self.__DllObj.PharmacistCreateUdpConnection()
        if (rs == 0):
            logging.info(self.docAccout+" startUdp sucessful")
        else:
            logging.error(self.docAccout+"startUdp FAIL"+rs.__str__())

    # 医生暂离
    def pause(self, val):
        if (self.__DllObj.PharmacistPauseService(val) == 0):
            self.logTime["pauseTimes"] += 1
            self.PauseTime = time.time()
            self.is_Pause = val
            logging.info(self.docAccout+(" is Pause %s")%val)
        else:
            logging.error(self.docAccout+"Pause fail.")

    # 事件回调
    def callbackEvent(self, event, intVal, strValue, strLen, jsonVal, jsonLen, pUser):
        if (event == 0):  # 匹配成功
            self.DcoStatus = 1
            self.logTime["beAssignTimes"] += 1
            logging.info(self.docAccout+" has be assign..")
        elif (event == 4):
            self.free()
            self.logTime["clientEndTaskTime"] += 1
            logging.info(self.docAccout+" has be clientEndTaskTime..")
        elif (event == 5):
            self.free()
            self.logTime["clientLogoutTime"] += 1
            logging.info(self.docAccout+" has be clientLogoutTime..")
        elif (event == 6):
            self.free()
            self.logTime["clientNetErrorTime"] += 1
            logging.info(self.docAccout+" has be clientNetErrorTime..")
        elif (event == 8):
            # print(intVal,strValue)
            logging.info(self.docAccout + " PE_UDP_ESTABLISH")
        elif (event == 9):  # 超时未接离线
            self.DcoStatus = 4
            self.logTime["beLeaveTimes"] += 1
            logging.info(self.docAccout+" has be leave..")
        elif (event == 11):
            self.waitNum = intVal
            self.logTime["waitChangeTimes"] += 1
        elif (event == 7):  # 与调度断开连接
            self.DcoStatus = 0
            self.logTime["beLogoutTimes"] += 1
            logging.info(self.docAccout+" has be logout..")
        else:
            pass


if __name__=='__main__':
    MultDocWoring()
    # while True:
    #     do = Doctor()
    #     do.login(b"ajx", 4)
    #     while True:
    #         time.sleep(25)
    #         if(do.DcoStatus ==1):
    #             pass
    #         elif(do.DcoStatus==0):
    #             do.login(b"ajx", 4)
