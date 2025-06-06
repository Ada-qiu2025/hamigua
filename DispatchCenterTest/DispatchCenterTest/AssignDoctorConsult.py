# encoding: utf-8

from mypackage.disPacher import *
import time, random
import logging.config, os
import mypackage.comm as cm
import mypackage.stateCenter as sc
import logging.handlers
from multiprocessing import *

# # # 加载日志的配置文件
logging.config.fileConfig('logging.conf')
logging = logging.getLogger('root')

# right card 130530198101232523
pccustomer='{"busiType":201,"ftId":null,"dept_id":0,"custName":"lucy","IDCardNo":"130530198101232523","SSCardNo":null,"cardType":0,"cardPicUrl":"","sex":"1","age":36,"weight":0,"storeConfigDic":null,"busiData":{"id":null,"storeId":"15757","chainId":"8229","flowId":"20201124C8229S15757D0428","phone":"15688860858","ybId":"MPC2020112400037814"}}'
drugvalue='{"Age":"0","ChainId":8229,"CustName":"?????","DrugType":0,"Drugs":[{"batchNumbe":"","count":5,"onsellId":17420}],"Sex":"0","StoreId":15757,"Weight":0}'
def assignDoc():
	cu = Store()
	for num in range(1,2):
		cu.store_login('qq','mac',json_str=pccustomer,need_strategy=3)
		time.sleep(5)
		while cu.storestatus in [Storestatus.ST_MATCH_SUCCESS, Storestatus.ST_WAIT, Storestatus.ST_BUSY]:
			time.sleep(2)
			cu.custome_sendmsg(drugvalue)
			if cu.storestatus == Storestatus.ST_DOC_ENDCALL:
				print('doctor end business')
				cu.store_login('yy','mac',need_strategy=4,only_prescription_checking=1)
				print('find pharmist')
				time.sleep(30)
				break
			else:
				time.sleep(30)
		print('loop %d times ' %num)

def mult_store_rd_running(stroe_num):
    from multiprocessing import Process

    for i in range(stroe_num):
        p = Process(target=assignDoc)
        p.start()

if __name__=='__main__':
	mult_store_rd_running(1)