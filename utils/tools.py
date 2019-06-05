# -*- coding: utf-8 -*-
import datetime
from chinese_calendar import is_workday, is_holiday
def getDate(n ,date=None):
        """
        得到指定某天的第n天
        :param date:
        :return:
        """
        if date is None:
            date = datetime.date.today()
        else:
            date = datetime.datetime.strptime(date, "%Y%m%d") 
        date = date + datetime.timedelta(days=n)
        date = date.strftime("%Y%m%d")
        return date
def getDiscrepancy(start, end):
    '''获取相差多少天'''
    start_sec = datetime.datetime.strptime(start, '%Y%m%d')
    end_sec = datetime.datetime.strptime(end, '%Y%m%d')
    delta = end_sec - start_sec
    return delta.days

def isHolidayOrWeekend(day):
    """
    判断是否是星期六 0-周一，1-周二.....5-周六，6-周日, 返回值是<int>类型
    :param day:
    :return:
    """
    april_last = datetime.date(int(day[:4]), int(day[4:6]), int(day[6:]))
    if is_holiday(april_last):
        return True
    
    day_date = datetime.datetime.strptime(day, '%Y%m%d')
    day_week = day_date.weekday()
    # print('new_time:', new_time, ' day_week: ', day_week)
    if day_week == 5 or day_week == 6:
        return True
    return False
def isOverTime():
    '''当前是否超过18点'''
    now = datetime.datetime.now()
    now_str = now.strftime('%Y%m%d %H%M%S')
    timer = now_str.split(' ')
    if int(str(timer[1][:2])) < 18:
        return True
    else:
        return False