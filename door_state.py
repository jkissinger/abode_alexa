import logging
from datetime import datetime
from enum import Enum

import options

DOOR_STATE = {}


class State(Enum):
    CLOSED = 0
    OPEN = 1
    UNKNOWN = 2

class StateTime:
    def __init__(self, state, timestamp):
        self.state = state
        self.timestamp = timestamp
        self.last_warning_timestamp = timestamp


def update_door_state(door_name, string_state):
    state=State.UNKNOWN
    if string_state=='Opened':
        state=State.OPEN
    elif string_state == 'Closed':
        state = State.CLOSED

    if door_name in DOOR_STATE:
        logging.info("updating '" + door_name + "' from " + str(DOOR_STATE[door_name].state) + " to " + str(state))
    else:
        logging.info("created '" + door_name + "' as " + str(state))
    DOOR_STATE[door_name] = StateTime(state, datetime.now())


def validate_door_states():
    # return a list of doors that have been open too long
    open_doors = []
    for name, door in DOOR_STATE.items():
        if door.state == State.OPEN:
            difference = (datetime.now() - door.timestamp)
            seconds_door_was_open = difference.total_seconds()
            if seconds_door_was_open >= options.INITIAL_WARNING_THRESHOLD:
                difference = (datetime.now() - door.last_warning_timestamp)
                seconds_since_last_warning = difference.total_seconds()
                if seconds_since_last_warning >= options.NEXT_WARNING_THRESHOLD:
                    open_doors.append(name)
                    door.last_warning_timestamp = datetime.now()
    if open_doors:
        logging.info("Found these doors to be open too long: " + str(open_doors))
    return open_doors
