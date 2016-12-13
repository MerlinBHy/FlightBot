# -*- coding:UTF-8 -*-
from shared import const
from shared import QuestionStr
from flight_segments import AllFlightSegment
from FlightQueryInfo import FlightInfo

def analyse(text,uid):
    current_flight_info_list = FlightInfo.query.filter_by(uid=uid)

    flight_segments = AllFlightSegment()
    result = const.NLP.ner(text)[0]
    tags = result["tag"]
    if tags.count("ns") > 2:
        flight_segments.analyse_locations(text)