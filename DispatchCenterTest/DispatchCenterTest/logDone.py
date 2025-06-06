import time
from enum import Enum
import xlwt
import time


def getValue(str,key,spliter=':',dis=' '):
    keypoint = str.find(key)
    sliterpoint = keypoint + key.__len__()

    if keypoint>=0 and str[sliterpoint:sliterpoint+spliter.__len__()]==spliter:
        start = str[sliterpoint:].find(spliter) + sliterpoint + 1
        end = str[sliterpoint:].find(dis) + sliterpoint
        return  str[start:end]
    else:
        return None

# 行日志的类型
class ACTION_TYPE(Enum):
    DOC_LOGIN = 0  # 医生登录
    DOC_REVICE = 1   # 接收业务
    DOC_LEAVE = 2   # 医生离开
    DOC_PAUSE = 3  # 忙碌,业务中
    DOC_FREE = 4  # 医生空闲
    DOC_LOGOUT = 5  # 医生离开
    DOC_ENDCALL = 6 # 医生挂断
    CLIENT_LOGIN = 7  # 药店登录
    CLIENT_ENDCALL_ACTIVELY = 8  # 药店主动结束业务
    CLIENT_MATCH_FAIL = 9  # 匹配失败退出
    MOBILE_LOGIN = 10 # 手机客户端登录
    REVICE_COMMAND = 11 # 接收命令
    CLIENT_MATCH_WAIT = 12

def readlog(path):
    file = open(path)
    action_type = ()
    list = []
    data = {}

    while True:
        f = file.readline()
        type = None
        if len(f) == 0:  # Zero length indicates EOF
            break

        # 取出该行日志时间
        logtime = f[0:19]

        # 取出handler

        handler = getValue(f,'handler')
        # start = f.find('handler:')
        # if start>0:
        #     start = f.find('handler:')+8
        #     end = f[start:].find(' ')+start
        #     handler = f[start:end]
        if handler:
            if f.find('mobile login') > 0:
                type = ACTION_TYPE.Moblie_LOGIN
            elif f.find('client login') > 0:
                type = ACTION_TYPE.CLIENT_LOGIN
            elif f.find('end the business actively') > 0:
                type = ACTION_TYPE.CLIENT_ENDCALL_ACTIVELY
            elif f.find('finish business') > 0:
                type = ACTION_TYPE.CLIENT_ENDCALL_ACTIVELY
            elif f.find('is free') > 0:
                type = ACTION_TYPE.DOC_FREE
            elif f.find('doctor login')>0:
                type = ACTION_TYPE.DOC_LOGIN
            elif f.find('recv cmd')>0:
                type = ACTION_TYPE.REVICE_COMMAND
            elif f.find('match failure')>0:
                type = ACTION_TYPE.CLIENT_MATCH_FAIL
            elif f.find('match wait')>0:
                type = ACTION_TYPE.CLIENT_MATCH_WAIT

        if type==ACTION_TYPE.REVICE_COMMAND:
            code = getValue(f,'recv cmd',':','\n')

        if handler and logtime and type:
            action_type = (logtime,handler,type.value,code)
            # if(data.get(action_type)):
            #     # print(action_type)
            #     data[action_type] = data[action_type] + 1
            # else:
            #     data[action_type] = 1
            list.append(action_type)

        # if len(list) > 5000:
        #     # print(list)
        #     file.close()
        #     return list

    file.close()
    return list


def writeExcel(list,sheetName):
    # 将数据写入excel
    wbk = xlwt.Workbook()
    j = 0
    sheet = wbk.add_sheet(sheetName)
    for i in list:
        sheet.write(j ,0 , i[0])
        sheet.write(j ,1 , i[1])
        sheet.write(j ,2 , i[2])
        sheet.write(j ,3 , i[3])
        j+= 1
    wbk.save('d:/log-3.xls')

def calcLong(li):
    for i in li:
        if i[2] == 9:
            print(i)
            for j in li:
                if i[1] == j[1]:
                    if i[0]!=j[0]:
                        print(j)

if __name__=='__main__':
    # list = [('14:48:43', '21', '<ACTION_TYPE.REVICE_COMMAND: 11>', '1'), ('14:48:49', '21', '<ACTION_TYPE.CLIENT_LOGIN: 7>', '1'), ('14:48:45', '21', '<ACTION_TYPE.REVICE_COMMAND: 11>', '3')]
    li = readlog('d:/e')
    # print(li)
    calcLong(li)
    # writeExcel(li,'else')

# for i in data:
#     if i[1] == ACTION_TYPE.DOC_FREE:
#         print(i, data[i])

# 画图
#     index = [1,2,3,4,5,6,7,8,9,10]
#     y = [20, 10, 30, 25, 15]
#     plt.bar(left=index, height=y, color='green', width=0.5)
#     plt.show()
#
#     # if i[1] == ACTION_TYPE.CLIENT_LOGIN：
#     #     print()