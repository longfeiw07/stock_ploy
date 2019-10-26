import utils.tools as tools
import Shuju_ruku as shuju
import math
import pandas as pd

def jisuan_choumafenbu(start, end):
    for day in tools.getDateIterator(start, end):
        datas = shuju.get_choumafenbu(day)
        datas.set_index(['ts_code'], inplace = True, drop=False)
        print(datas)
        profit_list = {}
        for index, row in datas.iterrows():
            jishu = 0
            ts_code = row['ts_code']
            float_share = row['float_share']
            turnover_rate = row['turnover_rate']/100
            profit_amount = get_profit_amount(ts_code, day, turnover_rate)
            profit_per = (profit_amount - row['vol']) / (float_share*10000)
            profit_list[ts_code] = profit_per
        profit_series = pd.Series(profit_list, name="profit")
        print('profit_series:', profit_series)
        datas = datas + profit_series
        print('datas:', datas)

jishu = 0
def get_profit_amount(code, day, rate):
    datas = shuju.get_choumafenbu(day)
    datas.set_index(['ts_code'], inplace = True, drop=False)
    count = datas[code]['vol']
    print('count:',count)
    global jishu
    jishu += 1
    if count <= 1:
        return count
    
    return count + get_profit_amount(code, tools.getDate(-1, day), rate)*math.pow((1-rate), jishu)


# def fun(n):
#     global jishu
#     jishu += 1
#     if n==1:
#         return 1
#     return n+fun(n-1)

# s = fun(4)
# print(s)
# print(jishu)
# for i in range(2):
#     jishu = 0
#     s = fun(4)
#     print(s)
#     print(jishu)

jisuan_choumafenbu('20191024', '20191024')