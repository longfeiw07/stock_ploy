# -*- coding: utf-8 -*-
#
import os
import sys
import utils.util as util
import tushare as ts
import numpy as np
def test():
    pro = ts.pro_api()
    df = get_stock_private()
    write_excel(df)
#获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向
def get_stock_private():
    data = pro.moneyflow(trade_date='20190329')
    return data
#获取大单交易数据，默认为大于等于400手，数据来源于新浪财经。
def get_big_deal():
    df = ts.get_sina_dd('600131', date='2019-03-07', vol=400)  #指定大于等于500手的数据
    print(df)
#获取历史数据
def get_stock_hist(tock_id):
    ts.get_hist_data(tock_id,start='2015-01-05',end='2015-01-09')

#一次性获取最近一个日交易日所有股票的交易数据（结果显示速度取决于网速）
#返回参数：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率
def get_stock_today_all():
    data = ts.get_today_all()


def write_excel(data):
    columns = data.columns
    print(columns.values)
    # print(type(columns))
    title = columns.values
    for index, name in enumerate(title):
        title[index] = util.title[name]
        # print(title)
    path = os.path.join(util.get_file_path(), "resource", "all.xlsx")
    data.to_excel(path)

##获取股票列表
def get_stock_list():
    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='symbol,name')
    return data
if __name__ == "__main__":
    ts.set_token("5e9d772f754320c8f903311ac27e32b118248dd47f8ef182ccba62fe")
    # ts.set_token("8a4d963e3a1027bade337201ce469b63ddd997941c27e3a4f6b485d5")
    test()