import io
import json
import time
import os

import requests

import door_state
import gmail_checker
import options

settings = {}

with io.open(os.environ.get('ABODE_ALEXA_SETTINGS'), "r", encoding="utf-8") as json_file:
    settings = json.load(json_file)


def announce(announcement):
    if options.ANNOUNCEMENTS_ENABLED:
        response = requests.get(settings['announcement_url'] + announcement.replace(' ', '%20'))
        if not response.ok:
            print(response)
    else:
        print("Would be announcing: " + announcement)


def process_notifications():
    notifications = gmail_checker.check_notifications()
    for notification in notifications:
        # TODO switch to logging to a file
        print("Processing: " + notification)
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
