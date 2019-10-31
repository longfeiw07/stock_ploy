import utils.tools as tools
import Shuju_ruku as shuju
import pandas as pd


def jisuan_huolipanbili(date, n):
    datas_now = shuju.get_huolipanbili(date)
    data_result = pd.DataFrame()
    times = 0
    for index, row in datas_now.iterrows():
        for day in tools.getDateIterator(n, date):

            try:
                datas = shuju.get_huolipanbili_with_code(day, row['ts_code'])
                datas.set_index(['ts_code'], inplace = True, drop=False)
                if float(datas['profit'][0]) <= 0.5:
                    times = 0
                    break
                times += 1
                if n == times: 
                    data_result = data_result.append(row, ignore_index=False)
                    print('data_result: ', data_result)
            except (TypeError, KeyError) as e:
                times = 0
                break
    data_result = data_result[['ts_code', 'amount', 'average', 'float_share', 'turnover_rate', 'vol', 'profit']]        
    print('data_result: ', data_result)
    data_result.to_excel('Huolipanbili.xlsx')
    
        

jisuan_huolipanbili('20191024', 1)
# jisuan_choumafenbu('20190801', '20191023')
