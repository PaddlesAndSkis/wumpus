# Global.py

# Global variables.

_display = True
_debug   = False

# Start room.

_start_room = (1, 1)

# Probabilities.

_pit_probability = 0.2

# Directions

_east  = "east"
_west  = "west"
_north = "north"
_south = "south"

_left  = "left"
_right = "right"

_orientation_array = [ _north, _east, _south, _west]
_facing_array      = [ _left, _right]

# Actions

_forward_action   = "Forward"
_turnLeft_action  = "TurnLeft"
_turnRight_action = "TurnRight"
_shoot_action     = "Shoot"
_grab_action      = "Grab"
_climb_action     = "Climb"

# Define the set of actions an Agent can take.

_action_array = [ _forward_action, _turnLeft_action, _turnRight_action, _shoot_action, _grab_action, _climb_action ]

