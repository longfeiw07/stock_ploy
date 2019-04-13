# -*- coding: utf-8 -*-

import requests
import re
import json
import csv
class Reptile():
    def __init__(self):
        pass
    def getUrl(self):
        url = "http://datainterface3.eastmoney.com//EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?"
        return url
    def getResponse(self):
        params = {
            'tkn': 'eastmoney',
            'mkt': '0',
            'dateNum': '',
            'startDateTime': '2014-04-13',
            'endDateTime': '2014-05-13',
            'sortRule': '1',
            'sortColumn': '',
            'pageNum': '1',
            'pageSize': '50',
            'cfg': 'lhbggdrtj'
            }
        url = self.getUrl()
        response = requests.get(url, params=params).text
        return response
    def getDatas(self):
        response = self.getResponse()
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