# encoding: utf-8
import logging.config
import random
import time
from ctypes import *
from multiprocessing import *

from mypackage import stateCenter

# 定义一些变量
dispatch = b'114.215.253.88'  #
port  = 25001

#定义一些时间变量
sleepTime = 1 # 休息时间



# 加载日志的配置文件
logging.config.fileConfig('logging.conf')
logging = logging.getLogger('root')

# 多用户拷机测试
def multRunning():
    userNum = int(input("user Total Num:"))
    minNum = int(input("minNum Total Num:"))
    maxNum = int(input("maxNum Total Num:"))
    computerName = input("computer Name:")

    for i in range(userNum):
        mac = computerName + i.__str__()
        # p = Process(target=ProcessRun, args=(minNum, maxNum, mac,))
        p = Process(target=Running, args=(mac,))
        p.start()

# 用户拷机测试
def Running(minNum, maxNum ,mac):
    cu = Customer()
    while True:
        docName = stateCenter.getRdDoc()

        #先找空闲医生,再找忙碌的医生
        if  docName ==None:
            docName == stateCenter.getRdDoc(0)

        if docName:
            docName = docName.encode()
            # docName = mySql.getDocName(random.randint(minNum - 1, maxNum - 1)).encode("utf-8")
            cu.logIn(docName, 3, mac)
            while True:
                time.sleep(sleepTime)
                isEnd = random.randint(0, 5)
                if (cu.cusStatus == 3):
                    cu.endTask()
                elif((cu.cusStatus == 1 or cu.cusStatus ==2) and isEnd == 3):
                    cu.endTask()
                elif((cu.cusStatus == 1 or cu.cusStatus ==2) and isEnd == 5):
                    cu.logout()
                elif (cu.cusStatus == 0):
                    break
        else:
            print("no doctor found")

class Customer():
    __Objdll = None
    __CFUNA = None
    __CFUNB = None
    __PA = None
    __PB = None
    __mac = ""

    docName = ""
    cusStatus = 0  # 0 :未登陆  1: 等待接受业务  2:业务进行中 3:排队等待 4:登录调度成功

    def __init__(self):
        self.__Objdll = cdll.LoadLibrary("consult_client_sdk.dll")
        self.__Objdll.ConsultSdkInit()

        # callback fun define
        self.__CFUNA = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_char_p, c_void_p)
        self.__CFUNB = WINFUNCTYPE(None, c_int, c_char_p, c_void_p)
        self.__PA = self.__CFUNA(self.CustomerCallback)
        self.__PB = self.__CFUNB(self.logCallback)
        self.reglogCallback()

    def logIn(self, need_druggist_id, need_strategy, mac):
        drugstore_id = b"90"
        self.__mac = mac
        json_str = need_druggist_id
        self.docName = need_druggist_id.decode()

        self.loginTime = time.time()
        rs = self.__Objdll.CustomLogin(dispatch, port, self.__mac, self.__mac, drugstore_id, need_strategy,
                                  need_druggist_id, 0, 0, 100, json_str, b"pad",
                                  self.__PA, None, 1)
        if (rs == 0):
            self.cusStatus = 4
            return True
        else:
            logging.error('login fail'+rs.__str__())

    def closeudp(self):
        if (self.__Objdll.CustomCloseUdpConnection() == 0):
            logging.debug(" closeUdp sucessful")
        else:
            logging.error("closeUdp FAIL")

    def createudp(self):
        rs = self.__Objdll.CustomCreateUdpConnection()
        if (rs == 0):
            logging.debug(" startUdp sucessful")
        else:
            logging.error("startUdp FAIL"+rs.__str__())

    def reglogCallback(self):
        self.__Objdll.ConsultSetLogMsgCallback(self.__PB,None)

    def CustomerCallback(self, event, intVal, strValue, jsonVal, pUser):
        # print(time.time()-self.loginTime)
        print('event value is %s'%event)
        if (event == 0):
            self.cusStatus = 4
            costTime =time.time() - self.loginTime
            # logging.error('match fail ,costTime:'+costTime.__str__()+'code :'+intVal.__str__()+comm.getDocinfo(self.docName).__str__()+self.docName)
            # print(comm.getDocinfo(self.docName).__str__()+self.docName)
        elif (event == 1):  # 匹配成功
            self.cusStatus = 1
            costTime = time.time() - self.loginTime
            # logging.debug('match sucess ,costTime:' + costTime.__str__() + ', request Doc:' + self.docName)
        elif (event == 3):  # 医生接受业务
            self.cusStatus = 2
            logging.debug("recive task ")
            self.createudp()
        elif (event == 2):  # 排队等待
            self.cusStatus = 3
            # logging.debug("wait in the %d place"%(intVal))
        elif (event == 4 or event == 5 or event == 6):
            logging.debug("user logout")
            self.cusStatus = 4
            # self.closeudp()
        elif (event == 7):
            logging.debug(" logout the center")
            self.cusStatus = 0
        elif(event==8):
            logging.debug('CE_UDP_ESTABLISH')
        elif (event == 10):
            logging.debug(" ,doctor leave")
        #发送电子审方结果
        elif (event == 29):
            print(" prescpition result send suceess")
        else:
            logging.debug("unknown event")

    def endTask(self):
        self.__Objdll.CustomEndTask()

    def logout(self):
        self.__Objdll.CustomLogout()

    def endTask(self):
        self.__Objdll.CustomEndTask()

    def printLog(self):
        pass

    def logCallback(self, intval, charval, pUser):
        # pass
        logging.debug(intval.__str__() + charval.decode('utf-8'))

    def __del__(self):
        self.__Objdll.ConsultSdkUnit()

# 多药店保持做业务
def multWorking():
    pass

# 药店保持做业务测试
def login_te(mac):
    cu = Customer()
    while True:
        docName = stateCenter.getRdDoc()

        # 先找空闲医生,再找忙碌的医生
        if docName == None:
            docName == stateCenter.getRdDoc(0)

        if docName:
            docName = docName.encode()
            cu.logIn(docName, 3, mac)
        else:
            print("no doctor found")

if (__name__ == '__main__'):
    pass