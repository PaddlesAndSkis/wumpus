# ProbAgentC

# Import libraries.

import random
import networkx as nx
import math
import torch
from torch._prims_common import Tensor
from pomegranate.distributions import Categorical
from pomegranate.distributions import ConditionalCategorical
from pomegranate.bayesian_network import BayesianNetwork
import numpy

# Import Project classes.

import Global
from MovePlanningAgentC import MovePlanningAgentC
from PredicateC import PredicateC
 

class ProbAgentC(MovePlanningAgentC):

    # Constructor

    def __init__(self, location):

        # Invoke the super class.

        super().__init__(location)
        
        # Initialize the variables.

        self.has_arrow = True
        self.move_plan = []
        self.path_taken = []
        self.rooms_dict = {}

        # Build the model.

        self.build_model()



    # percept

    def percept(self, percepts):

        # For the Move Planning Agent, it will use the Percepts for grabbing the gold and
        # climbing out of the cave.  As it also uses the Percepts for detecting a Bump when
        # trying to go out of bounds, it will also use the Percepts to detect that a valid
        # move has been made.

        # Call the super class to register the percepts.

        super().percept(percepts)

        new_location = self.percepts.get_move()
        direction    = self.percepts.get_direction()

        # Determine if a scream has been heard from the wumpus.

        if (self.percepts.get_scream()):

            # A scream has been heard.

            if Global._display: print ("Status:\t\t\t*** Agent has detected the Scream from a dead Wumpus.  Setting Wumpus probability to 0..")

            # Iterate over rooms.

            for room_key in self.rooms_dict.keys():

                # As the Wumpus is dead, the probability of dying from the Wumpus is now 0.
                # Update the Wumpus predicates and Wumpus list.

                new_prob = 0
                wumpus_categorical = PredicateC(new_prob).toCategorical()
                self.wumpus_predicate_list[room_key] = wumpus_categorical
                self.wumpus_list[room_key] = 0

        # Determine if a move has been made.

        if (len(new_location) != 0):

            # A move has been made, add the new node to the graph.
                    
            if Global._display: print ("Action Result:\t\tLooking to add", new_location, "facing", direction, "(and other directions) to the visited room graph.")

            self._add_node_to_graph(self.location, new_location, direction)
            
            # Update the Agent's location and direction.

            self.location  = new_location
            self.direction = direction

            # The graph node is in the form (1, 1).  Convert it into a dictionary lookup value "1-1".

            current_room = str(self.location[0]) + "-" + str(self.location[1])

            # If the Agent got to this point, the Agent is still alive so this room is neither a pit
            # or the location of the Wumpus.

            self.pit_list[current_room] = 0
            self.wumpus_list[current_room] = 0

            # As the Wumpus has an original 1/15 probability of being in a room, if this room
            # does not have the Wumpus then the probability of the other rooms having the Wumpus
            # increases.

            # Count how many rooms already have been determined to not contain the Wumpus.

            wumpus_free_room_count = 0

            for wumpus_room in self.wumpus_list.keys():

                # If the room was already Wumpus-free, add it to the count.

                if (self.wumpus_list[wumpus_room] == 0):

                    wumpus_free_room_count = wumpus_free_room_count + 1

            # Calculate the new probability for the Wumpus.

            new_wumpus_prob = 1/(15 - wumpus_free_room_count) if wumpus_free_room_count < 15 else 0
            if Global._display: print ("Status:\t\t\t*** Agent has calculated the new Wumpus probability for each unknown room as", new_wumpus_prob)

            # Iterate over the rooms and update the Wumpus predicate and probability info.

            for room_key in self.rooms_dict.keys():

                # Update the Wumpus room probability if the room is 'unknown'.  The other rooms
                # would already have a 0 (e.g., 1-1).

                if (self.wumpus_list[room_key] == -1):

                    # Set the new probability.

                    wumpus_categorical = PredicateC(new_wumpus_prob).toCategorical()
                    self.wumpus_predicate_list[room_key] = wumpus_categorical


            # Finally, add this room to the path taken.

            self.path_taken.append(current_room)


    # action

    def action(self) -> str:
 
        action = None

        # The Agent is either exploring, looking for the Gold or the Agent has
        # found it and is executing on its exit plan.

        # Determine if the Agent is exploring or executing its exit plan.

        if (len(self.exit_plan) > 0):

            # The Agent is executing its exit plan.  Therefore, get the next
            # action in the plan.

            if Global._display: print ("Status:\t\t\t*** Agent is currently executing its exit plan...")

            if Global._display: print ("Exit plan:\t\t\t", self.exit_plan)

            # Get the next action to take.

            action = self.exit_plan[0]

            if Global._display: print ("Action from Exit plan:\t\t", action)

            # Remove the action from the exit plan.

            self.exit_plan.pop(0)

            if Global._display: print ("Exit plan after action:\t\t", self.exit_plan)


        elif (len(self.move_plan) > 0):

            # The Agent is executing its move plan.  Therefore, get the next
            # action in the plan.

            if Global._display: print ("Status:\t\t\t*** Agent is currently in a movement plan...")

            if Global._display: print ("Move plan:\t\t\t", self.move_plan)

            # Get the next action to take.

            action = self.move_plan[0]

            if Global._display: print ("Action from Move plan:\t\t", action)

            # Remove the action from the exit plan.

            self.move_plan.pop(0)

            if Global._display: print ("Move plan after action:\t\t", self.move_plan)

        
        else:

            # For the Move Planning Agent, use its sensors to read the percepts to see if the gold 
            # is in the current room or if they can climb out the cave with the gold.

            if Global._display: print ("Status:\t\t\t*** Agent is currently exploring looking for Gold...")

            if (self.percepts.get_glitter()) and (self.has_gold == False):

                if Global._display: print ("Status:\t\t\t*** Agent has detected the Gold and will now grab it...")
    
                # Glitter has been sensed.  Action the Grab.

                action = Global._grab_action

                # Update the Agent's gold attribute.

                self.has_gold = True

                # Create the Exit plan that will be actioned the next time the Agent needs
                # to action.

                self.exit_plan = self._create_exit_plan(self.location, (1, 1), self.direction)

            elif (self.location == Global._start_room) and (self.has_gold == True):

                # The climb action is handled via the Agent's exit plan and the environment.

                action = Global._climb_action

            elif ((self.percepts.get_stench()) and (self.has_arrow == True)):

                # Stench has been detected and we have the arrow.  May as well give it a shot.

                action = Global._shoot_action
                self.has_arrow = False

            else:
      
                # Move Action.  First, identify the Agent location and direction.

                # The graph node is in the form (1, 1).  Convert it into a dictionary lookup value "1-1".

                current_room = str(self.location[0]) + "-" + str(self.location[1])

                # Breeze

                self.breeze_list[current_room] = 1 if (self.percepts.get_breeze()) else 0

                # Stench

                self.stench_list[current_room] = 1 if (self.percepts.get_stench()) else 0

                # Get the possible move options based on the possibility that the next room is a pit or the Wumpus.

                pit_move_options = self.get_move_options(current_room)
                wumpus_move_options = self._get_move_options_to_avoid_wumpus(current_room)

                best_room_option = self.choose_best_move_option(current_room, pit_move_options, wumpus_move_options, self.direction)
             
                if Global._display: print ("Status:\t\t\t*** The best room for the Agent to move to is", best_room_option)

                # If the best room option is Exit, the Agent has determined that it is too dangerous to move as the
                # probability of dying is > 50 %.  Exit out of the cave.

                if (best_room_option == 'Exit'):

                    if Global._display: print ("Status:\t\t\t*** Next moves are too dangerous.  Agent is bailing.", self.move_plan)

                    # Do one final grab just in case!

                    action = Global._grab_action

                    # Create the Exit plan that will be actioned the next time the Agent needs
                    # to action.

                    self.exit_plan = self._create_exit_plan(self.location, (1, 1), self.direction)
                
                else:

                    # Get the move plan and execute it.  The move plan will be something like ["TurnLeft", "Forward"].

                    self.move_plan = self.get_move_plan(current_room, best_room_option, self.direction)

                    if Global._display: print ("Status:\t\t\t*** The Agent's move plan is", self.move_plan)

                    # Get the first action to take.

                    action = self.move_plan.pop(0)


        # Return the selected action.

        return action


    # build_model

    def build_model(self):

        # Build the neighbours model.

        # Iterate over the x-grid.

        for i in range (1,5):

            # Iterate over the y-grid.

            for j in range (1,5):

                # Identify the current room's neighboours and add them to the set.

                neighbours = []

                if ((i-1) > 0):
                    west_neighbour = str(i-1) + "-" + str(j)
                    neighbours.append(west_neighbour)

                if ((i+1) < 5):
                    east_neighbour = str(i+1) + "-" + str(j)
                    neighbours.append(east_neighbour)

                if ((j+1) < 5):
                    north_neighbour = str(i) + "-" + str(j+1)
                    neighbours.append(north_neighbour)

                if ((j-1) > 0):
                    south_neighbour = str(i) + "-" + str(j-1)
                    neighbours.append(south_neighbour)

                if Global._display: print ("Status:\t\t\t*** The Agent's neighbours at (", i, ",", j, ") -> ", neighbours)

                # Construct the room key and add it and the neighbours to the room dictionary.

                my_key = str(i) + "-" + str(j)

                self.rooms_dict[my_key] = neighbours

        # Print the rooms dictionary.

        if Global._display: print ("Status:\t\t\t*** The Agent's room dictionary is:", self.rooms_dict)

        # Now that the set of rooms and each room's neighbours has been constructed, set all
        # rooms to be the standard 20% probability that the room could be a pit (before any
        # evidence is gathered).

        self.pit_predicate_list = {}
        pit_categorical = PredicateC(0.2).toCategorical()
        
        # All of the rooms, except for 1-1, can be a pit.  Therefore, create a pit list of all
        # the rooms and set them to be -1 (unknown).  These will be updated as the Agent gathers
        # more information about the cave and which rooms are safe.

        self.pit_list = {}
        pit_unknown = -1

        # Keep a list of all rooms that have a breeze.

        self.breeze_list = {}
        breeze_unknown = -1

        # Add the Wumpus model. To start, the probability of the Wumpus being in a room is 1/15 (the Wumpus
        # can't be in the start room).  However, as the cave is explored, the probability of the Wumpus being
        # there increases.

        self.wumpus_predicate_list = {}
        wumpus_categorical = PredicateC(1/15).toCategorical() 

        self.wumpus_list = {}
        wumpus_unknown = -1

        # Add the Stench model.

        self.stench_list = {}
        stench_unknown = -1

        # Iterate over the room keys which will include all rooms in the cave.
        # Create the categorical probability for the dictionary
        # Set each room to be unknown for a pit and unknown for a breeze.

        for room_key in self.rooms_dict.keys():

            # Pit and breeze info.  NOTE: don't need separate unknowns for breeze, pit etc. as they are the same.

            self.pit_predicate_list[room_key] = pit_categorical
            self.pit_list[room_key]           = pit_unknown
            self.breeze_list[room_key]        = breeze_unknown

            # Wumpus and stench info.

            self.wumpus_predicate_list[room_key] = wumpus_categorical
            self.wumpus_list[room_key]           = wumpus_unknown
            self.stench_list[room_key]           = stench_unknown


        # Room 1-1 cannot be a pit or wumpus.  Therefore, it will be set to 0 (safe).

        self.pit_list["1-1"] = 0
        self.wumpus_list["1-1"] = 0

        # Finally, add the starting room to the path taken.

        self.path_taken.append("1-1")


    # get_move_plan

    def get_move_plan(self, src_room, dest_room, direction):

        move_plan = []

        # Get the x, y coordinates of the source and destination rooms.

        src_x = src_room[0]
        src_y = src_room[2]

        dest_x = dest_room[0]
        dest_y = dest_room[2]

        # Determine if the destination node is North, East, West or South 
        # from the source node.

        if (dest_x < src_x):
            destination = Global._west

        elif (dest_x > src_x):
            destination = Global._east

        elif (dest_y < src_y):
            destination = Global._south

        elif (dest_y > src_y):
            destination = Global._north

        # Now figure out how to turn to get there.

        if ((direction == Global._east) and (destination == Global._north)):

            # This is the only direction and destination where turning left
            # is better.

            move_plan.append(Global._turnLeft_action)
        else:

            # Might as well turn right.

            while (direction != destination):

                # Continue turning right and updating the direction until it matches the
                # destination.

                direction = self.turn_right(direction)
                move_plan.append(Global._turnRight_action)

        # Add the forward action to the plan.

        move_plan.append(Global._forward_action)

        return move_plan 


    # turn_right
    
    def turn_right(self, direction):

        # By turning right, return the new direction.

        if (direction == Global._north):
            return Global._east
        elif (direction == Global._east):
            return Global._south
        elif (direction == Global._south):
            return Global._west
        elif (direction == Global._west):
            return Global._north


    # choose_best_move_option
            
    def choose_best_move_option(self, current_location, neighbour_prob_dict, wumpus_neighbour_prob_dict, direction):

        # Set the best room variables.

        best_false_value = 0
        best_room_option = ""
        best_room_options = []

        # Iterate over the current room's neighbours.

        for best_room in neighbour_prob_dict.keys():        # pit_neighbour and wumpus_neighbour are the same thing

            # Get the True / False dictionary for this neighbour from the Pit network and extract the False value.
            # The False value is the % that the room does not have a Pit or Wumpus (i.e., it would be
            # True if it contained a pit or wumpus).

            true_false_dict = neighbour_prob_dict[best_room]
            false_value = true_false_dict["False"]

            # Get the True / False dictionary from the Wumpus network.

            wumpus_true_false_dict = wumpus_neighbour_prob_dict[best_room]
            wumpus_false_value = wumpus_true_false_dict["False"]

            if Global._display: print ("Status:\t\t\t*** Evaluating room", best_room, "the % that it is NOT a pit is", false_value)
            if Global._display: print ("Status:\t\t\t*** Evaluating room", best_room, "the % that it is NOT a wumpus is", wumpus_false_value)

            # Calculate the % that the room is a pit or wumpus. 

            not_a_pit_or_wumpus = false_value * wumpus_false_value

            if Global._display: print ("Status:\t\t\t*** Evaluating room", best_room, "the % that it is NOT both is (1-p)(1-w)", not_a_pit_or_wumpus)

            # Sometimes, the % calculation from the Bayesian Network is not a number.  Convert it to 1.

            is_nan = isinstance(not_a_pit_or_wumpus, float) and math.isnan(not_a_pit_or_wumpus)

            if (is_nan):
                not_a_pit_or_wumpus = 1
                if Global._display: print ("Status:\t\t\t*** Converting room:", best_room, ": the % that it is NOT both is (1-p)(1-w)", not_a_pit_or_wumpus)

            # Determine if the new % is greater or equal to the current best False value.

            if (not_a_pit_or_wumpus >= best_false_value):

                # Ensure that the best room is not in the path of rooms visited so that it doesn't go into
                # an endless loop.  Always explore further!

                if (best_room not in (self.path_taken)):

                    # If the combined % > Best False value.
                    # Set the best room options to be just this room.

                    if (not_a_pit_or_wumpus > best_false_value):
                        best_room_options = [best_room] 
                    else:
                        # If the combined % = Best False value.
                        # Add this room to the set of best room options.

                        best_room_options.append(best_room) 

                    # Set the new high watermark.

                    best_false_value = not_a_pit_or_wumpus

        # Check if there is a set of best rooms (e.g., tied with their False values).

        if (len(best_room_options) > 1):

            shortest_path = 100    # Make it large to start!

            # Iterate over the best room options.

            for candidate_option in best_room_options:

                # Calculate the shortest path to get to that room.

                path_len = self.calculate_shortest_path(current_location, candidate_option, direction)

                print ("Path Len from ", current_location, "to", candidate_option, "while facing", direction, "is", path_len)

                # Check to see if this path length is the shortest path between the nodes.

                if (path_len < shortest_path):
                    shortest_path = path_len
                    best_room_option = candidate_option

        else:

            # There is only one best room in the set.  Just set it.

            best_room_option = best_room_options[0]

        
        # Determine if it is best if the Agent just leaves.  If the probability that the room is safe (i.e., False)
        # is lower than 50 %, it is best for the Agent to bail.

        if (best_false_value < .5):

            # Best for the Agent to leave.

            best_room_option = 'Exit'

        # Return the best room option.

        return best_room_option

    
    # calculate_shortest_path

    def calculate_shortest_path(self, source, dest, direction):

        return len(self.get_move_plan(source, dest, direction))


    # create_neighbour_cases_for_room

    def create_neighbour_cases_for_room(self, current_room) -> []:

        # Get the current room's neighbours.

        current_room_neighbours = self.rooms_dict[current_room]
        current_room_neighbours_count = len(current_room_neighbours)

        # Based on the number of neighbours, create the cases.

        if (current_room_neighbours_count == 2):

            current_room_cases = self.create_cases_2()

        elif (current_room_neighbours_count == 3):

            current_room_cases = self.create_cases_3()

        elif (current_room_neighbours_count == 4):

            current_room_cases = self.create_cases_4()

        return current_room_cases


    # _get_move_options_to_avoid_wumpus

    def _get_move_options_to_avoid_wumpus(self, current_room):

        # Get the neighbours for the current room.

        current_room_neighbours = self.rooms_dict[current_room]

        # Build the neighbour cases for the current room.

        current_room_cases = self.create_neighbour_cases_for_room(current_room)

        # Create the conditional categorical object now that we have the cases for the current room's neighbours.
        
        stench_condition_categorical = ConditionalCategorical([current_room_cases])

        # Create the variables (stench room and its adjacent rooms) and the
        # edges (an edge is from an adjacent room to the stench room).

        variable_list        = []
        edge_list            = []
        room_and_stench_list = []

        # Iterate over the current room's neighbours.

        for current_room_neighbour in current_room_neighbours:

            # If the stench has been detected, the Wumpus is in one of the neighbouring rooms.
            # Therefore, update the probability.
              
            if (self.percepts.get_stench()):

                # Update the probability.

                if (self.wumpus_list[current_room_neighbour] != 0):

                    # Calculate the new probability and set it.

                    new_prob = 1/len(current_room_neighbours)
                    wumpus_categorical = PredicateC(new_prob).toCategorical()
                    self.wumpus_predicate_list[current_room_neighbour] = wumpus_categorical
            
            # Create the room predicate.

            current_room_neighbour_predicate = self.wumpus_predicate_list[current_room_neighbour]
            variable_list.append(current_room_neighbour_predicate)

            # Create the edge.

            edge_list.append((current_room_neighbour_predicate, stench_condition_categorical))

            # Add the knowledge of if the neighbour is a wumpus to the tensor.
            # -1 is unknown; 0 is safe; 1 is a pit

            current_room_neighbour_wumpus_knowledge = self.wumpus_list[current_room_neighbour]
            room_and_stench_list.append(current_room_neighbour_wumpus_knowledge)

                
        # If there is a stench, then the Wumpus is in one of the neighbouring rooms.
        # Therefore, set the rest of the locations to 0 (no Wumpus) and the
        # predicates to 0 (no chance of a Wumpus).
        # Note that this only applies to the Wumpus since there is only one.  This can't
        # be applied to the pits as there can be many.
        
        if (self.percepts.get_stench()):

            # Iterate over the Wumpus list.

            for room in self.wumpus_list.keys():

                # Update the knowledge about which room can have the Wumpus.

                if ((self.wumpus_list[room] == -1) and (room not in current_room_neighbours)):

                    no_wumpus_categorical = PredicateC(0).toCategorical()
                    self.wumpus_predicate_list[room] = no_wumpus_categorical
                    self.wumpus_list[room] = 0

        # Now add the predicate for the stench room at the end of the list.
        # Add the stench knowledge - 0 if no stench is detected, 1 if a stench is detected.

        stench_condition_knowledge = self.stench_list[current_room]  

        variable_list.append(stench_condition_categorical)
        room_and_stench_list.append(stench_condition_knowledge)

        if Global._display: print ("Status:\t\t\t*** Evaluating probability for the Wumpus - room and stench list", room_and_stench_list)

        # Run the Pomegranate model to get the neighbour rooms' probabilities.

        neighbour_prob_dict = self.run_model_single(current_room_neighbours, variable_list, edge_list, room_and_stench_list)

        if Global._display: print ("Status:\t\t\t*** Evaluating probability for the Wumpus - neighbour probabilities", neighbour_prob_dict)

        return neighbour_prob_dict


    # get_move_options

    def get_move_options(self, current_room):

        # Get the neighbours for the current room.

        current_room_neighbours = self.rooms_dict[current_room]

        # Build the neighbour cases for the current room.

        current_room_cases = self.create_neighbour_cases_for_room(current_room)

        # Now, setup the breeze room by getting the first room (1-1).
        # This can be done by iterating over the keys.

       # breeze_room =  "1-1" #"2-2" #"1-2"  # "1-1"
        #pit_list["2-2"] = 0             # Remove this, just here to simulate that the Agent is safe

        #current_room_cases = []

        ## Get the breeze room's neighbours.

        #current_room_neighbours = self.rooms_dict[current_room]
        #current_room_neighbours_count = len(current_room_neighbours)

        #print ("The number of neighbours that breeze room", current_room, "has is", current_room_neighbours_count)



     #   pit21 = PredicateC(0.2).toCategorical()

       # pit12 = "1-2"
       # print ("pit12 should be Categorical = ", pit_predicate_list[pit12])

      #  pit_categorical = pit_predicate_list[pit12]
      #  print ("pit12.probs (T) = ", pit_categorical.probs[0][1])

        #if (current_room_neighbours_count == 2):
            
        #    current_room_cases = self.create_cases_2()

        #elif (current_room_neighbours_count == 3):

        #    current_room_cases = self.create_cases_3()

        #elif (current_room_neighbours_count == 4):

        #    current_room_cases = self.create_cases_4()

        #print ("Breeze room cases:", current_room_cases)

        # Create the probability matrix for the breeze room and the predicate.
        # Create the knowledge of the breeze room if it's a pit or not (should be 0 - safe as
        # the Agent would have died otherwise).
         
        breeze_condition_categorical = ConditionalCategorical([current_room_cases])
        breeze_condition_predicate   = self.pit_predicate_list[current_room]     # !!! Remove -This isn't used - breeze useses the categorical value that contains the cases not the predicate value

        stench_condition_categorical = ConditionalCategorical([current_room_cases])

      #  print ("Breeze11 condition categorical:", breeze_condition_categorical)
      #  print ("Breeze11 condition predicate:  ", breeze_condition_predicate)

        # Create the variables (breeze room and its adjacent rooms) and the
        # edges (an edge is from an adjacent room to the breeze room).

        variable_list        = []
        edge_list            = []
        room_and_breeze_list = []

        for current_room_neighbour in current_room_neighbours:

            # Create the room predicate.

            if (self.percepts.get_breeze()):
                new_prob = 1/len(current_room_neighbours)
                print ("BREEzE DETECTed: THEREFORE UPDATING NEIGHTBOURS PROBS TO", new_prob)
                pit_categorical = PredicateC(new_prob).toCategorical()
                self.pit_predicate_list[current_room_neighbour] = pit_categorical

            current_room_neighbour_predicate = self.pit_predicate_list[current_room_neighbour]
            variable_list.append(current_room_neighbour_predicate)

            # Create the edge.

            edge_list.append((current_room_neighbour_predicate, breeze_condition_categorical))

            # Add the knowledge of if the neighbour is a pit to the tensor.
            # -1 is unknown; 0 is safe; 1 is a pit

            current_room_neighbour_pit_knowledge = self.pit_list[current_room_neighbour]
            room_and_breeze_list.append(current_room_neighbour_pit_knowledge)

        # Now add the predicate for the breeze room at the end of the list.
        # Add the breeze knowledge - 0 if no breeze is detected, 1 if a breeze is detected.

        breeze_condition_knowledge = self.breeze_list[current_room]  #1 # breeze is detected

        variable_list.append(breeze_condition_categorical)
        room_and_breeze_list.append(breeze_condition_knowledge)

     #   print ("variable_list:", variable_list)
     #   print ("edge list:    ", edge_list)
        print ("room_and_breeze_list:  ", room_and_breeze_list)

        # Run the model.
        neighbour_prob_dict = self.run_model_single(current_room_neighbours, variable_list, edge_list, room_and_breeze_list)

        print ("neighbour_prob_dict:", neighbour_prob_dict)

        return neighbour_prob_dict

       # self.run_model(variable_list, edge_list)
       # self.run_model(variable_list[0], edge_list[0])


    # Just ask one question - I know if I feel a breeze or not; given what I know of my neighbours,
    # which is the best one to go to.

    def run_model_single(self, breeze_room_neighbours, variables, edges, room_and_breeze_list): 

        # Construct the model with the three variables, and two edges

      #  variables = [pit12, pit21, breeze11]
      #  edges = [(pit12, breeze11), (pit21, breeze11)]

        # Check shapes
        print('variables shape', numpy.array(variables).shape)
        print('edges shape', numpy.array(edges).shape)

        pits_model = BayesianNetwork(variables, edges)

        # If no breeze in breeze room and we haven't visited the other two rooms, what is the
        # likelihood that there is a pit in the other rooms?

        #  breeze room is #3 -> 0 no breeze; 1 breeze

        # Just ask one question at a time.

        # Create the tensor based on the neighbours and the breeze room.

        X = torch.tensor([room_and_breeze_list])


        # 2 neighbours
 #       X = torch.tensor([[-1, -1, 0]])# ,  # pit12?, pit21?, breeze11 is false   These should be the only
 
        # 3 neighbours
 #       X = torch.tensor([[-1, -1, -1, 0]])# ,  # pit12?, pit21?, pitxx, breeze11 is false   These should be the only

        # 4 neighbours (example, neighbour1 is a pit, neighbour 2 is a pit, neighbour 3 is not, neighbour 4 is unknown and I don't feel a breeze)
 #       X = torch.tensor([[1, 1, 0, -1, 0]])# ,  # pit12?, pit21?, pitxx, breeze11 is false   These should be the only

                        #  [-1, -1, 1]  # pit12?, pit21?, breeze11 is true          2 we see as we will be able
                #          [-1, -1, -1], # pit12?, pit21?, breeze11?                to detect breezes
                #          [1, -1, -1]   # pit12 is true, pit21?, breeze11?
                         #])

        X_masked = torch.masked.MaskedTensor(X, mask=X >= 0)
        print(X_masked)


        my_tensors = pits_model.predict_proba(X_masked)

        print ("Tensors:", my_tensors)

        # Extract the probabilities for each of the neighbours then the Agent makes its decision
        # based on that which way it goes.


        neighbour_prob_dict = {}
        tensor_idx = 0

        for breeze_room_neighbour in breeze_room_neighbours:
            
            breeze_room_neighbour_tensor = my_tensors[tensor_idx]
            breeze_room_neighbour_tensor_probs_list = breeze_room_neighbour_tensor.tolist()

            print ("Tensor", tensor_idx, "=", breeze_room_neighbour_tensor)
            print ("Tensor", tensor_idx, "=", breeze_room_neighbour_tensor_probs_list)
            print ("Tensor", tensor_idx, "=", breeze_room_neighbour_tensor_probs_list[0][0])

            true_false_dict = {}
            true_false_dict["False"] = breeze_room_neighbour_tensor_probs_list[0][0]
            true_false_dict["True"]  = breeze_room_neighbour_tensor_probs_list[0][1]

            neighbour_prob_dict[breeze_room_neighbour] = true_false_dict

            tensor_idx = tensor_idx + 1

        return neighbour_prob_dict


    # create_cases_2

    def create_cases_2(self):

        grid = []

        for i in [False, True]:
            layer = []
            for j in [False, True]:
                case = i or j      # we can use or between them because we have a breeze if there is a pit in any of the adjacent squares
                if case:
                    p = 1.0
                else:
                    p = 0.0
                layer.append(PredicateC(p).toList())  # row

                print ("layer:", layer)

            grid.append(layer)

        print ("grid:", grid)

        return grid


    def create_cases_3(self):

        grid = []

        for h in [False, True]:

            cube = []
            for i in [False, True]:
                layer = []
                for j in [False, True]:
                    case = i or j      # we can use or between them because we have a breeze if there is a pit in any of the adjacent squares
                    if case:
                        p = 1.0
                    else:
                        p = 0.0
                    layer.append(PredicateC(p).toList())  # row

                    print ("layer:", layer)

                cube.append(layer)
                
            grid.append(cube)

        print ("grid:", grid)

        return grid


    def create_cases_4(self):

        grid = []

        for g in [False, True]:
            structure = [] 

            for h in [False, True]:

                cube = []
                for i in [False, True]:
                    layer = []
                    for j in [False, True]:
                        case = i or j      # we can use or between them because we have a breeze if there is a pit in any of the adjacent squares
                        if case:
                            p = 1.0
                        else:
                            p = 0.0
                        layer.append(PredicateC(p).toList())  # row

                        print ("layer:", layer)

                    cube.append(layer)
                
                structure.append(cube)

            grid.append(structure)

        print ("grid:", grid)

        return grid

    

