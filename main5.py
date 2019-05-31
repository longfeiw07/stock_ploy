# -*- coding: utf-8 -*-
#
import os
import sys
import utils.util as util
import tushare as ts
import numpy as np
import copy
import pandas as pd
import datetime
import openpyxl
import gc

def write_excel(data, filename='all'):
    columns = data.columns
    print(columns.values)
    # print(type(columns))
    title = columns.values
    for index, name in enumerate(title):
        title[index] = util.title[name]
        # print(title)
    path = os.path.join(util.get_file_path(), "resource", filename+'.xlsx')
    data.to_excel(path)

##获取股票列表
def get_stock_list():
    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code, symbol, name')
    return data

def getDatas():
    pro = ts.pro_api()
    # df = pro.daily(trade_date='20190513')
    df1 = pro.daily_basic(ts_code='', trade_date='20190422',fields='ts_code,close')
    df2 = pro.daily_basic(ts_code='', trade_date='20190513',fields='ts_code,close,turnover_rate')    

    df1_map = df1.set_index('ts_code').T.to_dict('list')
    df2_map = df2.set_index('ts_code').T.to_dict('list')

    datas = {key: df1_map[key] + df2_map[key] for key in df1_map.keys() & df2_map.keys()}
    tock_names = get_stock_list()
    result = []
    for index, row in tock_names.iterrows():
        if row["ts_code"] in datas:
            result_item = []
            result_item.insert(0, row["symbol"])
            result_item.insert(1, row["name"])
            result_item = result_item + datas[row["ts_code"]]
            result.append(result_item)
    # print(result)
    df = pd.DataFrame(result, columns=list({'symbol', 'name', 'colse0', 'close', 'turnover'}))    
    write_excel(df)

N = 5
def getHeavyStockControlUnit():
    """
    1、最近n(n=7)个交易日 每天的收盘价 找出来。n是个可以调的变量。
    2、最近一天的价格必须大于前n-1天的收盘价
    """
    pro = ts.pro_api()
    tmp_lst = {}
    df_lst = {}
    i = 0
    max_day = N
    while i < max_day:
        date = getDate(i, '20190517')
        if isWeekend(date):
            max_day += 1
        else: 
            if i == 0 and isOverTime():
                max_day += 1
            else:
                print(date)
                # i += 1
                # continue
                df = pro.daily_basic(ts_code='', trade_date=date,fields='ts_code,close,turnover_rate')
                if len(tmp_lst) == 0:
                    tmp_lst = df.set_index('ts_code').T.to_dict('list')
                else:
                    df_lst = df.set_index('ts_code').T.to_dict('list')
                if len(tmp_lst) != 0 and len(df_lst) != 0:
                    for key in tmp_lst.keys() & df_lst.keys():
                        if tmp_lst[key][0] > df_lst[key][0]:
                            print('key:', tmp_lst[key], df_lst[key])
                            pass
                        else:
                            tmp_lst.pop(key) 
        i += 1
    # print(tmp_lst)  
    tock_names = get_stock_list()  
    result = []
    for index, row in tock_names.iterrows():
        if row["ts_code"] in tmp_lst:
            result_item = []
            result_item.insert(0, row["symbol"])
            result_item.insert(1, row["name"])
            result_item = result_item + tmp_lst[row["ts_code"]]
            result.append(result_item) 
    # print(result)
    df_shoot = pd.DataFrame(result, columns=list({'symbol', 'name', 'close', 'turnover'}))    
    write_excel(df_shoot)
        

title_excel = ['C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R']    
def writeExcel(datas):
    dst_wb = openpyxl.Workbook()
    dst_sheet = dst_wb.active
    dst_sheet.title = u"重仓控盘股"
    dst_sheet["A1"] = u"代码"
    dst_sheet["B1"] = u"名称"
    for i in range(N, 0, -1):
        date = getDate(i)
        dst_sheet["{}1".format(title_excel[(N-i)*2])] = u"{}".format(date)
        dst_sheet.merge_cells("{}1:{}1".format(title_excel[(N-i)*2], title_excel[(N-i)*2+1]))
    start_row = 2
    index = 1
    for item in datas:
        print(item)
        dst_sheet[u"A{}".format(start_row)] = item[0]
        dst_sheet[u"B{}".format(start_row)] = item[1]
        for i in range(N, 0, -1):
            date = getDate(i)
            if date in item[2]:
                dst_sheet["{}{}".format(title_excel[(N-i)*2], start_row)] = item[2][date][0]
                dst_sheet["{}{}".format(title_excel[(N-i)*2+1], start_row)] = item[2][date][1]
        start_row += 1
        index = +1
    dst_wb.save(r'./resource/all1.xlsx')

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
        date = date + datetime.timedelta(days=-n)
        date = date.strftime("%Y%m%d")
        return date
def isWeekend(day):
    """
    判断是否是星期六 0-周一，1-周二.....5-周六，6-周日, 返回值是<int>类型
    :param day:
    :return:
    """
    day_date = datetime.datetime.strptime(day, '%Y%m%d')
    day_week = day_date.weekday()
    # print('new_time:', new_time, ' day_week: ', day_week)
    if day_week == 5 or day_week == 6:
        return True
    return False
def isOverTime():
    now = datetime.datetime.now()
    now_str = now.strftime('%Y%m%d %H%M%S')
    timer = now_str.split(' ')
    if int(str(timer[1][:2])) < 18:
        return True
    else:
        return False
