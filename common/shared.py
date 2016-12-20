# -*- coding: utf-8 -*-
'''
Created on 2016-12-14
@author bhy
'''
import os
import datetime
import re

from bosonnlp import BosonNLP

from common import const

const.APIKEY = "PVKqAK3eGjceCcrvQF3OVRefZAYZQQRU"
const.LOWFARE_URL = "https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search"
const.INSPIRATION_URL = "https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search"
const.APPKEY = "K08ZGK-o.10455.nEdxL3yYLAWC"
const.NLP = BosonNLP("K08ZGK-o.10455.nEdxL3yYLAWC")
const.MAXDURATION = 300


class DateTransfer:
    def __init__(self):
        return

    @staticmethod
    def date_transfer(date_str):
        reg_str_with_year = "(?P<year>[0-9]{2,4})[/,\.,\-](?P<month>[0-3]?[0-9])[/,\.,\-](?P<day>[0-3]?[0-9])"
        reg_str_without_year = "(?P<month>[0-1]?[0-9])[/,\.,\-](?P<day>[0-3]?[0-9])"
        result = date_str
        match = re.search(reg_str_with_year, result)
        while match:
            replace_str = ""
            try:
                month = int(match.group("month"))
                day = int(match.group("day"))
                year = int(match.group("year"))
                if 50 < year < 100:
                    year += 1900
                if year < 50:
                    year += 2000
                validate = DateTransfer.check_validate(year, month, day)
                if validate == 1:
                    replace_str += str(year) + u"年"
                    replace_str += str(month) + u"月"
                    replace_str += str(day) + u"日"
                    result = re.subn(reg_str_with_year, replace_str, result, count=1)[0].encode("utf-8")
                else: raise Exception
                match = re.search(reg_str_with_year, result)

            except Exception, d:
                print (d.msg)
                return None
        match = re.search(reg_str_without_year, result)
        while match:
            replace_str = ""
            try:
                month = int(match.group("month"))
                day = int(match.group("day") )
                year = datetime.datetime.now().year
                validate = DateTransfer.check_validate(year, month, day)
                if validate == 1:
                    replace_str += str(year) + u"年"
                    replace_str += str(month) + u"月"
                    replace_str += str(day) + u"日"
                    #replace_str = const.NLP.convert_time(replace_str,datetime.datetime.today())["timestamp"]
                    result = re.subn(reg_str_without_year, replace_str, result, count=1)[0].encode("utf-8")
                else: raise Exception
            except Exception, d:
                print (d.msg)
                return None
            match = re.search(reg_str_without_year, result)
        return result

    @staticmethod
    def check_validate(year, month, day):
        days_in_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        validate = 0
        if month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            if 1 <= day <= 29:
                validate = 1
        elif 1 <= month <= 12:
            if 1 <= day <= days_in_month[month - 1]:
                validate = 1
        return validate

class CitySearch:

    @staticmethod
    def get_city_code(city):
        basedir = os.path.abspath(os.path.dirname(__file__))
        citypath = os.path.join(basedir, 'cities.txt')
        fo = open(citypath, "r")
        for line in fo:
            items = line.split("|")
            if city in items[3].decode('utf-8'):
                fo.close()
                return items[0].decode('utf-8')
        fo.close()
        return None

    @staticmethod
    def get_city_name(code):
        fo = open("./cities.txt","r")
        for line in fo:
            items = line.split("|")
            if code == items[0].decode('utf-8'):
                fo.close()
                return items[3].decode('utf-8').split("，")[0]
        fo.close()
        return None

class QuestionStr:
    def __init__(self):
        self.start_q = u"请问有什么可以帮您？\n"
        self.start_location_q = u"请问您的出发城市是？\n"
        self.end_location_q = u"请问您的目标城市是？\n"
        self.fight_type_q = u"请问是单程航班还是往返航班？\n"
        self.start_date_q = u"出发日期是？\n"
        self.return_date_q = u"返回日期是\n"
        self.end_str =u"你需要预订的是："
        self.cancel_str_q = u"确认取消当前查询（是、否）？\n"
        self.canceled_str = u"查询已取消，请重新查询\n"
        self.change_str = u"需要修改的条件是（出发、到达、日期）？\n"

    def get_question_str(self, status):
        switcher = {
            0: self.start_q,
            1: self.start_date_q,
            2: self.end_location_q,
            3: self.fight_type_q,
            4: self.start_date_q,
            5: self.return_date_q,
            6: self.end_str,
            7: self.cancel_str_q,
            8: self.canceled_str
        }
        txt = switcher.get(status, lambda: "nothing")
        return txt