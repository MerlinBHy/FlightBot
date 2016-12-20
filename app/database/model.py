# -*- coding: utf-8 -*-
'''
Created on 2016-12-14
@author bhy
'''
import datetime
from app import SQLAlchemyDB as db
from app.shared import DateTransfer,const,QuestionStr,CitySearch

class FlightSegment:
    def __init__(self,uid = None):
        self.departure = None
        self.destination = None
        self.start_date = None
        self.status = 0
        self.uid = uid

class AllFlightSegment:
    nlp = const.NLP

    def __init__(self,uid):
        self.flight_segment_list = []
        self.uid = uid

    def __add_segment(self, flight_segment):
        self.flight_segment_list.append(flight_segment)

    def __remove_segment(self,flight_segment):
        self.flight_segment_list.remove(flight_segment)

    def __clear_segment(self):
        self.flight_segment_list = []

    def __change_segment(self, old_segment, new_segment):
        try:
            index = self.flight_segment_list.index(old_segment)
            self.flight_segment_list[index] = new_segment
        except IndexError:
            print("没有相应的行程段1")
        else:
            print("没有相应的行程段2")

    def analyse_locations(self,text):
        text = DateTransfer.date_transfer(text)
        to_tuple = (u"到",u"去",u"飞",u"回",u"飞回",u"飞到",u"飞往")
        from_tuple = (u"从",)
        destination_locations = []
        departure_locations = []
        words = self.nlp.tag(text, space_mode=0, oov_level=3, t2s=0, special_char_conv=0)[0]["word"]
        tags = self.nlp.tag(text, space_mode=0, oov_level=3, t2s=0, special_char_conv=0)[0]["tag"]
        status = 0
        temp_location = ""
        for i in range(0,len(words)):
            if words[i] in from_tuple:
                status = 1
                temp_location = ""
            if words[i] in to_tuple:
                if status != 2 and temp_location != "":
                    departure_locations.append(temp_location)
                elif temp_location != "":
                    destination_locations.append(temp_location)
                status = 2
                temp_location = ""
            if tags[i] == "ns":
                temp_location += words[i]
        if temp_location != "" and status == 2:
            destination_locations.append(temp_location)
        for i in range(0, len(departure_locations)):
            flight_segment = FlightSegment(self.uid)
            flight_segment.departure = departure_locations[i]
            flight_segment.destination = destination_locations[i]
            self.flight_segment_list.append(flight_segment)
        if len(departure_locations) < len(destination_locations):
            for i in range(len(departure_locations) - 1, len(destination_locations) - 1):
                flight_segment = FlightSegment(self.uid)
                flight_segment.departure = destination_locations[i]
                flight_segment.destination = destination_locations[i+1]
                self.flight_segment_list.append(flight_segment)
        self.__save_flight_detail()
        return

    def __save_flight_detail(self):
        for flight_segment in self.flight_segment_list:
            flight = FlightInfo(uid=flight_segment.uid,start_location=flight_segment.departure, end_location=flight_segment.destination,
                                flight_type=1,status=4)
            flight.save()

class FlightInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80))
    start_location = db.Column(db.String(120))
    end_location = db.Column(db.String(120))
    start_date = db.Column(db.String(120))
    return_date = db.Column(db.String(120))
    flight_type = db.Column(db.INTEGER)
    status = db.Column(db.INTEGER)
    complete = db.Column(db.Boolean)
    update_time = db.Column(db.DATETIME, default=datetime.datetime.utcnow())
    nlp = const.NLP

    def __init__(self,uid,start_location=None,end_location=None,flight_type=None,status=0):
        # 状态：0 ：初始状态内容为空 1:缺少起始城市 2:缺少到达城市 3 缺少类型（往返或者单程）
        # 4:缺少出发时间 5缺少返回时间 6：完成
        self.uid = uid
        self.start_location = start_location
        self.end_location = end_location
        self.start_date = None
        self.return_date = None
        #航班类型1：单程 2：往返
        self.flight_type = flight_type
        self.status = status
        self.complete = False

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_qstr(self):
        q = QuestionStr()
        if self.status == 4:
            return ( u"您从" + self.start_location + u"到" + self.end_location +u"的行程" + q.get_question_str(self.status))
        if self.status == 5:
            return (u"您从" + self.end_location + u"返回" + self.start_location + u"的行程"+ q.get_question_str(self.status))
        if self.status == 6:
            return q.get_question_str(self.status) + self.start_location + u'到' + self.end_location + u'的机票'
        else:
            return q.get_question_str(self.status)

    def analyse(self,text):
        text = DateTransfer.date_transfer(text)
        self.__get_flight_info(text)
        self.__change_status()
        self.save()

    def get_dict(self):
        rst={}
        rst['origin'] = CitySearch.get_city_code(self.start_location)
        rst['destination'] = CitySearch.get_city_code(self.end_location)
        rst['departure_date'] = self.start_date
        if self.return_date is None:
            return rst
        else:
            rst['return_date']=self.return_date

    def __get_flight_type(self,text):
        result = self.nlp.tag(text)[0]['word']
        for d in result:
            if d == u"单程":
                self.flight_type = 1
                break
            if d == u"往返":
                self.flight_type = 2
                break

    def __get_flight_info(self, text):
        times = []
        locations = []
        result = self.nlp.ner(text)[0]
        words = result['word']
        entities = result['entity']
        for entity in entities:
            if entity[2] == "time":
                times.append(words[entity[0]:entity[1]])
            if entity[2] == "location":
                locations.append(words[entity[0]:entity[1]])
        self.__get_flight_type(text)
        if len(times) == 2:
            self.start_date = self.__date_trans(times[0])
            self.return_date = self.__date_trans(times[1])
        if self.return_date is None and self.start_date is not None and len(times) == 1:
            self.return_date = self.__date_trans(times[0])
        if self.start_date is None and len(times) == 1:
            self.start_date = self.__date_trans(times[0])
        if len(locations) == 2:
            self.start_location = "%s" % locations[0][0]
            self.end_location = "%s" % locations[1][0]
            return
        if len(locations) == 1 and self.start_location is None:
            self.start_location = "%s" % locations[0][0]
            return
        if len(locations) == 1 and self.start_location is not None:
            self.end_location = "%s" % locations[0][0]
            return

    def __date_trans(self,date):
        ret = u""
        for d in date:
            ret += d
        return ret

    def __change_status(self):
        if self.start_location is None:
            self.status = 1
            return
        if self.end_location is None:
            self.status = 2
            return
        if self.flight_type is None:
            self.status = 3
            return
        if self.start_date is None:
            self.status = 4
            return
        if self.flight_type == 2 and self.return_date is None:
            self.status = 5
            return
        self.status = 6
        return

    def change_complete(self):
        self.complete = True
        self.save()


class DialogueResult:
    def __init__(self, complete=False, question="", dialogue_result={}):
        self.complete = complete
        self.question = question
        self.dialogue_result = dialogue_result




