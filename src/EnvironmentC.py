# Import libaries.

import random

# Import Project classes.

from AgentStateC import AgentStateC
from WumpusStateC import WumpusStateC
from PerceptsC import PerceptsC

# class: EnvironmentC

class EnvironmentC:
    
    # Constructor.
    
    def __init__(self, width=4, height=4, allowClimbWithoutGold=True, pitProb=0.2):

        self.active_episode = True
        self.width = width
        self.height = height
        self.allowClimbWithoutGold = allowClimbWithoutGold
        self.pitProb = pitProb

        # Create an occupied_list array.

        occupied_list = []

        # Initialize the Agent and add its location to the occupied list.
    
        self.agent_location = (1, 1)
        self.agentState = AgentStateC(self.agent_location)
        occupied_list.append(self.agent_location)

        # Initialize the location of the Wumpus and add its location to the occupied list.

        self.wumpus_location = self.__get_random_coordinate(occupied_list)
        self.wumpusState = WumpusStateC(self.wumpus_location)
        occupied_list.append(self.wumpus_location)

        # Initialize the location of the Gold and add its location to the occupied list.

        self.gold_location = self.__get_random_coordinate(occupied_list)
        occupied_list.append(self.gold_location)

        # Initialize the location of the pits based on the occupied list.

        self.pit_locations = self.__determine_pit_locations(occupied_list)

    #    print ("The Episode:")
    #    print ("------------")
     #   print ("The Agent is at: \t", self.agent_location)
    #    print ("The Wumpus is at: \t", self.wumpus_location)
     #   print ("The Gold is at: \t", self.gold_location)
    #    print ("The Pit(s) are at: \t", self.pit_locations)


    def get_active_episode(self):

        if ((self.agentState.get_isAlive()) and (self.agentState.get_hasClimbedOut() == False)):
            return True


    def get_Agent_Score(self):

        return self.agentState.get_score()

    def display_initial_episode(self):

        print ("The Episode:")
        print ("------------")
        print ("The Agent is at: \t", self.agent_location)
        print ("The Wumpus is at: \t", self.wumpus_location)
        print ("The Gold is at: \t", self.gold_location)
        print ("The Pit(s) are at: \t", self.pit_locations)
        print ("The Agent is facing: \t", self.agentState.get_orientation())
        # Display the initial episode board.

        self.display_board()



