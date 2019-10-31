# -*- coding: utf-8 -*-
#
import os
import sys
import utils.util as util
import tushare as ts
import numpy as np
import datetime
import pandas as pd
import utils.tools as tools
from sqlalchemy import create_engine
# engine = create_engine('mysql+pymysql://root:nopwdmysql@localhost:3306/MySQL80/tushare')
def getDateIterator(starttime, endtime):
    """
    获取每天的生成器
    """
    for i in range(tools.getDiscrepancy(starttime, endtime)+1):
        day = tools.getDate(i, starttime)
        if not tools.isHolidayOrWeekend(day):
            # print('day:', day)
            yield day
def db_stock_basic():
    '''入库 股票列表'''
    pro = ts.pro_api()
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        stock_basic = pro.stock_basic(exchange='',list_status='L')
        stock_basic.to_sql('stock_basic', con, index= False, if_exists='replace')
def db_tick_data(start,end):
    '''入库 历史分笔'''
    pro = ts.pro_api()
    name_lst = pro.stock_basic(exchange='', list_status='L', fields='ts_code, symbol, name')
    for day in getDateIterator(start, end):
        table_name = 'tick_data_{}'.format(day)
        if check_table(table_name):
            continue
        tick_day_lst = []
        for index, row in name_lst.iterrows():
            print('day:',day,' symbol', row['symbol'])
            try:
                historical_tick = ts.get_tick_data(row['symbol'],date=day,src='tt', retry_count=10,pause=5)
                for index1, row1 in historical_tick.iterrows():
                    buy_volume = 0
                    sell_volume = 0
                    if row1['type'] == u'买盘':
                        buy_volume += row1['volume']
                    else:
                        sell_volume += row1['volume']
                main_day_volume = (buy_volume/2 + sell_volume/10) / 2
                tick_lst = [row['ts_code'], row['symbol'], row['name'], buy_volume, sell_volume, main_day_volume]
                # print('tick_lst', tick_lst)
                tick_day_lst.append(tick_lst)
            except Exception as e:
                print('error:',e)
                print('day',day, ' symbol:',row['symbol'])
                continue

        tick_day_arr = np.array(tick_day_lst)
        tick_day_data = pd.DataFrame(tick_day_arr, columns=['ts_code','symbol', 'name', 'buy_volume', 'sell_volume', 'main_day_volume'])
        print(tick_day_data)
        engine = create_engine('sqlite:///tushare.db')
        with engine.connect() as con:
            # table_name = 'tick_data_{}'.format(day)
            # print(table_name)
            tick_day_data.to_sql(table_name, con, index= False, if_exists='replace')
def db_daily_basic(start, end):
    '''入库 每日指标'''
    pro = ts.pro_api()
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        for day in getDateIterator(start, end):
            daily_basic = pro.daily_basic(ts_code='', trade_date=day) 
            table_name = 'daily_basic_{}'.format(day)
            daily_basic.to_sql(table_name, con, index= False, if_exists='replace')
def db_top_list(start, end):
    '''入库 龙虎榜每日明细'''
    pro = ts.pro_api()
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        for day in getDateIterator(start, end):
            top_lst = pro.top_list(trade_date=day)
            table_name = 'top_list_{}'.format(day)
            top_lst.to_sql(table_name, con, index= False, if_exists='replace')
def db_oneyflow(start, end):
    '''入库 个股资金流向'''
    pro = ts.pro_api()
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        for day in getDateIterator(start, end):
            moneyflow = pro.moneyflow(trade_date=day)
            table_name = 'moneyflow_{}'.format(day)
            moneyflow.to_sql(table_name, con, index= False, if_exists='replace')
def get_stock_basic(fields=None,chunksize=None):
    '''从数据库读取 股票列表 注：fields为list，但无效'''
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        sql_cmd = "SELECT * FROM stock_basic"
        print(type(fields), fields)
        stock_basic = pd.read_sql(sql=sql_cmd, con=con, columns=fields, chunksize=chunksize)
    return stock_basic
def get_daily_basic(day):
    '''从数据库读取每日指标'''
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        table_name = 'daily_basic_{}'.format(day)  
        sql_cmd = "SELECT * FROM {}".format(table_name)
        df = pd.read_sql(sql=sql_cmd, con=con)
        print(df)
def get_table_list():
    '''获取数据库表的列表'''
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        sql_cmd = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        tables = pd.read_sql(sql=sql_cmd, con=con)
        return tables
def check_table(name, isForce=False):
    if not isForce:
        tables_name = get_table_list()
        if name in tables_name.values:
            return True
    else:
        return False
    return False

