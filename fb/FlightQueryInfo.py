# -*- coding:utf-8 -*-
import datetime
from shared import db
from shared import const
from shared import DateTransfer
from shared import CitySearch
from shared import QuestionStr

class FlightInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80))
    start_location  = db.Column(db.String(120))
    end_location = db.Column(db.String(120))
    start_date = db.Column(db.String(120))
    return_date = db.Column(db.String(120))
    flight_type = db.Column(db.INTEGER)
    status = db.Column(db.INTEGER)
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


    def __get_location_info(self, text):
        result = self.nlp.ner(text)[0]
        words = result['word']
        entities = result['entity']
        for entity in entities:
            if entity[2] == "location":
                yield words[entity[0]:entity[1]]

    def __get_time_info(self,text):
        result = self.nlp.ner(text)[0]
        words = result['word']
        entities = result['entity']
        for entity in entities:
            if entity[2] == "time":
                yield words[entity[0]:entity[1]]

    def __get_flight_type(self,text):
        result = self.nlp.tag(text)[0]['word']
        for d in result:
            if d.decode() == "单程":
                self.flight_type = 1
                break
            if d.decode() == "往返":
                self.flight_type = 2
                break

    def __analyse_locations(self,text):
        to_tuple = ("到","去","飞","回","飞回","飞到","飞往")
        from_tuple = ("从",)
        destination_locations = []
        departure_locations = []
        words = self.nlp.tag(text,space_mode=0, oov_level=3, t2s=0, special_char_conv=0)[0]["word"]
        tags = self.nlp.tag(text,space_mode=0, oov_level=3, t2s=0, special_char_conv=0)[0]["tag"]
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
            self.start_date = times[0]
            self.return_date = times[1]
        if self.return_date is None and self.start_date is not None and len(times) == 1:
            self.return_date = times[0]
        if self.start_date is None and len(times) == 1:
            self.start_date = times[0]
        if len(locations) == 2:
            self.start_location = locations[0]
            self.end_location = locations[1]
            return
        if len(locations) == 1 and self.start_location is None:
            self.start_location = locations[0]
            return
        if len(locations) == 1 and self.start_location is not None:
            self.end_location = locations[0]
            return

    def __save_info(self):
        db.session.add(self)
        db.session.commit()

    def __get_info(self):

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

    def format_info(self):
        for key in self.__dict__:
            if self.__dict__ is not None:
                temp = ""
                if isinstance(self.__dict__[key],list):
                    for item in self.__dict__[key]:
                        temp += item
                    self.__dict__[key] = temp
                if key == "start_date" or key == "end_date":
                    self.__dict__[key] = self.nlp.convert_time(self.__dict__[key], datetime.datetime.today())["timestamp"]
                    self.__dict__[key] = datetime.datetime.strptime(self.__dict__[key], '%Y-%m-%d %H:%M:%S')
                if key == "start_location" or key == "end_location":
                    self.__dict__[key] = CitySearch.get_city_code(self.__dict__[key])
        switcher = {
            1: "OW",
            2: "RT"
        }
        self.flight_type = switcher.get(self.flight_type, lambda: "nothing")
        print (self.__dict__)
        return


    def control_center(self, text=None,status=None):
        '''
        1.分析text，更新状态 2.返回问句
        '''
        q = QuestionStr()
        if status is not None:
            self.status = status
        if text is not None:
            text = DateTransfer.date_transfer(text)
            self.__get_flight_info(text)
            self.__change_status()

        if self.status == 4:
            return ( "您从" + self.start_location[0] + "到" + self.end_location[0] +"的行程" + q.get_question_str(self.status))
        if self.status == 5:
            return ("您从" + self.end_location[0] + "返回" + self.start_location[0] + "的行程"+ q.get_question_str(self.status))
        text = q.get_question_str(self.status)
        return text