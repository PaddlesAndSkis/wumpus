# Import libaries.

import random

# Import Project classes.

from AgentStateC import AgentStateC
from WumpusStateC import WumpusStateC

# class: EnvironmentC

class EnvironmentC:
    
    # Constructor.
    
    def __init__(self, width=4, height=4, allowClimbWithoutGold=False, pitProb=0.2):

        self.active_episode = True
        self.width = width
        self.height = height
        self.allowClimbWithoutGold = allowClimbWithoutGold
        self.pitProb = pitProb

        self.coordinates =  [['-' for x in range(1, self.width)] for y in range(1, self.height)] 

        # Create an occupied_list array.

        occupied_list = []

        # Initialize the Agent and add its location to the occupied list.
    
        self.agent_location = (1, 1)
        self.agentState = AgentStateC(self.agent_location)
        occupied_list.append(self.agent_location)

        # Initialize the location of the Wumpus and add its location to the occupied list.

        self.wumpus_location = self.get_random_coordinate(occupied_list)
        self.wumpusState = WumpusStateC(self.wumpus_location)
        occupied_list.append(self.wumpus_location)

        # Initialize the location of the Gold and add its location to the occupied list.

        self.gold_location = self.get_random_coordinate(occupied_list)
        occupied_list.append(self.gold_location)

        # Initialize the location of the pits based on the occupied list.

        self.pit_locations = self.determine_pit_locations(occupied_list)

        print (self.coordinates)

        print ("Agent", self.agent_location)
        print ("Wumpus", self.wumpus_location)
        print ("Gold", self.gold_location)
        print ("Pit", self.pit_locations)


    def get_active_episode(self):

        if (self.agentState.get_isAlive()):
            return True

#  Add this later once successful climb        return self.active_episode

    def display_board(self):

        print("displaying board")

        for i in range(1, self.height+1):

            for j in range(1, self.width+1):

                if ((i, j) == self.agent_location):
                    print ('A', ' ', end='')
                elif ((i, j) == self.wumpus_location):

                    if (self.wumpusState.get_isAlive()):
                        print ('W', ' ', end='')
                    else:
                        print ('w', ' ', end='')
                elif ((i, j) == self.gold_location):
                    print ('G', ' ', end='')
                elif ((i, j) in self.pit_locations):
                    print ('P', ' ', end='')
                else:
                    print ('-', ' ', end='')

            print()

    def action_next_move(self, next_move):

        if (next_move == "Forward"):
            self.agentState.forward()
            self.agent_location = self.agentState.get_agent_loc()

            self.determine_forward_fate()

        elif (next_move == "TurnLeft"):
            self.agentState.turnLeft()
        elif (next_move == "TurnRight"):
            self.agentState.turnRight()
        elif (next_move == "Shoot"):
            self.shoot_action()
        elif (next_move == "Grab"):
            self.grab_action()
        elif (next_move == "Climb"):
            self.agentState.climb()




    # get_random_coordinate

    def get_random_coordinate(self, occupied_list):

        # Get a random coordinate.  Keep trying until the random coordinate
        # is available.

        attempts = 0

        while (attempts != 16):
            random_row = random.randint(1, 4)
            random_col = random.randint(1, 4)

            if ((random_col, random_row) not in occupied_list):
                break

            attempts = attempts + 1

        # Check to see if all points on the board are occupied.

        if (attempts == 16):
            random_col, random_row = 0

        return (random_col, random_row)


    # determine_pit_locations

    def determine_pit_locations(self, occupied_list):

        pit_list = []
        pit_or_nopit = [ 'P', '-' ]
        pit_probabilities = [self.pitProb, (1 - self.pitProb)]
        #pit_probabilities = [0.2, 0.8]

        for i in range(1, self.height+1):

            for j in range(1, self.width+1):

                if ((i, j) not in occupied_list):

                    pit = random.choices(pit_or_nopit, weights=pit_probabilities, k=1)[0]

                    if (pit == 'P'):
                        pit_list.append((i, j))
    #                    print('Pit', pit)

        return pit_list

    def determine_forward_fate(self):

        if (self.agent_location in self.pit_locations):
            print ("AAAAHHHH... FELL INTO A PIT")
            self.agentState.set_isAlive(False)

        elif (self.agent_location == self.wumpus_location):
            print ("AAAGGGG.... WUMPUS HAS EATEN THE AGENT")
            self.agentState.set_isAlive(False)


    def grab_action(self):

        if (self.agent_location == self.gold_location):
            print("GOT THE GOLD!!!!")
            self.agentState.set_hasGold(True)
        else:
            print("NO GOLD HERE!!")


    def shoot_action(self):

        print ("HAVE ARROW? ", self.agentState.get_hasArrow())
        if (self.agentState.get_hasArrow()):

            orientation = self.agentState.get_orientation()
            current_loc = self.agentState.get_agent_loc()
            current_loc_col = current_loc[0]
            current_loc_row = current_loc[1]

            if (orientation == "south"):
                current_loc_col = current_loc_col + 1
            elif (orientation == "north"):
                current_loc_col = current_loc_col - 1
            elif (orientation == "east"):
                current_loc_row = current_loc_row + 1
            elif (orientation == "west"):
                current_loc_row = current_loc_row - 1
    
            shoot_location = (current_loc_col, current_loc_row)

            if (shoot_location == self.wumpus_location):
                print ("WUMPUS HAS BEEN KILLED")

                self.wumpusState.set_isAlive(False)
            else:
                print ("NO WUMPUS THERE")

            self.agentState.set_hasArrow(False)