def getFiveDaysTurnover():
    """
    从今天起往前推5天，这5天每天的换手率都低于3%
    """
    pro = ts.pro_api()
    df_lst = {}
    result_lst = {}
    i = 0
    max_day = N
    while i < max_day:
        date = getDate(i)
        if isWeekend(date):
            max_day += 1
        else: 
            if i == 0 and isOverTime():
                max_day += 1
            else:
                df = pro.daily_basic(ts_code='', trade_date=date,fields='ts_code,turnover_rate')
                # print('df_lst: ', df_lst)
                if len(df_lst) == 0:
                    df_lst = df.set_index('ts_code').T.to_dict('list')
                else:
                    tmp_lst = df.set_index('ts_code').T.to_dict('list')
                    for key in tmp_lst.keys() & df_lst.keys():
                        df_lst[key].append(tmp_lst[key][0])
      
        i += 1
    for key, value in df_lst.items():
        index = 0
        for j in range(len(value)):
            if value[j] < 3:
                index += 1
        if index == N:
            result_lst[key] = []

    # print(result_lst)
    tock_names = get_stock_list()  
    result = []
    for index, row in tock_names.iterrows():
        if row["ts_code"] in result_lst:
            result_item = []
            result_item.insert(0, row["symbol"])
            result_item.insert(1, row["name"])
            result.append(result_item) 
        # print(row["ts_code"])
    # print('result:', result)
    df_shoot = pd.DataFrame(result, columns=list({'symbol', 'name'}))    
    write_excel(df_shoot)

def getMainControlPanelRatio(days):
    """
    多支股票主力控盘比例
    """
    pro = ts.pro_api()
    tock_names = get_stock_list()
    # print(tock_names.columns.values.tolist())
    tock_names.set_index(['ts_code'], inplace = True, drop=True)
    daily_basic_all = pd.DataFrame(None, columns=['ts_code','turnover_rate', 'float_share'])
    for day in getIterator(days):
        print(day)
        daily_basic = pro.daily_basic(ts_code='', trade_date=day,fields='ts_code,turnover_rate,float_share') 
        daily_basic.set_index(['ts_code'], inplace = True, drop=True)
        # print(daily_basic)
        for index, row in daily_basic.iterrows():
            if daily_basic_all.empty:
                daily_basic_all = copy.deepcopy(daily_basic) 
                daily_basic_all['symbol'] = 0
                # print('daily_basic_all:',daily_basic_all)
            else:
                if index in daily_basic_all.index.values:
                    daily_basic_all.loc[index, 'turnover_rate'] += row['turnover_rate']
            if index in tock_names.index.values:
                daily_basic_all.loc[index, 'symbol'] = tock_names['symbol'][index]

    daily_basic_all = daily_basic_all[daily_basic_all['turnover_rate'] > 15]
    print('daily_basic_all:', daily_basic_all)
    del tock_names
    gc.collect()

    daily_basic_all['purchase_sum'] = 0
    daily_basic_all['purchase_sum_per'] = 0
    for day in getIterator(days):
        for index, row in daily_basic_all.iterrows():
            symbol = '{:0>6}'.format(int(row["symbol"]))
            print('symbol:', symbol)
            day = day[:4] + '-' + day [4:6]+ '-' + day[6:]
            historical_tick = ts.get_tick_data(symbol,date=day,src='tt', retry_count=10,pause=5)
            buy_amount = 0
            sell_amount = 0
            for index1, row1 in historical_tick.iterrows():
                if row1['type'] == u'买盘':
                    buy_amount += row1['volume']
                else:
                    sell_amount += row1['volume']
            main_day_amount = (buy_amount/2 + sell_amount/10) / 2
            daily_basic_all.loc[index, 'purchase_sum'] += main_day_amount
            # print(index, daily_basic_all['purchase_sum'][index])
            if day == getMaxDay(days):
                daily_basic_all.loc[index, 'purchase_sum_per'] = float(100*daily_basic_all['purchase_sum'][index])/daily_basic_all['float_share'][index]
    
    daily_basic_all = daily_basic_all.sort_index(axis=0,by='purchase_sum_per',ascending=False)
    print(daily_basic_all)
    write_excel(daily_basic_all, 'MainControl')
def getIterator(days):
    """
    获取days前的迭代器
    """
    i = 0
    max_day = days
    while i < max_day:
        date = getDate(i)
        if isWeekend(date):
            max_day += 1
        else: 
            if i == 0 and isOverTime():
                max_day += 1
            else:
                yield date
        i += 1
def getMaxDay(days):
    """
    获取days天前的日期
    """
    i = 0
    max_day = days
    while i < max_day:
        date = getDate(i)
        if isWeekend(date):
            max_day += 1
        else: 
            if i == 0 and isOverTime():
                 max_day += 1
        i += 1
    return getDate(max_day - 1)
def test():
    day = '20190531'
    day = day[:4] + '-' + day [4:6]+ '-' + day[6:]
    print(day)
if __name__ == "__main__":
    ts.set_token("7e10445dc47be74db4cac3a6ebb22e049ed954d4d070234b36ec738a")
    # ts.set_token("8a4d963e3a1027bade337201ce469b63ddd997941c27e3a4f6b485d5")
    getMainControlPanelRatio(1)
    # test()
    # print(getMaxDay(5))