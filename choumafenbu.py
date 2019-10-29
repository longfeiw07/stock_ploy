import utils.tools as tools
import Shuju_ruku as shuju
import math
import pandas as pd
import sys
from sqlalchemy import create_engine

import numpy as np
# sys.setrecursionlimit(1000000)

jishu = 0
amount = 0
rate = 1

def jisuan_choumafenbu(start, end):
    for day in tools.getDateIterator(start, end):
        datas = shuju.get_choumafenbu(day)
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
    """
    """
    # print('day: ', day)
    datas_current = shuju.get_choumafenbu(day)
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
        print("day:{0}, code:{6}, count:{1}, turnover_rate:{2}, rate:{3}, amount:{4}, float_share: {5}, jishu: {7}, amount:{8}".format(day, count, turnover_rate, rate, amount, float_share, code, jishu, amount))
    else:
        per_shou = np.around(count*rate)

        print("day:{0}, code:{7}, count:{1}, turnover_rate:{2}, rate:{3}, per_shou:{4}, amount:{5}, float_share: {6}, jishu: {8}, amount:{9}".format(day, count, turnover_rate, rate, per_shou, amount, float_share, code, jishu, amount))
        if per_shou <= 1 or amount >= float_share or jishu >= 30:
            return amount
        amount += per_shou
    rate = rate*(1-turnover_rate)
    jishu += 1
    return get_profit_amount(code, tools.getDateWithoutHoliday(-1, day))

def filter

jisuan_choumafenbu('20191024', '20191024')