# AgentStateC.py

# Import Project classes.

import Global

from CharacterStateA import CharacterStateA


class AgentStateC(CharacterStateA):


    # Default constructor.

    def __init__(self, location):

        # Call the super class to set the location.

        super().__init__(location)

        # Define attributes specific to AgentStateC.

        self.orientation = Global._east
        self.facing = Global._right

        self.hasGold = False
        self.hasArrow = True
        self.hasClimbedOut = False

        # Initialize the score to 0.

        self.score = 0


    # Define Getters and Setters.

    def get_orientation(self) -> str:
        return self.orientation

    def set_orientation(self, orientation):
        self.orientation = orientation

    def get_facing(self) -> str:
        return self.facing

    def set_facing(self, facing):
        self.facing = facing

    def get_hasGold(self) -> bool:
        return self.hasGold

    def set_hasGold(self, hasGold):
        self.hasGold = hasGold

    def get_hasArrow(self) -> bool:
        return self.hasArrow

    def set_hasArrow(self, hasArrow):
        self.hasArrow = hasArrow
    
    def get_hasClimbedOut(self) -> bool:
        return self.hasClimbedOut

    def set_hasClimbedOut(self, hasClimbedOut):
        self.hasClimbedOut = hasClimbedOut

    def get_score(self) -> int:
        return self.score

    def set_score(self, score):
        self.score = score

    def update_score(self, score_value):
        self.score = self.score + score_value


    # forward

    def forward(self) -> ():

        # Only advance the Agent if within the cave boundaries.

        current_loc_col = self.location[0]
        current_loc_row = self.location[1]

        if (self.orientation == Global._south):
            current_loc_row = current_loc_row - 1
        elif (self.orientation == Global._north):
            current_loc_row = current_loc_row + 1
        elif (self.orientation == Global._east):
            current_loc_col = current_loc_col + 1
        elif (self.orientation == Global._west):
            current_loc_col = current_loc_col - 1

        if Global._display: print ("Action Result:\t\tAgent is looking to move", self.orientation, "to", (current_loc_col, current_loc_row))

        return (current_loc_col, current_loc_row)


    # turnLeft

    def turnLeft(self):

        # Update the Agent's orientation based on its current orientation.

        orientation_index = Global._orientation_array.index(self.orientation)
        self.orientation = Global._orientation_array[orientation_index-1]

        if Global._display: print ("Action Result:\t\tAgent has turned left and is now facing", self.orientation)
        
    
    # turnRight

    def turnRight(self):

        # Update the Agent's orientation based on its current orientation.

        orientation_index = Global._orientation_array.index(self.orientation)
        right_index = orientation_index + 1

        # Unlike the turnRight method, an index larger than the array is an out
        # of bounds error.  Check for this condition (len will be the index of the
        # out of bounds as array starts at 0).

        if (right_index == len(Global._orientation_array)):
            right_index = 0

        self.orientation = Global._orientation_array[right_index]

        if Global._display: print ("Action Result:\t\tAgent has turned right and is now facing", self.orientation)