#  Add this later once successful climb        return self.active_episode

    def display_board(self, pre_action_percepts=None, post_action_percepts=None):

        if (pre_action_percepts != None):
            print ("Pre-Action Percepts:\t", end='')
            pre_action_percepts.print()

        if (post_action_percepts != None):
            print ("Post-Action Percepts:\t", end='')
            post_action_percepts.print()

        print ("The agent score is: ", self.agentState.get_score())

        print ("\n\t     ", end='')

        # Draw the x grid numbers.

        for x in range(1, self.width+1):
            print ('.', x, '.  ', end='')

        print ("\n")

        # Get the orientation of the Agent.

        agent_orientation = self.agentState.get_orientation()
        agent_x = self.agent_location[0]
        agent_y = self.agent_location[1]

       # print ("Orientation: ", agent_orientation, (agent_x, agent_y-1))

        # Draw the y grid starting from height.

        for y in range(self.height, 0, -1):
            
            # Deal with the northern layer.
            
            print ("\t     ", end='')

            for z in range(1, self.width+1):
               
               # for zz in range(1, 3):

                    if ((z, y) == (agent_x, agent_y)) and (agent_orientation == "north"):
                        print ('--^--  ', end='')
                    else:
                        print ('-----  ', end='')

            print ("\n")

            # Tab over for more readability.

            print ("\t", y, "  ", end='')



            # Draw the x grid starting from 1.

            for x in range(1, self.width+1):

             #           1  2  3  4 
             #       4

             #       3         A               A = (3, 3)     East  (4, 3)
             #                                                West  (2, 3)
             #       2                                        North (3, 4)
             #                                                South (3, 2)
             #       1  

                if ((x, y) == self.agent_location) and (agent_orientation == "west"):
                    print ('<.A..', ' ', end='')
                elif ((x, y) == self.agent_location) and (agent_orientation == "east"):
                    print ('..A.>', ' ', end='')
                elif ((x, y) == self.agent_location):
                    print ('..A..', ' ', end='')

               # elif ((x, y) == (agent_x-1, agent_y)) and (agent_orientation == "west"):
              #      print ('<', ' ', end='')
             #   elif ((x, y) == (agent_x+1, agent_y)) and (agent_orientation == "east"):
             #       print ('>', ' ', end='')

                elif ((x, y) == self.wumpus_location):

                    if (self.wumpusState.get_isAlive()):
                        print ('..W..', ' ', end='')
                    else:
                        print ('..w..', ' ', end='')

                elif ((x, y) == self.gold_location):
                    print ('..G..', ' ', end='')
                elif ((x, y) in self.pit_locations):
                    print ('..P..', ' ', end='')
                else:
                    print ('.....', ' ', end='')

            print ("\n")

            # Deal with the southern orientation layer.
             
            print ("\t     ", end='')
          
            for z in range(1, self.width+1):

              #  for zz in range(1, 3):

                    if ((z, y) == (agent_x, agent_y)) and (agent_orientation == "south"):
                        print ('--V--  ', end='')
                    else:
                        print ('-----  ', end='')



            print("\n\n")

      #  print ("\n--------------------<<\n")


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

        # An action has been taken.  Regardless of the outcome, update 
        # the score by -1.

        self.agentState.update_score(-1)

        if (next_move == "Forward"):
            my_actionPercepts = self.__forward_action()
        elif (next_move == "TurnLeft"):
            self.agentState.turnLeft()
        elif (next_move == "TurnRight"):
            self.agentState.turnRight()
        elif (next_move == "Shoot"):
            my_actionPercepts = self.__shoot_action()
        elif (next_move == "Grab"):
            self.__grab_action()
        elif (next_move == "Climb"):
            self.__climb_action()

        return my_actionPercepts


    # Private methods


    # __get_random_coordinate

    def __get_random_coordinate(self, occupied_list):

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


    # __determine_pit_locations

    def __determine_pit_locations(self, occupied_list):

        pit_list = []
        pit_or_nopit = [ 'P', '-' ]
        pit_probabilities = [self.pitProb, (1 - self.pitProb)]

        for i in range(1, self.height+1):

            for j in range(1, self.width+1):

                if ((i, j) not in occupied_list):

                    pit = random.choices(pit_or_nopit, weights=pit_probabilities, k=1)[0]

                    if (pit == 'P'):
                        pit_list.append((i, j))

        return pit_list


    # __forward_action

    def __forward_action(self):
        my_actionPercepts = PerceptsC()

        candidate_move_loc = self.agentState.forward()

        candidate_loc_col = candidate_move_loc[0]
        candidate_loc_row = candidate_move_loc[1]

        print ("Action Result:\t\t Candidate: (", candidate_loc_col, candidate_loc_row,")" )
        if ((candidate_loc_col < 1) or (candidate_loc_col > 4) or 
            (candidate_loc_row < 1) or (candidate_loc_row > 4)):

            print("Action Result:\t\t INVALID MOVE OUT OF BOUNDS")
            my_actionPercepts.set_bump(True)

        else:

            self.agentState.set_location(candidate_move_loc)
            self.agent_location = candidate_move_loc
            self.__determine_forward_fate()

        return my_actionPercepts


    # __determine_forward_fate

    def __determine_forward_fate(self):

        if (self.agent_location in self.pit_locations):
            print ("Action Result:\t\t AAAAHHHH... FELL INTO A PIT")
            self.agentState.set_isAlive(False)

            # The Agent has fallen into a pit.  Update the score -1000.

            self.agentState.update_score(-1000)


        elif ((self.agent_location == self.wumpus_location) and
              (self.wumpusState.get_isAlive())):
            print ("Action Result:\t\t AAAGGGG.... WUMPUS HAS EATEN THE AGENT")
            self.agentState.set_isAlive(False)

            # The Agent has been eaten by the Wumpus.  Update the score -1000.

            self.agentState.update_score(-1000)


    # __shoot_action

    def __shoot_action(self):

        my_actionPercepts = PerceptsC()

        print ("Action Result:\t\t HAVE ARROW? ", self.agentState.get_hasArrow())
        print ("Action Result:\t\t FACING:     ", self.agentState.get_orientation())
        if (self.agentState.get_hasArrow()):

            # The arrow has been slung.  Update the score -10.

            self.agentState.update_score(-10)

            orientation = self.agentState.get_orientation()
            current_loc = self.agentState.get_location()
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
                    print ("Action Result:\t\t WUMPUS HAS BEEN KILLED")

                    my_actionPercepts.set_scream(True)
                    self.wumpusState.set_isAlive(False)
                    break;
                else:
                    print ("Action Result:\t\t NO WUMPUS THERE")

            self.agentState.set_hasArrow(False)

        return my_actionPercepts


    def __grab_action(self):

        if (self.agent_location == self.gold_location):
            print("Action Result:\t\t GOT THE GOLD!!!!")
            self.agentState.set_hasGold(True)
        else:
            print("Action Result:\t\t NO GOLD HERE!!")


    def __climb_action(self):

        # The Agent can only climb out from the original room.

        if (self.agent_location == (1, 1)):

            # Determine if the Agent has the gold.

            if (self.agentState.get_hasGold()):
                
                # The gold has been grabbed and climbing out.  Update the score +1000.

                self.agentState.update_score(1000)

                print ("Action Result:\t\t Climbing out with the gold :-) !!")
                self.agentState.set_hasClimbedOut(True)

            else:
                # The Agent can only climb out without the gold if the
                # episode permits its.

                if (self.allowClimbWithoutGold):
                    print ("Action Result:\t\t Climbing out without the gold :-( ")
                    self.agentState.set_hasClimbedOut(True)

                else:
                    print ("Action Result:\t\t Agent cannot climb out without the gold")

        else:
            # The Agent is not in the original room.

            print ("Action Result:\t\t CAN'T CLIMB OUT - need to be at (1,1)")


