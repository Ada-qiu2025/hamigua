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


# ��ȡ�����ļ�����Ϣ
os.chdir('E:\Pydemo\DispatchCenterTest\DispatchCenterTest')
confile = 'sever.ini'
config = ConfigParser.ConfigParser()
config.read(confile)
_dis_ip = config.get('disCenter', 'ip')    # ���ȷ����ַ
_dis_port = config.getint('disCenter', 'port')  # ���ȷ���˿�
dllpath = './dll/'  # config.get('sdk', 'path')    # ����sdk����·��

# # ������Ҫ�õ���sdk��Ϣ
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


# ҽ���ص���ö������
class PharmacistCallbackEvent(Enum):
    PE_MATCH_SUCCEED = 0  # ƥ��ɹ�	intValue:�û����� 0���¶� 1�ƶ��� stringValue:�����¶ˣ�ҩ��ID jsonValue:(�ֻ���)�ֻ���Ϣ
    PE_AV_CONTROL = 1  # ����Ƶ����	stringValue:  jsonValue: ��������Ƶ��Ϣ
    PE_FILE_URL = 2  # ͼƬ֪ͨ  stringValue:ͼƬurl
    PE_GPS_INFO = 3  # GPS��Ϣ   jsonValue:
    PE_CLIENT_END_TASK = 4  # �ͻ�����ҵ��
    PE_CLIENT_OFFLINE = 5  # �ͻ�����
    PE_CLIENT_EXCEPTION_END = 6  # �ͻ��쳣�Ͽ�
    PE_DISCONNECTED = 7  # ��������Ͽ�����
    PE_UDP_ESTABLISH = 8  # UDP���ӽ����ɹ�
    PE_LEAVE = 9
    PE_PUSH_MESSAGE = 10  # ͼ����Ϣ��Ϣ
    PE_WAIT = 11  # �Ŷӿͻ���
    PE_CUSTOM_SEND_CUSTOM_MSG =12 #custome_senddrugmsg


# ҽ����״̬��ö��
class Docstatus(Enum):
    DO_OFFLINE = 0  # ����
    DO_MATCH_SUCESS = 1  # �ѷ��������ҵ��
    DO_BUSY = 2  # æµ
    DO_FREE = 3  # ����
    DO_LEAVE = 4  # �뿪
    DO_STORE_ENDCALL = 5  # ҩ��Ҷ�ҵ��


# //druggist_type ҽ����ҩʦ���� 0��ҩʦ 1��ҩʦ 2ִҵ��ҩʦ 3ִҵ��ҩʦ 4ҽ��
class DocType(Enum):
    DO_TYPE_DRUGGIST = 1  # ҩʦ
    DO_TYPE_DOCTOR = 4  # ҽ��


# //need_strategy ������� 1���ҽ�� 2���ҩʦ 3ָ��ҽ�� 4ָ��ҩʦ
class Need_Strategy(Enum):
    STRATEGY_RD_DOC = 1
    STRATEGY_RD_DRUGGIST = 2
    STRATEGY_FIXED_DOC = 3
    STRATEGY_FIXED_DRUGGIST = 4
    STRATEGY_RD_ZDRUGGIST=5
    STRATEGY_RD_WDRUGGIST=6
    ASSIGN_DRUGGIST_EX = 7


