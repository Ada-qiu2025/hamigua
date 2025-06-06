import threadpool
import time, random


# def hello(str):
#     return str
#
# def print_result(request, result):
#     print("the result is %s %s" % (request.requestID, result))
#
# data = [random.randint(1, 10) for i in range(20)]
#
# pool = threadpool.ThreadPool(5)
#
# requests = threadpool.makeRequests(hello, data, print_result)
#
# [pool.putRequest(req) for req in requests]
#
# pool.wait()

def Main_Def(par1, par2, par3):
    print("par1 = %s, par2 = %s, par3 = %s" % (par1, par2, par3))


if __name__ == '__main__':
    # 方法1
    list_var1 = ['1', '2', '3']
    list_var2 = ['4', '5', '6']
    par_list = [(list_var1, None),(list_var2, None)]
    print(par_list)
    # 方法2
    dict_var1 = {'par1': '1', 'par2': '2', 'par3': '3'}
    dict_var2 = {'par1': '4', 'par2': '5', 'par3': '6'}
    par_list = [(None, dict_var1), (None, dict_var2)]
    print(par_list)
    pool = threadpool.ThreadPool(2)
    requests = threadpool.makeRequests(Main_Def, par_list)
    [pool.putRequest(req) for req in requests]
    time.sleep(1)
    pool.wait()
