# -*- coding:UTF-8 -*-
import re
import datetime
from Exception import DateTransferException
from ConstElements import const
from bosonnlp import BosonNLP

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
                    replace_str += str(year) + "年"
                    replace_str += str(month) + "月"
                    replace_str += str(day) + "日"
                    #temp_time = BosonNLP(const.APPKEY).convert_time(replace_str, datetime.datetime.today())
                    #replace_str = temp_time["timestamp"]
                    result = re.subn(reg_str_with_year, replace_str, result, count=1)[0].encode("utf-8")
                else: raise DateTransferException
                match = re.search(reg_str_with_year, result)

            except DateTransferException, d:
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
                    replace_str += str(year) + "年"
                    replace_str += str(month) + "月"
                    replace_str += str(day) + "日"
                    #replace_str = const.NLP.convert_time(replace_str,datetime.datetime.today())["timestamp"]
                    result = re.subn(reg_str_without_year, replace_str, result, count=1)[0].encode("utf-8")
                else: raise DateTransferException
            except DateTransferException, d:
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


if __name__ == '__main__':
    print(DateTransfer.date_transfer("huhuhuh92-11-23jssd92.11.98ijiji"))