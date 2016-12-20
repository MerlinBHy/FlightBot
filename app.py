# -*- coding=utf-8 -*-

import os
import sys
import json
from common import instance
from amadeus.FlightInfo import FlightInfoQuery
import requests
from facebook.tripconvertor import itineraryconvertor
from flask import request
from dialogue import bussiness

reload(sys)
sys.setdefaultencoding("utf-8")

app = instance.app

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


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

                    sessionresult = bussiness.analyse_text(recipient_id, message_text)
                    if(sessionresult.complete):
                        params = sessionresult.dialogue_result
                        params['number_of_results'] = '1'
                        params['nonstop'] = 'true'
                        fli = FlightInfoQuery(**params)
                        response = fli.get_trip_result()
                        iticonvertor = itineraryconvertor()
                        fbresults = iticonvertor.convert_from_1A_to_fb(response)
                        for fbresult in fbresults:
                            send_journey(sender_id, fbresult)
                    else:
                        send_message(sender_id, sessionresult.question)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_journey(recipient_id, message_text):

    log(u"sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_message(recipient_id, message_text):
    log(u"sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

        

def log(message):  # simple wrapper for logging to stdout on heroku
    print message
    sys.stdout.flush()


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(threaded=True)
