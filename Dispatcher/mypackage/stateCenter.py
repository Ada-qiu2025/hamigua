import urllib.request as rs
import json,random,time
import configparser
import logging

# 读取配置文件的信息
confile = 'sever.ini'
config = configparser.ConfigParser()
config.read(confile)
url = None
state_center = None
state_center_listarea = None


def getDocinfo(account):
    '''从调度服务中的doclist获取医生的状态和排队数'''
    page = rs.urlopen(url)
    data = page.read()
    data = data.decode('utf-8')
    start = data.find('account:'+account)
    if start!=-1:
        end = data[start:].find('\n')
        data = data[start-8:start+end]
        status = data[data.find("workstate")+10:data.find("workstate")+11]
        queued = data[data.find("queued")+7:data.find("queued")+8]
        return (status,queued)
    else:
        return None


#
# def verfydocstatus(docobj):
#     s = getDocinfo(docobj.docAccout)
#     if s:
#         assert docobj.waitNum == int(s[1])
#         print('waitNum == '+s[1])
#         if docobj.DcoStatus == 1:
#             assert int(s[0])== 2
#             print('status == 1')
#         if docobj.DcoStatus == 2:
#             assert int(s[0]) == 2
#             print('status == 2')
#         if docobj.DcoStatus == 3:
#             assert  int(s[0]) == 0
#             print('status == 3')
#     else:
#         assert docobj.DcoStatus == 0
#         print('status == 0')


# '''从状态中心获取医生的列表,0为空闲医生,2为忙碌医生'''
def getDocLi(type=0):
    li = []
    page = rs.urlopen(state_center)
    try:
        hjson = json.loads(page.read())
        for i in list(hjson):
            Type = (hjson.get(i))['Type']
            Accout = (hjson.get(i))['Accout']
            WaitPatient = (hjson.get(i))['WaitPatient']
            TempLeave = (hjson.get(i))['TempLeave']
            State = (hjson.get(i))['State']
            if type == 0 and State == 0 and TempLeave == False:
                li.append(Accout)
            elif State == 2 and type == 2:
                li.append(Accout)
    except Exception as e:
        logging.error('没有找到医生%s'%e.__str__())
    finally:
        return li



# '''随机获取状态中心医生列表信息0.空闲 2.忙碌'''
def getRdDoc(type=0):
    li  = getDocLi(type)
    if len(li)>0:
        return li[random.randint(0,len(li)-1)]
    elif len(li) == 0:
        logging.error('寻找随机医生失败,type:%d'%type)


# '''从状态中心找医生,找到则返回找到的时间点.time()'''
# start_time 开始计时的时间.
# 返回值为所用到的时间
def find_Doc(account,status,find_times=100):
    logging.info('开始寻找医生,%s'%account)
    start_time = time.time()
    j = 0
    while True:
        j += 1
        page = rs.urlopen(state_center)
        try:
            hjson = json.loads(page.read())
            State = hjson[account]['State']
            logging.getLogger('root').debug('轮训查找,Account:%s,status:%s' %(account,State))
        except Exception as e:
            State = -1
            logging.debug('没有找到医生,Account:%s,error:%s'%(account,e))

        if State == status or j >= find_times:
            logging.debug('找到医生或超时退出寻找,轮训次数:%d,Account:%s'%(j,account))
            break
        time.sleep(0.01)
    return time.time() - start_time

if __name__=='__main__':
    state_center = 'http://114.55.2.253:8091/list'
else:
    url = config.get('disCenter', 'doctorlist')
    state_center = config.get('statcenter', 'list')
    state_center_listarea = config.get('statcenter', 'listArea')