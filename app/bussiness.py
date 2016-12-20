# -*- coding: utf-8 -*-
'''
Created on 2016-12-14
@author bhy
'''
from app.database.model import FlightInfo,AllFlightSegment,DialogueResult
from app.shared import const

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
            result = f.get_dict()
            dialogue_result = DialogueResult(complete=f.complete,question="",dialogue_result=f.get_dict())
        else:
            dialogue_result = DialogueResult(complete=f.complete, question=f.get_qstr())
        return dialogue_result
    else:
        '''有订单'''
        f.analyse(text)
        rst = FlightInfo.query.filter_by(id=f.id).first()
        if rst.status == 6:
            rst.change_complete()
            dialogue_result = DialogueResult(complete=rst.complete,question="",dialogue_result=rst.get_dict())
        else:
            dialogue_result = DialogueResult(complete=rst.complete, question=rst.get_qstr())
        return dialogue_result





def query_userinfo(uid):
    f = FlightInfo.query.filter_by(uid = uid).first()
    return f.uid




