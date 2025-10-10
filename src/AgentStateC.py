# AgentStateC.py

# Import Project classes.

import Global

from CharacterStateA import CharacterStateA


class AgentStateC(CharacterStateA):


    # Default constructor.

    def __init__(self, location):

        # Call the super class.

        super().__init__(location)

        # Define attributes specific to AgentStateC.

        self.orientation = Global._east
        self.facing = Global._right

        self.hasGold = False
        self.hasArrow = True
        self.hasClimbedOut = False

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

        if Global._display: print ("Action Result:\t\t Currently at (", current_loc_col, current_loc_row, ") facing ", self.orientation)

        if (self.orientation == Global._south):
            current_loc_row = current_loc_row - 1
        elif (self.orientation == Global._north):
            current_loc_row = current_loc_row + 1
        elif (self.orientation == Global._east):
            current_loc_col = current_loc_col + 1
        elif (self.orientation == Global._west):
            current_loc_col = current_loc_col - 1

        if Global._display: print ("Action Result:\t\t Moved ", self.orientation, " and now at (", current_loc_col, current_loc_row, ")")

        return (current_loc_col, current_loc_row)


    # turnLeft

    def turnLeft(self):

        if (self.orientation == Global._south):
            self.orientation = Global._east
        elif (self.orientation == Global._north):
            self.orientation = Global._west
        elif (self.orientation == Global._east):
            self.orientation = Global._north
        elif (self.orientation == Global._west):
            self.orientation = Global._south

        if Global._display: print ("Action Result:\t\t Currently facing ", self.orientation)
        
    
    # turnRight

    def turnRight(self):

        if (self.orientation == Global._south):
            self.orientation = Global._west
        elif (self.orientation == Global._north):
            self.orientation = Global._east
        elif (self.orientation == Global._east):
            self.orientation = Global._south
        elif (self.orientation == Global._west):
            self.orientation = Global._north

        if Global._display: print ("Action Result:\t\t Currently facing ", self.orientation)


    def shoot(self):

        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Shoot!!")

    def grab(self):

        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Grab!!")

    def climb(self):

        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Climb!!")


