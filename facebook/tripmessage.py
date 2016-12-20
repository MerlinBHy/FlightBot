#!/usr/bin/python
#encoding=utf-8

import json

class attachment:
    'trip result template'

    def __init__(self, payload):
        self.type = "template"
        self.payload = payload

    def __str__(self):
        return json.dumps(self.__dict__)


class payload:
    'trip result'

    def __init__(self, pnr_number, passenger_info, flight_info, passenger_segment_info, total_price, currency, theme_color='#009ddc', price_info=[], base_price=None, tax=None):
        self.template_type = 'airline_itinerary'
        self.intro_message = 'Here\'s your flight itinerary.'
        self.locale = 'en_US'
        self.pnr_number = pnr_number
        self.passenger_info = passenger_info
        self.flight_info = flight_info
        self.passenger_segment_info = passenger_segment_info
        self.total_price = total_price
        self.currency = currency
        self.theme_color = theme_color
        self.price_info = price_info
        self.base_price = base_price
        self.tax = tax

    def __str__(self):
        return json.dumps(self.__dict__)


class passenger_info:
    'info of passenger'

    def __init__(self, passenger_id, name, ticket_number=None):
        self.passenger_id = passenger_id
        self.name = name
        self.ticket_number = ticket_number

    def __str__(self):
        return json.dumps(self.__dict__)

    
class flight_info:
    'info of flight'

    def __init__(self, connection_id, segment_id, flight_number, departure_airport, arrival_airport, flight_schedule, travel_class, aircraft_type=None):
        self.connection_id = connection_id
        self.segment_id = segment_id
        self.flight_number = flight_number
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.flight_schedule = flight_schedule
        self.travel_class = travel_class
        self.aircraft_type = aircraft_type

    def __str__(self):
        return json.dumps(self.__dict__)


class passenger_segment_info:
    'map of passenger and segment'

    def __init__(self, segment_id, passenger_id, seat, seat_type, product_info=[]):
        self.segment_id = segment_id
        self.passenger_id = passenger_id
        self.seat = seat
        self.seat_type = seat_type
        self.product_info = product_info

    def __str__(self):
        return json.dumps(self.__dict__)
    
        
class airport:

    def __init__(self, airport_code, city, terminal, gate=None):
        self.airport_code = airport_code
        self.city = city
        self.terminal = terminal
        self.gate = gate

    def __str__(self):
        return json.dumps(self.__dict__)
    
        
class flight_schedule:

    def __init__(self, departure_time, arrival_time, boarding_time=None):
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def __str__(self):
        return json.dumps(self.__dict__)
    

class price_info:

    def __init__(self, title, amount, currency=None):
        self.title = title
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return json.dumps(self.__dict__)
    

class product_info:

    def __init__(self, title, value):
        self.title = title
        self.value = value

    def __str__(self):
        return json.dumps(self.__dict__)
