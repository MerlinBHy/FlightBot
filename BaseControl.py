# -*- coding:UTF-8 -*-
import sys
from QuestionStr import QuestionStr
from ConstElements import const
from FlightSegment import FlightSegment
from FlightSegment import AllFlightSegment
from FlightInfo import FlightInfo


'''
    开始（输入的内容可能有 1）地点，与当前所在地进行匹配，如果相同作为起始地点，否则作为目的地。创建一段行程
                            2) 包含多个地点或者时间信息的语句，获取关键信息创建一段或者几段行程
                            3）其他
    状态:  0 初始态  1 确定了类型，多段或者单次，多段用

'''

def main():
    flight_segments = AllFlightSegment()
    flight_info = FlightInfo()
    while True:
        text = QuestionStr().get_question_str(0)()
        result = const.NLP.ner(text)[0]
        tags = result["tag"]
        if tags.count("ns") > 2:
            flight_segments.analyse_locations(text)
            break;
        elif tags.count("ns") > 0:
            flight_info.control_center(text=text)
            break;
        elif "订票" in text or "机票" in text:
            flight_info.control_center(status=1)
            break;

if __name__ == '__main__':
    main()