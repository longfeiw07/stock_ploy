# -*- coding: utf-8 -*-

import requests
import re
import json
import csv
import utils.util as util
import time
import datetime
import asyncio
import aiohttp
class Reptile():
    def __init__(self, start, end, isappend):
        self._startTime = start
        self._endTime = end
        self.isAppend = isappend
        self.__pageAll = 0
    @staticmethod
    def is_valid(start, end):
        if start != '' and end != '':
            return True
        else:
            return False

    def GetUrl(self):
        url = "http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?"
        return url
    def GetResponse(self, page, start, end):
        params = {
            'tkn': 'eastmoney',
            'mkt': '0',
            'dateNum': '',
            'startDateTime': start,
            'endDateTime': end,
            'sortRule': '1',
            'sortColumn': '',
            'pageNum': page,
            'pageSize': '50',
            'cfg': 'lhbggdrtj'
            }
        url = self.GetUrl()
        response = requests.get(url, params=params).text
        return response
    def ToJsonForm(self, titles, value):
        """
        生成器
        """
        title_lst = titles.split(',')
        data = re.search(r"\[(.*?)\]", value).group(1)
        # print('data: ', data)
        value_lst = re.finditer(r"\"(.*?)\"", data)
        # print('value_lst: ', value_lst)
        for v_item in value_lst:
            # print(v_item.group())
            item_lst =  re.search(r"\"(.*?)\"", v_item.group()).group(1).split("|")
            dict_item = {}
            for (title_item, value_item) in zip(title_lst, item_lst):
                dict_item[title_item] = value_item
            # data_lst.append(dict_item)
            yield dict_item


    def GetTable(self, page, start, end):
        index = 3
        data = ''
        while index > 0:
            if data == '' or len(data) == 2:
                response = self.GetResponse(page, start, end)
                # print('response:', response)
                self.__pageAll = re.search(r"\"TotalPage\":(\d+)", response).group(1)
                title = re.search(r"\"FieldName\":\"(.*?)\"", response).group(1)
                # print(self.__pageAll)
                result = re.search(r"\"Data\":(\[.*\])", response).group(1)
                data = re.search(r"\"Data\":(\[.*?\])", result).group(1)
                
            else:
                break
            index -= 1
        
        datas_iter = self.ToJsonForm(title, data)
        # print(title)
        return title, datas_iter
    def WriteHeader(self, data):
        title_lst = []
        for key, value in util.longhu_title.items():
            if value != '':
                title_lst.append(value)
            else:
                title_lst.append(key)
        # print('title_lst: ', title_lst)
        with open('resource/eastmoney.csv', 'w', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(title_lst)
    def WriteTable(self, dataiter):
        # print("dataiter: ", dataiter)
        for d in dataiter:
            # print('d: ', d)
            with open('resource/eastmoney.csv', 'a', encoding='utf_8_sig', newline='') as f:
                if d['Ltsz'] != '' or d['Ltsz']:
                    d['Ltsz'] = round(float(d['Ltsz'])/100000000.0)
                if d['JmMoney'] != '':
                    d['JmMoney'] = round(float(d['JmMoney'])/1000)
                if d['BMoney'] != '':
                    d['BMoney'] = round(float(d['BMoney'])/1000)
                if d['Smoney'] != '':
                    d['Smoney'] = round(float(d['Smoney'])/1000)
                if d['ZeMoney'] != '':
                    d['ZeMoney'] = round(float(d['ZeMoney'])/1000)
                if d['Turnover'] != '':
                    d['Turnover'] = round(float(d['Turnover'])/1000)
                w = csv.writer(f)
                w.writerow(d.values())
    def GetAllDatas(self, start, end):
        if self.CalTime(start, end) < 2:
            print('时间间隔不足2天，数据不全')
            return
        for page in range(1, int(self.__pageAll)+1):
            datas_iter = self.GetTable(page, start,end)[1]
            self.WriteTable(datas_iter)
        
    def StartReptile(self):
        """
        """
        print('天数：', self.CalTime(self._startTime, self._endTime))
        if self.isAppend == 'no':
            self.WriteHeader(self.GetTable(0, self._startTime, self.DesignatedOneDay(self._startTime, 2))[0])

        if self.IsData(self._startTime) and self.IsData(self._endTime):
            if self.CalTime(self._startTime, self._endTime) <= 30:
                self.GetAllDatas(self._startTime, self._endTime)
            else:
                start = self._startTime
                end = self._endTime
                while self.CalTime(start, end) >= 0:
                    try:
                        start = self.DesignatedOneDay(end, -30)
                    except:
                        print("相差不到30天")
                        start = self._startTime
                      
                    self.GetAllDatas(start, end)
                    end = start
        else:
            print('请输入正确日期')
    def IsData(self, datastr):
        """
        判断日期是否合法
        """
        try:
            time.strptime(datastr,"%Y-%m-%d")
            return True
        except:
            return False
    def CalTime(self, date1, date2):
        """
        计算相差天数
        """
        date1=time.strptime(date1,"%Y-%m-%d")
        date2=time.strptime(date2,"%Y-%m-%d")
        date1=datetime.datetime(date1[0],date1[1],date1[2])
        date2=datetime.datetime(date2[0],date2[1],date2[2])
        return (date2-date1).days

    def DesignatedOneDay(self, date, n):
        """
        得到指定某天的第n天
        :param date:
        :param n:
        :return:
        """
        date = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=n)
        date = date.strftime("%Y-%m-%d")
        return date