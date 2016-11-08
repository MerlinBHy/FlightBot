# -*- coding:UTF-8 -*-
import requests


class GetFlightInfoRequest:

    def __init__(self, origin,destination,departure_date,flight_type,duration="1-7",direct=True,desc=True):
        self.req_url = "https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?apikey=Lw8RARxb4lZDmdiqcPeE6lZyz07rJ9Vw"
        self.origin = origin
        self.destination = destination
        self.departure_date = departure_date
        if flight_type == "OW":
            self.one_way = True
        else:
            self.one_way = False
        self.duration = duration#停留时间
        self.direct = direct#直飞
        self.desc = desc#价格降价排序

    def send_request(self):
        param = {"origin":"NYC",
                 "destination":"lax",
                 "departure_date": "%d-%d-%d" % (self.departure_date.year, self.departure_date.month, self.departure_date.day),
                 "one-way":self.one_way,
                 #"duration":self.duration,
                 "direct":self.direct,
                 }
        res = requests.get(self.req_url, params=param)
        print res.url
        print res.json()

