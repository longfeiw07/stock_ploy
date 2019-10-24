# -*- coding: utf-8 -*-

import pandas as pd
import utils.tools as tools
from sqlalchemy import create_engine
import sqlite3
def getTickDatas(day):
    """
    获取分笔数据
    """
    engine = create_engine('mysql+pymysql://root:nopwdmysql@localhost:3306/tushare')
    try:
        table_name = 'tick_data_{}'.format(day)  
        sql_cmd = "SELECT * FROM {}".format(table_name)
        historical_tick = pd.read_sql(sql=sql_cmd, con=engine)
        return historical_tick
        
    except Exception as identifier:
        print('error:', identifier, 'day:', day)
        return pd.DataFrame(columns=['ts_code','symbol'])

def dbsqlite():
    for day in tools.getDateIteratorWithTimer('20190506', '20190612'):
        tick_day_data = getTickDatas(day=day)
        if tick_day_data.empty:
            continue
        engine = create_engine('sqlite:///tushare.db', echo=True)
        with engine.connect() as con:
            table_name = 'tick_data_{}'.format(day)
            print(table_name)
            tick_day_data.to_sql(table_name, con, index= False, if_exists='replace')

def getsqlite():
    engine = create_engine('sqlite:///tushare.db', echo=True)
    with engine.connect() as con:
        table_name = 'tick_data_{}'.format('20190506')  
        sql_cmd = "SELECT * FROM {}".format(table_name)
        # result = con.execute(sql_cmd)
        df = pd.read_sql(sql=sql_cmd, con=con)
    print(df)
def sqlite_read():
    mydb = sqlite3.connect('tushare.db')       # 链接数据库
    cur = mydb.cursor()                         # 创建游标cur来执行SQL语句
    # 获取表名
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    Tables = cur.fetchall()                     # Tables 为元组列表
    print(Tables)

dbsqlite()
# getsqlite()
sqlite_read()