class Doctor:
    def __init__(self, isprintlog=False):   # False ���λص���־��ӡ��Ϣ
        # self.__service_id = mydo.get_docservice(account)
        self.doc_status = Docstatus.DO_OFFLINE
        self.is_Pause = None  # �Ƿ�����
        self.loginTime = None  # ҽ����¼ʱ��
        self.PauseTime = None  # ҽ������ʱ���
        self.waitNum = None  # �ȴ�����
        self.Account = None  # ҽ�����˺�
        self.callback_Event = None  # ҽ���Ļص��¼�
        self.callbackEnd_Time = None  # ���һ�λص��¼���ʱ�� �ͻ��˽���ҵ��
        self.startwort_time = None # ��ʼҵ��ʱ��
        self.leave_time = None # �뿪��ʱ��
        self.callback_Time =None #���һ�λص��¼���ʱ��

   #     """��ʼ��sdk��ע��ص�����"""
        self.__DllObj = cdll.LoadLibrary(dllpath+'consult_client_sdk.dll')
        self.__DllObj.ConsultSdkInit()
        self.__CFUNC = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_int, c_char_p, c_int, c_void_p)
        self.__CBE = self.__CFUNC(self.callbackevent)

        # ΪTrue���ע����־�ص�����,Ĭ�ϲ�ע����־�ص�
        if not isprintlog:
            self.__CFUNB = WINFUNCTYPE(None, c_int, c_char_p, c_void_p)
            self.__CBEB = self.__CFUNB(self.nologCallback)
            # self.reglogcallback()

    def login(self,account,doctype=DocType.DO_TYPE_DRUGGIST,fullname='ft_Test',platname='FT',servertype=1):
  #      """ҽ����¼���ȷ���"""
        self.Account = account  # ҽ���˺ų�ʼ��
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
    #    """�ǳ����ȷ���"""
        rs = self.__DllObj.PharmacistLogout()
        if rs == 0:
            logging.getLogger('root').info("Doctor:%s has logouted sucessfully" % (self.Account))
            self.doc_status = Docstatus.DO_OFFLINE
            return True
        else:
            logging.getLogger('root').info("Doctor:%s logOUT FAIL..,code:%d") % (self.Account,rs)
            return False

    # ע����־�ص�
    def reglogcallback(self):
    #    """ע��ص�����"""
        rs = self.__DllObj.ConsultSetLogMsgCallback(self.__CBEB, None)
        if rs == 0:
            logging.getLogger('root').info("reglogcallback suceessful")
            return True
        else:
            logging.getLogger('root').error("reglogcallback fail ,code:%d")
            return False

    # @staticmethod
    # def logcallback(self, intval, charval, puser):
    #     """ע����־�ص�����"""
    #     logging.getLogger('root').info(intval.__str__() + charval.decode("gb2312"))

    def leave(self):
    #    """��ʱ�뿪"""
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
    #    '''����֪ͨ'''
        rs = self.__DllObj.PharmacistFree()
        if rs == 0:
            self.doc_status = Docstatus.DO_FREE
            logging.getLogger('root').info("Doc:%s ,is free.." % (self.Account))
            return True
        else:
            logging.getLogger('root').error("Doc:%s ,free fail.code:%d" % (self.Account,rs))
            return False

    def recevice(self, busiid=b'100'):
    #    """����ҵ��"""
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
    #    """ֹͣҵ��"""
        rs = self.__DllObj.PharmacistEndTask()
        if rs == 0:
            logging.getLogger('root').info("Doctor:%s ,is endTask.." % (self.Account))
            return True
        else:
            logging.getLogger('root').error("Doctor:%s ,endTask fail..code:%d" % (self.Account,rs))
            return False

    def pres_check(self, result):
     #       '''���ʹ�����˽��'''
            if (self.__DllObj.PharmacistPrescriptionCheckResult(result.encode('utf-8')) == 0):
                logging.getLogger('doctor').info("%s prescipition success" % (self.Account))
                return 0
            else:
                logging.getLogger('doctor').info("%s prescipition failed" % (self.Account))
                return -1
    # ҽ������
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

    # ����ӡ��־
    def nologCallback(self, intval, charval, pUser):
     #   '''����ӡ��־'''
        pass

    def callbackevent(self, event, intval, strvalue, strlen, jsonval, jsonlen, puser):
    #    '''�¼��ص�����'''

        # ��¼�¼���ʱ��
        self.callback_Event = event

        if event == PharmacistCallbackEvent.PE_MATCH_SUCCEED.value:  # ƥ��ɹ�
            self.doc_status = Docstatus.DO_MATCH_SUCESS
        elif event == PharmacistCallbackEvent.PE_FILE_URL.value:
            pass
        elif event == PharmacistCallbackEvent.PE_GPS_INFO.value:
            pass
        elif event == PharmacistCallbackEvent.PE_CLIENT_END_TASK.value:  # �ͻ��˽���ҵ��
            self.free()
            self.callbackEnd_Time=time.time()
            logging.getLogger('root').info("%s ,has be clientEndTask.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_CLIENT_OFFLINE.value:  # �ͻ��˵���
            self.free()
            logging.getLogger('root').info("%s ,has be clientLogout.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_CLIENT_EXCEPTION_END.value:  # �ͻ��������쳣
            self.free()
            logging.getLogger('root').info("%s ,has be clientNetError.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_LEAVE.value:  # ҽ����ʱδ��ҵ��,��ʱ����
            self.doc_status = Docstatus.DO_LEAVE
            self.leave_time = time.time()
            logging.getLogger('root').info("%s ,has be leave.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_WAIT.value:  # �Ŷ������䶯�ص�
            self.waitNum = int(intval)
            # logging.getLogger('root').info("%s ,has be waitchanged.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_DISCONNECTED.value:  # ����ȷ���Ͽ�
            self.doc_status = Docstatus.DO_OFFLINE
            logging.getLogger('root').debug("%s ,has be logout.." % (self.Account))
        elif event == PharmacistCallbackEvent.PE_AV_CONTROL.value:
            pass
        elif event == PharmacistCallbackEvent.PE_PUSH_MESSAGE.value:
            pass
        elif event ==12: #����ҵ��
            self.callback_Time=time.time()
        else:
            pass


# �û��ص��¼�
class CustomCallbackEvent(Enum):
    CE_MATCH_FAILED = 0  # ƥ��ʧ��
    CE_MATCH_SUCCEED = 1  # ƥ��ɹ�
    CE_MATCH_WAIT = 2  # �ŶӵȺ���
    CE_DRUGGIST_RECV_TASK = 3  # ҽҩʦ�ѽ�������
    CE_DRUGGIST_END_TASK = 4  # ҽҩʦ����ҵ��
    CE_DRUGGIDO_OFFLINE = 5  # ҽҩʦ����
    CE_DRUGGIST_EXCEPTION_END = 6  # ҽҩʦ�쳣�Ͽ�
    CE_DISCONNECTED = 7  # ��������Ͽ�����
    CE_UDP_ESTABLISH = 8  # UDP���ӽ����ɹ�
    CE_PUSH_DRUG = 9  # �Ƽ�ҩƷ
    CE_LEAVE = 10  # ҽ���뿪
    CE_SCREENSHOT = 11  # ��ͼ�ɹ��ص�
    CE_PRESCRIPT_CHECK = 12  # ������˽��
    CE_LOGIN_SUCCEED = 13  # ��¼�ɹ�


# ҩ���״̬
class Storestatus(Enum):
    ST_OFFLINE = 0  # ҩ������
    ST_WAIT = 1   # ҩ���ڵȴ�״̬
    ST_MATCH_SUCCESS = 2   # �ȴ�����ҵ��
    ST_MATCH_FAIL = 3   # ƥ��ʧ��
    ST_BUSY = 4  # æµ,ҵ����
    ST_LEAVE = 5  # ҽ���뿪
    ST_DOC_ENDCALL = 6  # ҽ������,�Ҷ�ҵ������쳣�뿪
    ST_LOGIN_DISPATCH = 7 # ҩ���¼���ȷ���


class Store:
    callback_Time = None
    def __init__(self, isprintlog=False):
        # mydo = test_case.dispatchcenter.mysql_db.MyDao()
        # self._storeinfo = mydo.get_stroreinfo(mac)
        self.__mac = None
        self.waitNum = None
        self.storestatus = Storestatus.ST_OFFLINE
        self.loginTime = None
        self.callback_Event = None  # �ص�������
        self.callback_Time=None  # �ص���ʱ��

        # ���ض�̬�⼰ע��ص�����
        self.__Objdll = cdll.LoadLibrary(dllpath+'consult_client_sdk.dll')
        self.__Objdll.ConsultSdkInit()
        self.__CFUNA = WINFUNCTYPE(None, c_int, c_int, c_char_p, c_char_p, c_void_p)
        self.__PA = self.__CFUNA(self.customercallback)

        # ����ӡ�ص���־
        if not isprintlog:
            self.__CFUNB = WINFUNCTYPE(None, c_int, c_char_p, c_void_p)
            self.__PB = self.__CFUNB(self.nologCallback)
            self.reglogcallback()

    # //need_strategy ������� 1���ҽ�� 2���ҩʦ 3ָ��ҽ�� 4ָ��ҩʦ
    # //need_druggist_id ��Ҫ��ҽ����ҩʦID need_strategy��ҪΪ3����4
    # //only_prescription_checking	���������,������Ϊ0
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
     #   '''�ص��¼�������'''
        # ��¼�¼���ʱ��
        self.callback_Time = time.time()
        self.callback_Event = event
        print(event)
        # �¼�����
        if event == CustomCallbackEvent.CE_MATCH_FAILED:    # ƥ��ʧ��
            self.storestatus = Storestatus.ST_MATCH_FAIL
            logging.debug('match fail,%d' % intval)
        elif event == CustomCallbackEvent.CE_MATCH_SUCCEED:  # ƥ��ɹ�
            self.storestatus = Storestatus.ST_MATCH_SUCCESS
            print('match sucess')
            logging.debug('match sucess')
        elif event == CustomCallbackEvent.CE_DRUGGIST_RECV_TASK:  # ҽ������ҵ��
            self.storestatus = Storestatus.ST_BUSY
            print('doctor receive task')
        elif event == CustomCallbackEvent.CE_MATCH_WAIT:  # �Ŷӵȴ�
            self.storestatus = Storestatus.ST_WAIT
            self.waitNum = int(intval)
            logging.debug('store:%s,waiting in the %d place'%(self.__mac,self.waitNum))
        elif event == CustomCallbackEvent.CE_DRUGGIST_END_TASK or event == \
                CustomCallbackEvent.CE_DRUGGIST_EXCEPTION_END\
                or event == CustomCallbackEvent.CE_DRUGGIDO_OFFLINE:
            self.storestatus = Storestatus.ST_DOC_ENDCALL
            print('doctor end task')
        elif event == CustomCallbackEvent.CE_DISCONNECTED:  # ҩ�����
            self.storestatus = Storestatus.ST_OFFLINE
            print('store offline')
        elif event == CustomCallbackEvent.CE_LEAVE:   # ҽ���뿪
            self.storestatus = Storestatus.ST_LEAVE
        elif event == CustomCallbackEvent.CE_PRESCRIPT_CHECK:  # �󷽽��
            print('precepition success ')
            self.callback_Time = time.time()
        elif event == CustomCallbackEvent.CE_LOGIN_SUCCEED:  # ��¼�ɹ�
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
     #   '''����ӡ��־'''
        pass

    def logCallback(self, intval, charval, pUser):
     #   '''��־�ص�����'''
        logging.debug(intval.__str__() + charval.decode('utf-8'))
