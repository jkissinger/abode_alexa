from enum import Enum

DOOR_STATE = {}

class State(Enum):
    CLOSED=0
    OPEN=1


def update_door_state(door_name, state):
    if door_name in DOOR_STATE:
        print("updating '" + door_name + "' from " + DOOR_STATE[door_name] + " to " + state)
        DOOR_STATE[door_name] = state
    else:
        DOOR_STATE[door_name] = state
        print("created '" + door_name + "' as " + state)