# BACKUP


    def get_move_options_wumpus(self, current_room):

        # Get the neighbours for the current room.

        current_room_neighbours = self.rooms_dict[current_room]

        # Build the neighbour cases for the current room.

        current_room_cases = self.create_neighbour_cases_for_room(current_room)

        # Now, setup the breeze room by getting the first room (1-1).
        # This can be done by iterating over the keys.

       # breeze_room =  "1-1" #"2-2" #"1-2"  # "1-1"
        #pit_list["2-2"] = 0             # Remove this, just here to simulate that the Agent is safe
  #      current_room_cases = []

        # Get the stench room's neighbours.

        #current_room_neighbours = self.rooms_dict[current_room]
        #current_room_neighbours_count = len(current_room_neighbours)

        #print ("The number of neighbours that stench room", current_room, "has is", current_room_neighbours_count)



     #   pit21 = PredicateC(0.2).toCategorical()

       # pit12 = "1-2"
       # print ("pit12 should be Categorical = ", pit_predicate_list[pit12])

      #  pit_categorical = pit_predicate_list[pit12]
      #  print ("pit12.probs (T) = ", pit_categorical.probs[0][1])

        #if (current_room_neighbours_count == 2):
            
        #    current_room_cases = self.create_cases_2()

        #elif (current_room_neighbours_count == 3):

        #    current_room_cases = self.create_cases_3()

        #elif (current_room_neighbours_count == 4):

        #    current_room_cases = self.create_cases_4()

        #print ("Stench room cases:", current_room_cases)

        # Create the probability matrix for the stench room and the predicate.
        # Create the knowledge of the stench room if it's a wumpus or not (should be 0 - safe as
        # the Agent would have died otherwise).
         
       # breeze_condition_categorical = ConditionalCategorical([current_room_cases])
       # breeze_condition_predicate   = self.pit_predicate_list[current_room]     # !!! Remove -This isn't used - breeze useses the categorical value that contains the cases not the predicate value

        stench_condition_categorical = ConditionalCategorical([current_room_cases])

      #  print ("Breeze11 condition categorical:", breeze_condition_categorical)
      #  print ("Breeze11 condition predicate:  ", breeze_condition_predicate)

        # Create the variables (stench room and its adjacent rooms) and the
        # edges (an edge is from an adjacent room to the stench room).

        variable_list        = []
        edge_list            = []
        room_and_stench_list = []

        for current_room_neighbour in current_room_neighbours:

            # Create the room predicate.

            if (self.percepts.get_stench()):

                if (self.wumpus_list[current_room_neighbour] != 0):
                    new_prob = 1/len(current_room_neighbours)
                    print ("STEnCh DETECTed: THEREFORE UPDATING NEIGHTBOURS PROBS TO", new_prob)
                    wumpus_categorical = PredicateC(new_prob).toCategorical()
                    self.wumpus_predicate_list[current_room_neighbour] = wumpus_categorical
                  #  self.wumpus_list[current_room_neighbour] = 1  # do this if the agent survives

            current_room_neighbour_predicate = self.wumpus_predicate_list[current_room_neighbour]
            variable_list.append(current_room_neighbour_predicate)

            # Create the edge.

            edge_list.append((current_room_neighbour_predicate, stench_condition_categorical))

            # Add the knowledge of if the neighbour is a wumpus to the tensor.
            # -1 is unknown; 0 is safe; 1 is a pit

            current_room_neighbour_wumpus_knowledge = self.wumpus_list[current_room_neighbour]
            room_and_stench_list.append(current_room_neighbour_wumpus_knowledge)

                
        # If there is a stench, then the Wumpus is in one of the neighbours.
        # Therefore, set the rest of the locations to 0 (no Wumpus) and the
        # predicates to 0 (no chance of a Wumpus).
        
        if (self.percepts.get_stench()):

            for room in self.wumpus_list.keys():

                if ((self.wumpus_list[room] == -1) and (room not in current_room_neighbours)):

                    no_wumpus_categorical = PredicateC(0).toCategorical()
                    self.wumpus_predicate_list[room] = no_wumpus_categorical
                    self.wumpus_list[room] = 0

            print ("wumpus_list is now", self.wumpus_list)



        # Now add the predicate for the stench room at the end of the list.
        # Add the stench knowledge - 0 if no stench is detected, 1 if a stench is detected.

        stench_condition_knowledge = self.stench_list[current_room]  #1 # stench is detected

        variable_list.append(stench_condition_categorical)
        room_and_stench_list.append(stench_condition_knowledge)

     #   print ("variable_list:", variable_list)
     #   print ("edge list:    ", edge_list)
        print ("room_and_stench_list:  ", room_and_stench_list)

        # Run the model.
        neighbour_prob_dict = self.run_model_single(current_room_neighbours, variable_list, edge_list, room_and_stench_list)

        print ("neighbour_prob_dict:", neighbour_prob_dict)

        return neighbour_prob_dict