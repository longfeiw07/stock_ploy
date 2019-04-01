import os
import sys
def get_file_path():
    # 获取脚本路径
    path = sys.path[0]
    # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

title = {"code":"代码", "symbol": "ID", "name": "名称", "industry": "所属行业", "date":"日期", "open": "开盘价", "settlement":"昨日收盘价", "high":"最高价", "close": "收盘价", "low":"最低价","volume":"成交量", "amount": "成交金额", "price_change": "价格变动","p_change":"涨跌幅", 
    "ma5": "5日均价", "ma10": "10日均价", "ma20": "20日均价", "v_ma5": "5日均量", "v_ma10": "10日均量", "v_ma20": "20日均量", "turnover": "换手率",
    "ts_code": "TS代码",
"trade_date": "交易日期",
"buy_sm_vol": "小单买入量（手）",
"buy_sm_amount": "小单买入金额（万元）",
"sell_sm_vol": "小单卖出量（手）",
"sell_sm_amount": "小单卖出金额（万元）",
"buy_md_vol": "中单买入量（手）",
"buy_md_amount": "中单买入金额（万元）",
"sell_md_vol": "中单卖出量（手）",
"sell_md_amount": "中单卖出金额（万元）",
"buy_lg_vol": "大单买入量（手）",
"buy_lg_amount": "大单买入金额（万元）",
"sell_lg_vol": "大单卖出量（手）",
"sell_lg_amount": "大单卖出金额（万元）",
"buy_elg_vol": "特大单买入量（手）",
"buy_elg_amount": "特大单买入金额（万元）",
"sell_elg_vol": "特大单卖出量（手）",
"sell_elg_amount": "特大单卖出金额（万元）",
"net_mf_vol": "净流入量（手）",
"net_mf_amount": "净流入额（万元）",
"trade_date": "交易日期", "pre_close": "昨收价",
"change": "涨跌额","pct_chg": "涨跌幅","vol": "成交量 （手）",
}
