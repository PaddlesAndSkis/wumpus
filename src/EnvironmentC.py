# Import libaries.

import random

# Import Project classes.

from AgentStateC import AgentStateC
from WumpusStateC import WumpusStateC
from PerceptsC import PerceptsC

# class: EnvironmentC

class EnvironmentC:
    
    # Constructor.
    
    def __init__(self, width=4, height=4, allowClimbWithoutGold=False, pitProb=0.2):

        self.active_episode = True
        self.width = width
        self.height = height
        self.allowClimbWithoutGold = allowClimbWithoutGold
        self.pitProb = pitProb

        self.coordinates =  [['.' for x in range(1, self.width)] for y in range(1, self.height)] 

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

        if ((self.agentState.get_isAlive()) and (self.agentState.get_hasClimbedOut() == False)):
            return True

#  Add this later once successful climb        return self.active_episode

    def display_board(self):

        print("displaying board")

        for y in range(self.height, 0, -1):

            for x in range(1, self.width+1):

                if ((x, y) == self.agent_location):
                    print ('A', ' ', end='')
                elif ((x, y) == self.wumpus_location):

                    if (self.wumpusState.get_isAlive()):
                        print ('W', ' ', end='')
                    else:
                        print ('w', ' ', end='')
                elif ((x, y) == self.gold_location):
                    print ('G', ' ', end='')
                elif ((x, y) in self.pit_locations):
                    print ('P', ' ', end='')
                else:
                    print ('.', ' ', end='')

            print()


    def get_percepts(self):

        agent_percepts = PerceptsC()

        # Pits.  If the Agent is adjacent to a pit send a breeze percept.

        for loc in self.pit_locations:

            pit_adjacent_rooms = []

            curr_loc_col = loc[0]
            curr_loc_row = loc[1]

            pit_adjacent_rooms.append((curr_loc_col, curr_loc_row+1)) # north
            pit_adjacent_rooms.append((curr_loc_col, curr_loc_row-1)) # south
            pit_adjacent_rooms.append((curr_loc_col+1, curr_loc_row)) # east
            pit_adjacent_rooms.append((curr_loc_col-1, curr_loc_row)) # west

            if self.agent_location in pit_adjacent_rooms:
                agent_percepts.set_breeze(True)
                break


        # Wampus.  If the Agent is adjacent to the Wumpus or is on top of a dead
        # Wampus, send a stench percept.

        wampus_adjacent_rooms = []

        wampus_col = self.wumpus_location[0]
        wampus_row = self.wumpus_location[1]

        wampus_adjacent_rooms.append((wampus_col, wampus_row+1)) # north
        wampus_adjacent_rooms.append((wampus_col, wampus_row-1)) # south
        wampus_adjacent_rooms.append((wampus_col+1, wampus_row)) # east
        wampus_adjacent_rooms.append((wampus_col-1, wampus_row)) # west

        if self.agent_location in wampus_adjacent_rooms:
            agent_percepts.set_stench(True)

        # Gold.  If the Agent is in the same room as the gold
        # send a glitter percept.

        if (self.agent_location == self.gold_location):
            agent_percepts.set_glitter(True)

        return agent_percepts



    def action_next_move(self, next_move):

        my_actionPercepts = PerceptsC()

        if (next_move == "Forward"):
            my_actionPercepts = self.forward_action()
        elif (next_move == "TurnLeft"):
            self.agentState.turnLeft()
        elif (next_move == "TurnRight"):
            self.agentState.turnRight()
        elif (next_move == "Shoot"):
            my_actionPercepts = self.shoot_action()
        elif (next_move == "Grab"):
            self.grab_action()
        elif (next_move == "Climb"):
            self.climb_action()

        return my_actionPercepts


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

    def forward_action(self):
        my_actionPercepts = PerceptsC()

        candidate_move_loc = self.agentState.forward()

        #print(self.coordinates.shape)

        candidate_loc_col = candidate_move_loc[0]
        candidate_loc_row = candidate_move_loc[1]

        print ("Candidate: (", candidate_loc_col, candidate_loc_row,")" )
        if ((candidate_loc_col < 1) or (candidate_loc_col > 4) or 
            (candidate_loc_row < 1) or (candidate_loc_row > 4)):

            print("INVALID MOVE OUT OF BOUNDS")
            my_actionPercepts.set_bump(True)

        else:

            self.agentState.set_agent_loc(candidate_move_loc)
            self.agent_location = candidate_move_loc
            self.determine_forward_fate()

        return my_actionPercepts



    def determine_forward_fate(self):

        if (self.agent_location in self.pit_locations):
            print ("AAAAHHHH... FELL INTO A PIT")
            self.agentState.set_isAlive(False)

        elif ((self.agent_location == self.wumpus_location) and
              (self.wumpusState.get_isAlive())):
            print ("AAAGGGG.... WUMPUS HAS EATEN THE AGENT")
            self.agentState.set_isAlive(False)


    def grab_action(self):

        if (self.agent_location == self.gold_location):
            print("GOT THE GOLD!!!!")
            self.agentState.set_hasGold(True)
        else:
            print("NO GOLD HERE!!")


    def climb_action(self):

        if (self.agent_location == (1, 1)):
            print ("Climbing out!!")
            self.agentState.set_hasClimbedOut(True)
        else:
            print ("CAN'T CLIMB OUT - need to be at (1,1)")


    def shoot_action(self):

        my_actionPercepts = PerceptsC()

        print ("HAVE ARROW? ", self.agentState.get_hasArrow())
        print ("FACING:     ", self.agentState.get_orientation())
        if (self.agentState.get_hasArrow()):

            orientation = self.agentState.get_orientation()
            current_loc = self.agentState.get_agent_loc()
            current_loc_col = current_loc[0]
            current_loc_row = current_loc[1]

            shoot_path_rooms = []

            if (orientation == "south"):
                for i in range(current_loc_row-1, 0, -1):
                    shoot_path_rooms.append((current_loc_col, i))
            elif (orientation == "north"):
                for i in range(current_loc_row+1, 4+1):
                    shoot_path_rooms.append((current_loc_col, i))
            elif (orientation == "east"):
                for i in range(current_loc_col+1, 4+1):
                    shoot_path_rooms.append((i, current_loc_row))
            elif (orientation == "west"):
                for i in range(current_loc_col-1, 0, -1):
                    shoot_path_rooms.append((i, current_loc_row))
                    
            for shoot_location in shoot_path_rooms:

#            shoot_location = (current_loc_col, current_loc_row)
                print ("Shoot Room", shoot_location)
                if (shoot_location == self.wumpus_location):
                    print ("WUMPUS HAS BEEN KILLED")

                    my_actionPercepts.set_scream(True)
                    self.wumpusState.set_isAlive(False)
                    break;
                else:
                    print ("NO WUMPUS THERE")

            self.agentState.set_hasArrow(False)

        return my_actionPercepts
