"# ReadCSV" 
###记录
1.龙虎榜：http://data.eastmoney.com/stock/tradedetail.html

#### 待优化
1. 爬取龙虎榜信息时，时间跨度是30天


#### 数据库
1. 表名字说明
   - stock_list--股票列表
   - tick_data_{日期}--历史分笔
   - daily_basic_{日期}--每日指标


#### 计算筹码分布
数据来源tushare
1. 调用**日线行情**[daily]获取成交量和成交额
2. 调用**每日指标**[daily_basic]获取换手率、流通股本
3. 