def db_junjia_ruku(start, end):
    """
    计算获利盘比例时的均价数据入库
    """
    pro = ts.pro_api()
    for day in getDateIterator(start, end):
        table_name = 'choumafenbu_{}'.format(day)
        # if check_table(table_name):
        #     continue
        daily_basic = pro.daily_basic(ts_code='', trade_date=day, fields='ts_code,turnover_rate,float_share')
        daily_basic.set_index(['ts_code'], inplace = True, drop=False)
        daily = pro.daily(trade_date=day)
        daily.set_index(['ts_code'], inplace = True, drop=True)
        daily_basic['vol'] = daily['vol']
        daily_basic['amount'] = daily['amount']
        average_price = daily['amount']*1000/daily['vol']/100
        daily_basic['average'] = average_price
        # print(daily_basic)

        engine = create_engine('sqlite:///tushare.db')
        with engine.connect() as con:
            daily_basic.to_sql(table_name, con, index= False, if_exists='replace')
        
def get_junjia(day):
    '''从数据库读取每日指标，包括均价'''
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        table_name = 'choumafenbu_{}'.format(day)  
        sql_cmd = "SELECT * FROM {} ORDER BY ts_code".format(table_name)
        df = pd.read_sql(sql=sql_cmd, con=con)
        return df

jishu = 0
amount = 0
rate = 1
def db_huolipanbili_ruku(start, end):
    '''计算获利盘比例，并入库'''
    for day in tools.getEverydayIterator(start, end):
        datas = get_junjia(day)
        datas.set_index(['ts_code'], inplace = True, drop=False)
        # print(datas)
        profit_list = {}
        for index, row in datas.iterrows():
            global jishu
            global amount 
            global rate
            jishu = 0
            amount = 0
            rate = 1
            ts_code = row['ts_code']
            float_share = row['float_share']
            turnover_rate = row['turnover_rate']/100
            profit_amount = get_profit_amount(ts_code, day)
            if not profit_amount:
                continue
            profit_per = ((profit_amount - row['vol'])*100) / (float_share*10000)
            profit_list[ts_code] = str(profit_per)
        profit_series = pd.Series(profit_list, name="profit")
        
        datas['profit'] = profit_series
        print('datas:', datas)
        table_name = 'huolipanbili_{}'.format(day)
        engine = create_engine('sqlite:///tushare.db')
        with engine.connect() as con:
            datas.to_sql(table_name, con, index= False, if_exists='replace')

def get_profit_amount(code, day):
    '''计算获利的股票数，因获利盘比例=获利的股票数/流通股数'''
    datas_current = get_junjia(day)
    datas_current.set_index(['ts_code'], inplace = True, drop=False)
    # count = datas_current.get_value(code, 'vol')                    #成交量**手
    try:
        count = datas_current['vol'][code]
    except KeyError as e:
        return None
    turnover_rate = datas_current['turnover_rate'][code]/100  #换手率
    float_share = datas_current['float_share'][code]*100
    global jishu
    global amount 
    global rate
    
    if jishu == 0:
        amount += count
        # print("day:{0}, code:{6}, count:{1}, turnover_rate:{2}, rate:{3}, amount:{4}, float_share: {5}, jishu: {7}, amount:{8}".format(day, count, turnover_rate, rate, amount, float_share, code, jishu, amount))
    else:
        per_shou = np.around(count*rate)

        # print("day:{0}, code:{7}, count:{1}, turnover_rate:{2}, rate:{3}, per_shou:{4}, amount:{5}, float_share: {6}, jishu: {8}, amount:{9}".format(day, count, turnover_rate, rate, per_shou, amount, float_share, code, jishu, amount))
        if per_shou <= 1 or amount >= float_share or jishu >= 30:
            return amount
        amount += per_shou
    rate = rate*(1-turnover_rate)
    jishu += 1
    return get_profit_amount(code, tools.getDateWithoutHoliday(-1, day))

def get_huolipanbili(day):
    """获取获利盘比例"""
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        table_name = 'huolipanbili_{}'.format(day)  
        sql_cmd = "SELECT * FROM {} ORDER BY ts_code".format(table_name)
        df = pd.read_sql(sql=sql_cmd, con=con)
        return df
def get_huolipanbili_with_code(day, code):
    """根据股票代码ts_code获取获利盘比例"""
    engine = create_engine('sqlite:///tushare.db')
    with engine.connect() as con:
        table_name = 'huolipanbili_{}'.format(day)  
        sql_cmd = "SELECT * FROM {0} WHERE ts_code='{1}'".format(table_name, code)
        df = pd.read_sql(sql=sql_cmd, con=con)
        return df



def main():
    #数据入库
    # get_table_list()
    # db_daily_basic('20190603', '20190603')
    # db_top_list('20190501', '20190601')  
    # get_stock_basic('20190506')
    #计算获利盘比例
    # db_junjia_ruku('20180101', '20191029')
    db_huolipanbili_ruku('20191001', '20191023')
      

if __name__ == "__main__":    
    ts.set_token("478f21f5f334c11290a7f8c9646a838bb1bba46ce68d4d69ecf5f447")   
    main()
