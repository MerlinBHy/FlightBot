# -*- coding:UTF-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("UTF-8")


class DateTransferException(Exception):
    def __init__(self):
        self.msg = "时间转换时出错，请输入正确的时间"