# -*- coding: utf-8 -*-

import requests
import re
import json
import csv
import utils.util as util
class Reptile():
    def __init__(self, start, end):
        self.startTime = start
        self.endTime = end
    def getUrl(self):
        url = "http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?"
        return url
    def getResponse(self, page):
        params = {
            'tkn': 'eastmoney',
            'mkt': '0',
            'dateNum': '',
            'startDateTime': self.startTime,
            'endDateTime': self.endTime,
            'sortRule': '1',
            'sortColumn': '',
            'pageNum': page,
            'pageSize': '50',
            'cfg': 'lhbggdrtj'
            }
        url = self.getUrl()
        response = requests.get(url, params=params).text
        return response
    def getDatas(self):
        response = self.getResponse(1)
        # print(response)
        page_all = re.search(r"\"TotalPage\":(\d+)", response).group(1)
        title = re.search(r"\"FieldName\":\"(.*?)\"", response).group(1)
        # print(page_all)
        result = re.search(r"\"Data\":(\[.*\])", response).group(1)
        data = re.search(r"\"Data\":(\[.*?\])", result).group(1)
        # print(data)
        
        return page_all, title, data
    def toJsonForm(self, titles, value):
        title_lst = titles.split(',')
        data = re.search(r"\[(.*?)\]", value).group(1)
        value_lst = data.split(",")
        data_lst = []
        # print(value_lst)
        for v_item in value_lst:
            v_item = re.search(r"\"(.*?)\"", v_item).group(1)
            item_lst = v_item.split("|")
            # print(v_item)
            dict_item = {}
            for (title_item, value_item) in zip(title_lst, item_lst):
                dict_item[title_item] = value_item
            data_lst.append(dict_item)
        return data_lst
    def writeCSV(self):
        page_nums, titles, data = self.getDatas()
        datas = self.toJsonForm(titles, data)
        # print(datas)
        for d in datas:
            with open('004.csv', 'a', encoding='utf_8_sig', newline='') as f:
                w = csv.writer(f)
                w.writerow(d.values())

    def getTable(self, page):
        response = self.getResponse(page)
        print('response', response)
        page_all = re.search(r"\"TotalPage\":(\d+)", response).group(1)
        title = re.search(r"\"FieldName\":\"(.*?)\"", response).group(1)
        # print(page_all)
        result = re.search(r"\"Data\":(\[.*\])", response).group(1)
        data = re.search(r"\"Data\":(\[.*?\])", result).group(1)
        
        if len(data) == '[]':
            return
        datas = self.toJsonForm(title, data)
        # print(title)
        return page_all, title, datas
    def writeHeader(self, data):
        title_lst = []
        for key, value in util.longhu_title.items():
            if value != '':
                title_lst.append(value)
            else:
                title_lst.append(key)
        # print('title_lst: ', title_lst)
        with open('eastmoney.csv', 'a', encoding='utf_8_sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(title_lst)
    def writeTable(self, data):
        # print(data)
        for d in data[2]:
            # print('d: ', d)
            with open('eastmoney.csv', 'a', encoding='utf_8_sig', newline='') as f:
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
    def getAllDatas(self):
        self.writeHeader(self.getTable(1)[2])
        page_all = int(self.getTable(1)[0])
        for page in range(1, page_all):
            data = self.getTable(page)
            self.writeTable(data)