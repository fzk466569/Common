#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: fzk
# @Time  12:07

import re
import time
import json
import datetime
from decimal import Decimal, InvalidOperation
from collections import deque

import requests


class Stock(object):
    def __init__(self, code='sh601519'):
        self.code = code
        self.base = 'http://hq.sinajs.cn/list='
        self.format = ['name', 'open_price', 'last_close_price', 'cur_price', 'top_price', 'low_price', 'buy1', 'sell1',
                       'deal_num', 'deal_price', 'buy1_num', '_', 'buy2_num', 'buy2', 'buy3_num', 'buy3',
                       'buy4_num', 'buy4', 'buy5_num', 'buy5', 'sell1_num', '_', 'sell2_num', 'sell2', 'sell3_num',
                       'sell3', 'sell4_num', 'sell4', 'sell5_num', 'sell5', 'date', 'time']
        self.data = None
        self.maxlen = 12
        self.deque = deque(maxlen=self.maxlen)
        self.flag = True

    def get_html(self):
        resp = requests.get(self.base + self.code)
        return resp

    @staticmethod
    def str2int(s):
        # 字符串转数字
        try:
            return Decimal(s)
        except InvalidOperation as e:
            return int(s) if s.isdigit() else s

    def parse(self, response):
        data = re.search('"(.*)"', response.text).group(1)
        self.data = dict(zip(self.format, map(self.str2int, [x for x in data.split(',')])))

    def listen(self):
        self.parse(self.get_html())

    def rule(self):
        # 制定提醒规则
        buy1_num = self.data['buy1_num'] // 100
        self.deque.append(buy1_num)
        cur_time = datetime.datetime.now()
        print(cur_time, '当前涨停板', buy1_num)
        if buy1_num <= Decimal(10000):
            print(cur_time, '涨停板只剩10000手赶快查看')
            self.flag = False
        if len(self.deque) >= self.maxlen:
            # v 表示1分钟的变化量
            v = self.deque[-1] - self.deque[0]
            if v > 0:
                status = '+'
            elif v < 0:
                status = '-'
                v = -v
            else:
                status = ''
            print(cur_time, '相对于1分钟前涨停板 {0}{1}'.format(status, v))
            # v1 表示5秒钟的变化量
            v1 = self.deque[-1] - self.deque[-2]
            if v1 > 0:
                status = '+'
            elif v1 < 0:
                status = '-'
                v1 = -v1
            else:
                status = ''
            print(cur_time, '相对于5秒前涨停板 {0}{1}'.format(status, v1))

        else:
            print(cur_time, '1分钟初始化时间')

    def dictify(self):
        return json.dumps(self.data, default=lambda x: x.to_eng_string())


if __name__ == '__main__':
    code = 'sh600776'
    stock = Stock(code=code)
    while stock.flag:
        stock.listen()
        stock.rule()
        time.sleep(5)
