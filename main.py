import io
import json
import requests

import gmail_checker
import options

settings = {}

with io.open('settings.json', "r", encoding="utf-8") as json_file:
    settings = json.load(json_file)

def announce_door_open(door_name):
    announcement = 'The ' + door_name + ' door is open'
    announcement = announcement.replace(' ', '%20')
    if options.ANNOUNCEMENTS_ENABLED:
        response = requests.get(settings['announcement_url']+announcement)
        print(response)
    else:
        print("Would be announcing: " + announcement)

gmail_checker.main()
