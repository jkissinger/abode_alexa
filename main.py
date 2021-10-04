import io
import json
import logging
import time
import os

import requests

import door_state
import gmail_checker
import options

FORMAT = '%(asctime)-15s %(levelname)-10s %(message)s'
logging.basicConfig(format=FORMAT, filename='abode_alexa.log', level=logging.INFO)

settings = {}
scriptdir = os.path.dirname(os.path.realpath(__file__))

with io.open(scriptdir + '/settings.json', "r", encoding="utf-8") as json_file:
    settings = json.load(json_file)


def announce(announcement):
    if options.ANNOUNCEMENTS_ENABLED:
        response = requests.get(settings['announcement_url'] + announcement.replace(' ', '%20'))
        if not response.ok:
            logging.error("Announcement response: " + str(response))
    else:
        logging.debug("Would be announcing: " + announcement)


def process_notifications():
    notifications = gmail_checker.check_notifications()
    for notification in notifications:
        logging.debug("Processing: " + notification)
        tokenized = notification.split(" ")
        door_name = tokenized[2:len(tokenized) - 1]
        door_name = ' '.join(door_name)
        door_name = door_name.replace(" Door", "")
        state = tokenized[len(tokenized) - 1]
        door_state.update_door_state(door_name, state)



def announce_doors_to_close():
    doors_to_close = door_state.validate_door_states()
    # TODO This will do multiple announcements if multiple doors are open, concatenate instead of loop
    for door_name in doors_to_close:
        announce('The ' + door_name + ' door is open')


while True:
    process_notifications()
    announce_doors_to_close()
    time.sleep(options.NOTIFICATION_CHECK_FREQUENCY)
