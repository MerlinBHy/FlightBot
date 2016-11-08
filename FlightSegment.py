# -*- coding:UTF-8-*-
from FlightInfo import FlightInfo
from ConstElements import const
from DateTransfer import DateTransfer


class FlightSegment:
    def __init__(self):
        self.departure = None
        self.destination = None
        self.start_date = None
        self.status = 0


class AllFlightSegment:
    nlp = const.NLP

    def __init__(self):
        self.flight_segment_list = []
        self.flight_info_list = []

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
        to_tuple = ("到","去","飞","回","飞回","飞到","飞往")
        from_tuple = ("从",)
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
            flight_segment = FlightSegment()
            flight_segment.departure = departure_locations[i]
            flight_segment.destination = destination_locations[i]
            self.flight_segment_list.append(flight_segment)
        if len(departure_locations) < len(destination_locations):
            for i in range(len(departure_locations) - 1, len(destination_locations) - 1):
                flight_segment = FlightSegment()
                flight_segment.departure = destination_locations[i]
                flight_segment.destination = destination_locations[i+1]
                self.flight_segment_list.append(flight_segment)
        self.__get_flight_detail()
        return

    def __analyse_times(self,text):
        '''
        事件处理 TO DO
        '''
        text = DateTransfer.date_transfer(text)
        result = self.nlp.ner(text)[0]
        words = result['word']
        entities = result['entity']
        for entity in entities:
            if entity[2] == "time":
                yield words[entity[0]:entity[1]]

    def __get_flight_detail(self):
        for flight_segment in self.flight_segment_list:
            flight = FlightInfo(start_location=flight_segment.departure, end_location=flight_segment.destination,
                                flight_type=1,status=4)
            flight.control_center()
            self.flight_info_list.append(flight)

if __name__ == '__main__':
    f = AllFlightSegment()
    f.analyse_locations("从中国台湾飞英国曼彻斯特再飞回中国香港再到法国巴黎")

    print (".")