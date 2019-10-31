# -*- coding: utf-8 -*-
import os
import sys
import datetime
from chinese_calendar import is_workday, is_holiday
import utils.util as util
sys.setrecursionlimit(1000000)

def get_file_path():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)
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
def getDateWithoutHoliday(n ,date=None):
    """
    得到指定某天的第n天,且不是节假日
            :param date:
            :return:
    """
    if date is None:
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(date, "%Y%m%d") 
    date = date + datetime.timedelta(days=n)
    date = date.strftime("%Y%m%d")
    if isHolidayOrWeekend(date):
        return getDateWithoutHoliday(n, date)
    # print('返回：', date)
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
    :param day: %Y%m%d
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
def isOverTime(date):
    '''当前是否未超过18点'''
    now = datetime.datetime.now()
    now_str = now.strftime('%Y%m%d %H%M%S')
    timer = now_str.split(' ')
    if date == str(timer[0]):
        if int(str(timer[1][:2])) < 18:
            print('未超过18点，没有今天数据！！')
            return True
        else:
            return False
    else:
        return False
    
def getDateIterator(n, input_date=None, islater=False):
    """
    获取生成器，n天前到当天，islater为False，返回n天前生成器，islater为True，返回n天后生成器
    """
    i = 0
    max_day = n
    while i < max_day:
        if islater:
            date = getDate(i, input_date)
        else:
            date = getDate(-i, input_date)
        if isHolidayOrWeekend(date):
            max_day += 1
        else: 
            if isOverTime(input_date):
                max_day += 1
            else:
                yield date
        i += 1
def getDateIteratorWithTimer(starttime, endtime):
    """
    获取每天的生成器,starttime:开始时间，endtime:结束时间
    """
    for i in range(getDiscrepancy(starttime, endtime)+1):
        day = getDate(i, starttime)
        if not isHolidayOrWeekend(day):
            yield day
def getMaxDay(days, islater=False):
    """
    获取days天前的日期
    """
    i = 0
    max_day = days
    while i < max_day:
        if islater:
            date = getDate(i)
        else:
            date = getDate(-i)
        if isHolidayOrWeekend(date):
            max_day += 1
        else: 
            if i == 0 and isOverTime():
                 max_day += 1
        i += 1
    if islater:
        return getDate(max_day - 1)
    else:
        return getDate(-(max_day - 1))
def getMinDay(starttime, islater=False):
    """
    获取最开始的时间
    """
    timer = starttime
    i = 0
    while isHolidayOrWeekend(timer):
        if islater:
            timer = getDate(i, starttime)
        else:
            timer = getDate(-i, starttime)
        i += 1
    return timer
def write_excel(data, filename='default'):
    '''写入excel'''
    columns = data.columns
    # print(type(columns))
    title = columns.values
    for index, name in enumerate(title):
        title[index] = util.title[name]
        # print(title)
    path = os.path.join(get_file_path(), "resource", filename+'.xlsx')
    data.to_excel(path, index=False)

def getEverydayIterator(starttime, endtime):
    """
    获取每天的生成器
    """
    for i in range(getDiscrepancy(starttime, endtime)+1):
        day = getDate(i, starttime)
        if not isHolidayOrWeekend(day):
            # print('day:', day)
            yield day