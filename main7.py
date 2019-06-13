# -*- coding: utf-8 -*-
#
import os
import sys
import utils.util as util
import tushare as ts
# import numpy as np
import datetime
import utils.tools as tools
from sqlalchemy import create_engine
import pandas as pd
import copy
import gc

##获取股票列表
def get_stock_list():
    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')
    return data
def getMainControlPanelRatio(starttime, endtime):
    """
    多支股票主力控盘比例
    """
    pro = ts.pro_api()
    tock_names = get_stock_list()
    tock_names.set_index(['ts_code'], inplace = True, drop=True)

    daily_dic = {}
    for day in tools.getDateIteratorWithTimer(starttime, endtime):
        try:
            daily_basic = pro.daily_basic(ts_code='', trade_date=day,fields='ts_code,turnover_rate,float_share') 
            daily_basic.set_index(['ts_code'], inplace = True, drop=True)
        except Exception as e:
            print('error:',e)
        for index, row in daily_basic.iterrows():
            if index not in daily_dic:
                daily_dic[index] = row['turnover_rate']
            else:
                daily_dic[index] += row['turnover_rate']
    daily_series = pd.Series(daily_dic)
    # print('daily_series',daily_series)
    tock_names['turnover_rate'] = daily_series
    tock_names['float_share'] = daily_basic['float_share']
    tock_names = tock_names[tock_names['turnover_rate'] > 50]

    purchase_sum = {}
    purchase_sum_per = {}
    for day in tools.getDateIteratorWithTimer(starttime, endtime):
        historical_tick = getTickDatas(day)
        if historical_tick.empty:
            continue
        historical_tick.set_index(['ts_code'], inplace = True, drop=True)
        for index, row in tock_names.iterrows():
            if index in historical_tick.index.values:
                historical_data = (float(historical_tick.loc[index, 'buy_volume'])/2 + float(historical_tick.loc[index, 'sell_volume'])/10)/2
                share_data = float(tock_names.loc[index, 'float_share'])
                main_day_amount = historical_data/share_data
                if index not in purchase_sum:
                    purchase_sum[index] = main_day_amount
                else:
                    purchase_sum[index] += main_day_amount
    purchase_sum_series = pd.Series(purchase_sum)
    purchase_sum_per = 100*purchase_sum_series
    tock_names['purchase_sum_per'] = purchase_sum_per
    tock_names.drop(columns='float_share', inplace=True)
    tock_names = tock_names.dropna(subset=['purchase_sum_per'])
    tock_names = tock_names.sort_values(axis=0,by='purchase_sum_per',ascending=False)
    print('tock_names:',tock_names)
    tools.write_excel(tock_names, 'MainControlPanel_add')

def getTickDatas(day):
    """
    获取分笔数据
    """
    engine = create_engine('mysql+pymysql://root:nopwd@mysql@localhost:3306/tushare')
    try:
        table_name = 'tick_data_{}'.format(day)  
        sql_cmd = "SELECT * FROM {}".format(table_name)
        historical_tick = pd.read_sql(sql=sql_cmd, con=engine)
        return historical_tick
        
    except Exception as identifier:
        print('error:', identifier, 'day:', day)
        return pd.DataFrame(columns=['ts_code','symbol'])

if __name__ == "__main__":
    ts.set_token("7e10445dc47be74db4cac3a6ebb22e049ed954d4d070234b36ec738a")
    getMainControlPanelRatio('20190506','20190611')

