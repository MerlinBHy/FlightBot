# -*- coding: utf-8 -*-
'''
Created on 2016-12-14
@author bhy
'''
import datetime
from common import const
from database.model import FlightInfo,AllFlightSegment,DialogueResult


def analyse_text(uid,text):
    f = FlightInfo.query.filter_by(uid=uid,complete=False).first()
    if f is None:
        '''新订单'''
        result = const.NLP.ner(text)[0]
        tags = result["tag"]
        if tags.count("ns") == 0:
            return DialogueResult(question=u"我好像不明白你在说什么")
        if tags.count("ns") > 2:
            fs = AllFlightSegment(uid)
            fs.analyse_locations(text)
        elif tags.count("ns") > 0:
            fl = FlightInfo(uid)
            fl.analyse(text)
        f = FlightInfo.query.filter_by(uid=uid,complete=False).first()
        if f.status == 6:
            f.change_complete()
            dialogue_result = DialogueResult(complete=True,question="",dialogue_result=f.get_dict())
        else:
            dialogue_result = DialogueResult(complete=False, question=f.get_qstr())
        return dialogue_result
    else:
        duration = (datetime.datetime.utcnow() - f.update_time).total_seconds()

        if duration > const.MAXDURATION:
            '''超时请求，需要重新输入'''
            f.change_complete()
            return DialogueResult(question=u"请求超时，输入已失效，请重新输入")

        '''有订单'''
        f.analyse(text)
        rst = FlightInfo.query.filter_by(id=f.id).first()
        if rst.status == 6:
            rst.change_complete()
            dialogue_result = DialogueResult(complete=True,question="",dialogue_result=rst.get_dict())
        else:
            dialogue_result = DialogueResult(complete=False, question=rst.get_qstr())
        return dialogue_result


def query_userinfo(uid):
    f = FlightInfo.query.filter_by(uid = uid).first()
    return f.uid




