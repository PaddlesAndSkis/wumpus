

class AgentStateC():

    orientation_array = [ "north", "south", "east", "west"]
    facing_array = [ "left", "right"]

    # Default constructor.

    def __init__(self, location):

        # General.

        self.location = location
        self.orientation = "east"
        self.facing = "right"

        self.hasGold = False
        self.hasArrow = True
        self.isAlive = True


    # Define Getters and Setters.

    def get_agent_loc(self):
        return self.location

    def set_agent_loc(self, location):
        self.location = location

    def get_orientation(self):
        return self.orientation

    def set_orientation(self, orientation):
        self.orientation = orientation

    def get_facing(self):
        return self.facing

    def set_facing(self, facing):
        self.facing = facing

    def get_hasGold(self):
        return self.hasGold

    def set_hasGold(self, hasGold):
        self.hasGold = hasGold

    def get_hasArrow(self):
        return self.hasArrow

    def set_hasArrow(self, hasArrow):
        self.hasArrow = hasArrow
    
    def get_isAlive(self):
        return self.isAlive

    def set_isAlive(self, isAlive):
        self.isAlive = isAlive

    def forward(self):

        current_loc_col = self.location[0]
        current_loc_row = self.location[1]

        print ("Currently at (", current_loc_col, current_loc_row, ") facing ", self.orientation)

        if (self.orientation == "south"):
            current_loc_col = current_loc_col + 1
        elif (self.orientation == "north"):
            current_loc_col = current_loc_col - 1
        elif (self.orientation == "east"):
            current_loc_row = current_loc_row + 1
        elif (self.orientation == "west"):
            current_loc_row = current_loc_row - 1

        self.location = (current_loc_col, current_loc_row) 


    def turnLeft(self):

        if (self.orientation == "south"):
            self.orientation = "east"
        elif (self.orientation == "north"):
            self.orientation = "west"
        elif (self.orientation == "east"):
            self.orientation = "north"
        elif (self.orientation == "west"):
            self.orientation = "south"


    def turnRight(self):

        if (self.orientation == "south"):
            self.orientation = "west"
        elif (self.orientation == "north"):
            self.orientation = "east"
        elif (self.orientation == "east"):
            self.orientation = "south"
        elif (self.orientation == "west"):
            self.orientation = "north"


    def shoot(self):

        print ("Shoot!!")

    def grab(self):

        print ("Grab!!")

    def climb(self):

        print ("Climb!!")


