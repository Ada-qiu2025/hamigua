#-*-coding:UTF-8 -*-

# from itertools import permutations
#
# for i in permutations([1, 2, 3, 4], 3):
#     print(i)
#
# # for i in range(1,5):
# #     for j in range(1,5):
# #         for k in range(1,5):
# #             if (i !=k)and (i !=j)and (j !=k):
# #                 print(i,j,k)
#
# list_num = [1,2,3,4]
#
# list  = [i*100 + j*10 + k for i in list_num for j in list_num for k in list_num if (j != i and k != j and k != i)]
#
# print (list)


# year = int(input('year:\n'))
# month = int(input('month:\n'))
# day = int(input('day:\n'))
#
# months = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
# if 0 < month <= 12:
#     sum = months[month - 1]
# else:
#     print('data error')
# sum += day
# leap = 0
# if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
#     leap = 1
# if (leap == 1) and (month > 2):
#     sum += 1
# print('it is the %dth day.' % sum)


import  random
type=random.randint(0,4)
print( type)