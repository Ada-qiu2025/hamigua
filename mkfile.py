# -*- coding: utf-8 -*-
import os
from time import strftime, localtime
from datetime import timedelta, date
import calendar

year = strftime("%Y",localtime())
mon  = strftime("%m",localtime())
day  = strftime("%d",localtime())
hour = strftime("%H",localtime())
min  = strftime("%M",localtime())
sec  = strftime("%S",localtime())

filedir = os.listdir('D:\Program Files\富顿科技\微问诊医生工作站\RegulatorLog')

def addzero(n): 
    ''''' 
    add 0 before 0-9 
    return 01-09 
    ''' 
    nabs = abs(int(n)) 
    if(nabs<10): 
        return "0"+str(nabs) 
    else: 
        return nabs 
		
def get_days_of_month(year,mon): 
    ''''' 
    get days of month 
    ''' 
    return calendar.monthrange(year, mon)[1] 

def getyearandmonth(n=0): 
    ''''' 
    get the year,month,days from today 
    befor or after n months 
    ''' 
    thisyear = int(year) 
    thismon = int(mon) 
    totalmon = thismon+n 
    if(n>=0): 
        if(totalmon<=12): 
            days = str(get_days_of_month(thisyear,totalmon)) 
            totalmon = addzero(totalmon) 
            return (year,totalmon,days) 
        else: 
            i = totalmon/12 
            j = totalmon%12 
            if(j==0): 
                i-=1 
                j=12 
            thisyear += i 
            days = str(get_days_of_month(thisyear,j)) 
            j = addzero(j) 
            return (str(thisyear),str(j),days) 
    else: 
        if((totalmon>0) and (totalmon<12)): 
            days = str(get_days_of_month(thisyear,totalmon)) 
            totalmon = addzero(totalmon) 
            return (year,totalmon,days) 
        else: 
            i = totalmon/12 
            j = totalmon%12 
            if(j==0): 
                i-=1 
                j=12 
            thisyear +=i 
            days = str(get_days_of_month(thisyear,j)) 
            j = addzero(j) 
            return (str(thisyear),str(j),days) 

def get_today_month(n=0):
    (y,m,d) = getyearandmonth(n) 
    arr=(y,m,d) 
    if(int(day)<int(d)): 
        arr = (y,m,day) 
    return ("%s" %i for i in arr) 
	
def get_calender_days():
	
	
if __name__=="__main__":
    print(get_today_month(-3))