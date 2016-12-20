# -*- coding:utf-8 -*-
from common import const
import requests


class FlightInfoResult:
    def __init__(self, origin, destination, arrive_at, depart_at, price_per_adult, tax_per_adult, total_price, flight_number, marketing_airline,travel_class, seats_remaining,  currency="CNY"):
        self.origin = origin
        self.destination = destination
        self.arrive_at = arrive_at
        self.depart_at = depart_at
        self.price_per_adult = price_per_adult
        self.tax_per_adult = tax_per_adult
        self.total_price = total_price
        self.marketing_airline = marketing_airline
        self.flight_number = flight_number
        self.travel_class = travel_class
        self.seats_remaining = seats_remaining
        self.currency = currency


class FlightInfoQuery:
    def __init__(self, **kwargs):
        self.apikey = const.APIKEY
        for key, value in kwargs.items():
            self.__dict__['%s' % key] = value

    def get_trip_result(self):
        return requests.get(const.LOWFARE_URL, params=self.__dict__).json()
            
    def get_low_fare_result(self):
        response = requests.get(const.LOWFARE_URL, params=self.__dict__).json()
        currency = response['currency']
        if hasattr(self,"return_date"):
            print("往返")
        else:
            for result in response["results"]:
                flight_detail = result["itineraries"][0]["outbound"]["flights"][0]
                fare = result["fare"]
                flight_info = FlightInfoResult(origin="airport:%s terminal:%s" % (flight_detail["origin"]["airport"],flight_detail["origin"]["terminal"]),
                                               destination="airport:%s terminal:%s" % (flight_detail["destination"]["airport"],flight_detail["destination"]["terminal"]),
                                               arrive_at=flight_detail["arrives_at"],
                                               depart_at=flight_detail["departs_at"],
                                               total_price=fare["total_price"],
                                               price_per_adult=fare["price_per_adult"]["total_fare"],
                                               tax_per_adult=fare["price_per_adult"]["tax"],
                                               flight_number=flight_detail["flight_number"],
                                               marketing_airline=flight_detail["marketing_airline"],
                                               travel_class=flight_detail["booking_info"]["travel_class"],
                                               seats_remaining=flight_detail["booking_info"]["seats_remaining"],
                                               currency=currency
                                               )
                yield flight_info




if __name__ == '__main__':
    params = {'origin':'BOS','destination':'LON','departure_date':'2016-12-30','number_of_results':'5','nonstop':'true'}
    fli = FlightInfoQuery(**params)
    response = fli.get_low_fare_result()
    for result in response:
        print (result.__dict__)
