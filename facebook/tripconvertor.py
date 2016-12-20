#!/usr/bin/python
#encoding=utf-8

from tripmessage import *

class itineraryconvertor:

    def convert_from_1A_to_fb(self, response):
        results = []
        results1A = response["results"]
        if(results1A is None or len(results1A) == 0):
            return results

        psginfos=[]
        psgid = "p001"
        psginfos.append(self.create_psginfo(psgid, "Joyce"))

        currency = response["currency"]
        for result1A in results1A:
            flightinfos = []
            psgseginfos = []

            itinerary1A = result1A["itineraries"][0]
            outbound1A = itinerary1A["outbound"]
            outflights1A = outbound1A["flights"]
            self.convert_one_side(outflights1A, 0, flightinfos, psgseginfos, psgid)

            inbound1A = None
            if("inbound" in itinerary1A.keys()):
                inbound1A = itinerary1A["inbound"]
            if(inbound1A is not None):
                inflights1A = inbound1A["flights"]
                self.convert_one_side(inflights1A, len(outflights1A), flightinfos, psgseginfos, psgid)
            
            fare1A = result1A["fare"]
            totalprice = fare1A["total_price"]
            payload = self.create_payload(psginfos, flightinfos, psgseginfos, totalprice, currency)

            results.append(attachment(payload).__dict__)

        return results

            
    def convert_one_side(self, flights1A, start, flightinfos, psgseginfos, psgid):
        if(flights1A is None or len(flights1A) == 0):
            return
        
        for fltidx in range(len(flights1A)):
            flight1A = flights1A[fltidx]
            connid = ("c00%d" % (fltidx + start))
            segid = ("s00%d" % (fltidx + start))
            fltinfo = self.create_fltinfo(connid, segid, flight1A)
            flightinfos.append(fltinfo)

            seatclass = flight1A["booking_info"]["travel_class"]
            psgseginfo = self.create_psgseginfo(segid, psgid, seatclass)
            psgseginfos.append(psgseginfo)

        
            
    def create_payload(self, psginfos, fltinfos, psgseginfos, totalprice, currency):
        pl = payload("ABCDEF", psginfos, fltinfos, psgseginfos, totalprice, currency)
        return pl.__dict__

    def create_psginfo(self, psgid, name):
        psginfo = passenger_info(psgid, name)
        return psginfo.__dict__

    def create_fltinfo(self, connid, segid, flight1A):
        fltno = flight1A["flight_number"]
        origin1A = flight1A["origin"]
        destination1A = flight1A["destination"]
        dairport = self.create_airport(origin1A)
        aairport = self.create_airport(destination1A)
        schedule = self.create_schedule(flight1A)
        travelclass = flight1A["booking_info"]["travel_class"].lower()
        aircrafttype = flight1A["aircraft"]
        fltinfo = flight_info(connid, segid, fltno, dairport, aairport, schedule, travelclass, aircrafttype)
        return fltinfo.__dict__

    def create_psgseginfo(self, segid, psgid, travelclass):
        psgseginfo = passenger_segment_info(segid, psgid, "unkonwn", travelclass)
        return psgseginfo.__dict__

    def create_airport(self, airport1A):
        portcode = airport1A["airport"]
        port = airport(portcode, portcode, airport1A["terminal"])
        return port.__dict__

    def create_schedule(self, flight1A):
        schedule = flight_schedule(flight1A["departs_at"], flight1A["arrives_at"])
        return schedule.__dict__
