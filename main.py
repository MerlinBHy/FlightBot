# -*- coding=utf-8 -*-
import os
import sys
import json
from common import instance
import requests
from dialogue import bussiness
from flask import request
from amadeus.FlightInfo import FlightInfoQuery
from facebook.tripconvertor import itineraryconvertor

reload(sys)
sys.setdefaultencoding("utf-8")

app = instance.app

@app.route('/', methods=['GET'])
def verify():
    uid = request.args.get("uid")
    text = request.args.get("text")
    l = bussiness.analyse_text(uid,text)
    if l.complete:
        params = l.dialogue_result
        params['number_of_results'] = '1'
        params['nonstop'] = 'true'
        fli = FlightInfoQuery(**params)
        response = fli.get_trip_result()
        iticonvertor = itineraryconvertor()
        fbresults = iticonvertor.convert_from_1A_to_fb(response)
        send_message(uid, fbresults)
        return u"%s" % fbresults,200
    else:
        return l.question,200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    send_message(sender_id, "got it, thanks!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log(u"sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        #"access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

    return data
#    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
#    if r.status_code != 200:
#        log(r.status_code)
#        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print message
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(threaded=True)
