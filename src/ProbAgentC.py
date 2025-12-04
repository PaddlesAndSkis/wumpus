# ProbAgentC

# Import libraries.

import random
import networkx as nx


# Import Project classes.

import torch
from torch._prims_common import Tensor
import Global

from MovePlanningAgentC import MovePlanningAgentC
from PredicateC import PredicateC

from pomegranate.distributions import Categorical
from pomegranate.distributions import ConditionalCategorical
from pomegranate.bayesian_network import BayesianNetwork

import torch

import numpy

class ProbAgentC(MovePlanningAgentC):

    # Constructor

    def __init__(self, location):

        # Invoke the super class.

        super().__init__(location)
        
        print ("hello there Cam")

        self.build_model()

        current_room =  "1-1" #"2-2" #"1-2"  # "1-1"

        self.get_move_options(current_room)

      #  exit(0)





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

        # Determine if a move has been made.

        if (len(new_location) != 0):

            # A move has been made, add the new node to the graph.
                    
            if Global._display: print ("Action Result:\t\tLooking to add", new_location, "facing", direction, "(and other directions) to the visited room graph.")

            # CHANGED TO SUPER
            #self.__add_node_to_graph(self.location, new_location, direction)
            self._add_node_to_graph(self.location, new_location, direction)
            
            # Update the Agent's location and direction.

            self.location  = new_location
            self.direction = direction

        # Print the percepts.

        if Global._display: self.print_percepts()

        # Do we detect a breeze?  Maybe here decide best next move


    # action

    def action(self) -> str:
 
        print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! CURRENT ROOM:", self.location)

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

            else:
      
                # Know location and direction

                # 
                x = self.location[0]
                y = self.location[1]
                location_conversion = str(x) + "-" + str(y)

                print ("******* Agent is in: ", self.location, "facing", self.direction)
                print ("******* Converted Location: ", location_conversion)
                move_options = self.get_move_options(location_conversion)

             
                # Call the model to determine which neighbour we should move to.

                # If north and facing south, create a "turn plan" and add this to the action
                # similar to the exit plan "turn left; turn left"  ("Turning...")

                # _forward_action   = "Forward"
                    #_turnLeft_action  = "TurnLeft"
                    #_turnRight_action = "TurnRight"
                    #_shoot_action     = "Shoot"

                # Do we randomly shoot the arrow or shoot the arrow when we smell the wumpus?



                # Randomly select one of the possible actions from the action set (minus
                # Grab and Climb).

                agent_action = random.randint(0, 3)

                if Global._display: print ("Action:\t\t\t", Global._action_array[agent_action])
        
                action = Global._action_array[agent_action]

        # Return the selected action.

        return action




    def build_model(self):

        # Dictionary of rooms as each room is unique (e.g., "1-1").

        self.rooms_dict = {}

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

                print ("(", i, ",", j, ") -> ", neighbours)

                # Construct the room key and add it and the neighbours to the room dictionary.

                my_key = str(i) + "-" + str(j)

                self.rooms_dict[my_key] = neighbours

        # Print the rooms dictionary.

        print("Rooms:", self.rooms_dict)

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

        # Iterate over the room keys which will include all rooms in the cave.
        # Create the categorical probability for the dictionary
        # Set each room to be unknown for a pit and unknown for a breeze.

        for room_key in self.rooms_dict.keys():

            self.pit_predicate_list[room_key] = pit_categorical
            self.pit_list[room_key]           = pit_unknown
            self.breeze_list[room_key]        = breeze_unknown

        # Room 1-1 cannot be a pit.  Therefore, it will be set to 0 (safe).

        self.pit_list["1-1"] = 0

        self.pit_list["1-2"] = 1   # Exxample for testing

        # Print out the pit predicate list and the pit list.

        print ("pit_predicate_list", self.pit_predicate_list)
        print ("pit_list", self.pit_list)
        print ("breeze_list", self.breeze_list)


        # Start of code that gets run every time an Agent wants to move forward.
        #
        #

    def get_move_options(self, current_room):

        # Now, setup the breeze room by getting the first room (1-1).
        # This can be done by iterating over the keys.

       # breeze_room =  "1-1" #"2-2" #"1-2"  # "1-1"
        #pit_list["2-2"] = 0             # Remove this, just here to simulate that the Agent is safe
        current_room_cases = []

        # Get the breeze room's neighbours.

        current_room_neighbours = self.rooms_dict[current_room]
        current_room_neighbours_count = len(current_room_neighbours)

        print ("The number of neighbours that breeze room", current_room, "has is", current_room_neighbours_count)



     #   pit21 = PredicateC(0.2).toCategorical()

       # pit12 = "1-2"
       # print ("pit12 should be Categorical = ", pit_predicate_list[pit12])

      #  pit_categorical = pit_predicate_list[pit12]
      #  print ("pit12.probs (T) = ", pit_categorical.probs[0][1])

        if (current_room_neighbours_count == 2):
            
            current_room_cases = self.create_cases_2()

        elif (current_room_neighbours_count == 3):

            current_room_cases = self.create_cases_3()

        elif (current_room_neighbours_count == 4):

            current_room_cases = self.create_cases_4()

        print ("Breeze room cases:", current_room_cases)

        # Create the probability matrix for the breeze room and the predicate.
        # Create the knowledge of the breeze room if it's a pit or not (should be 0 - safe as
        # the Agent would have died otherwise).
         
        breeze_condition_categorical = ConditionalCategorical([current_room_cases])
        breeze_condition_predicate   = self.pit_predicate_list[current_room]     # !!! Remove -This isn't used - breeze useses the categorical value that contains the cases not the predicate value

        print ("Breeze11 condition categorical:", breeze_condition_categorical)
        print ("Breeze11 condition predicate:  ", breeze_condition_predicate)

        # Create the variables (breeze room and its adjacent rooms) and the
        # edges (an edge is from an adjacent room to the breeze room).

        variable_list        = []
        edge_list            = []
        room_and_breeze_list = []

        for current_room_neighbour in current_room_neighbours:

            # Create the room predicate.

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

        print ("variable_list:", variable_list)
        print ("edge list:    ", edge_list)
        print ("room_and_breeze_list:  ", room_and_breeze_list)

        # Run the model.
        neighbour_prob_dict = self.run_model_single(current_room_neighbours, variable_list, edge_list, room_and_breeze_list)

        print ("neighbour_prob_dict:", neighbour_prob_dict)
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

  #  def run_model(self, pit12, pit21, breeze11):
    def run_model(self, variables, edges):

        # Construct the model with the three variables, and two edges

      #  variables = [pit12, pit21, breeze11]
      #  edges = [(pit12, breeze11), (pit21, breeze11)]

        # Check shapes
        print('variables shape', numpy.array(variables).shape)
        print('edges shape', numpy.array(edges).shape)

        pits_model = BayesianNetwork(variables, edges)

        # Note that model.bake() is not required as it was in earlier versions of Pomegranate

        X = torch.tensor([[-1, -1, 0],  # pit12?, pit21?, breeze11 is false
                          [-1, -1, 1],  # pit12?, pit21?, breeze11 is true
                          [-1, -1, -1], # pit12?, pit21?, breeze11?
                          [1, -1, -1]   # pit12 is true, pit21?, breeze11?
                         ])

        X_masked = torch.masked.MaskedTensor(X, mask=X >= 0)
        print(X_masked)


        my_tensors = pits_model.predict_proba(X_masked)

        print ("Tensors:", my_tensors)


    def create_cases(self, neighbours):

        cases2 = []
        num_neighbours = len(neighbours)
        print ("neighbours = ", neighbours)
        print ("len of neighbours = ", num_neighbours)

      #  if (num_neighbours == 2):

      #      for i in [False, True]:
      #          c = []
       #         for j in [False, True]:
      ##              case = i or j      # we can use or between them because we have a breeze if there is a pit in any of the adjacent squares
       #             if case:
       #                 p = 1.0
       #             else:
       #                 p = 0.0
       #             c.append(PredicateC(p).toList())
       #         cases.append(c)

       # elif (num_neighbours == 4):
        if True:

            for index, neighbour in enumerate(neighbours, start=1):
                print ("index", index, "->", neighbour)

            for index, neighbour in enumerate(neighbours):

                print ("***Neighbour", neighbour, "at index", index, "and", index+1)

                for index2, neighbour2 in enumerate(neighbours[index+1:]): #, start=1):
        
                    cases = []

                    print ("\tIndex2: looking at neighbour", neighbour, "and", neighbour2)

                    for i in [False, True]:
                        c = []
                        for j in [False, True]:
                            case = i or j      # we can use or between them because we have a breeze if there is a pit in any of the adjacent squares
                            if case:
                                p = 1.0
                            else:
                                p = 0.0
                            c.append(PredicateC(p).toList())

                            print ("c:", c)

                        cases.append(c)
                        print ("cases for:", neighbour, "and", neighbour2, ":", cases)
                
                    cases2.append(cases)
                    print ("cases2 now:", cases2)

        print("Cases2: ", cases2) # check to make sure it is what we expect

        return cases2
       # print("breeze11.probs:", breeze11.probs)  











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

    


    # Old Constructor

    #def __init__(self, location):

    #    # Invoke the super class.

    #    super().__init__(location)
        
    #    print ("hello there Cam")

    # #   myPredicate = PredicateC(.8)
    #    pit12 = PredicateC(0.2).toCategorical()
    #    pit21 = PredicateC(0.2).toCategorical()

    #    print ("pit12 should be Categorical = ", pit12)
    #    print ("pit21 should be Categorical = ", pit21)

    #    print ("pit12.probs (T) = ", pit12.probs[0][1])
    #    print ("pit12.probs (F) = ", pit12.probs[0][0])

    #    print ("pit21.probs (T) = ", pit21.probs[0][1])
    #    print ("pit21.probs (F) = ", pit21.probs[0][0])

    #    breeze11 = ConditionalCategorical([[
    #        [[1.0, 0.0], [0.0, 1.0]],
    #        [[0.0, 1.0], [0.0, 1.0]]
    #    ]])


    #    cases = []
    #    for p12 in [False, True]:
    #        c = []
    #        for p21 in [False, True]:
    #            case = p12 or p21      # we can use or between them because we have a breeze if there is a pit in any of the adjacent squares
    #            if case:
    #                p = 1.0
    #            else:
    #                p = 0.0
    #            c.append(PredicateC(p).toList())
    #        cases.append(c)

    #    print("Cases: ", cases) # check to make sure it is what we expect
    #    print("breeze11.probs:", breeze11.probs)  



    #    breeze11 = ConditionalCategorical([
    #        cases
    #    ])



    #    #
    #    # Do this each time the Agent moves...
    #    #


    #    # Construct the model with the three variables, and two edges

    #    variables = [pit12, pit21, breeze11]
    #    edges = [(pit12, breeze11), (pit21, breeze11)]

    #    print ("variables:", variables)
    #    print ("edges:    ", edges)

    #    # Check shapes
    #    print('variables shape', numpy.array(variables).shape)
    #    print('edges shape', numpy.array(edges).shape)

    #    pits_model = BayesianNetwork(variables, edges)

    #    # Note that model.bake() is not required as it was in earlier versions of Pomegranate

    #    X = torch.tensor([[-1, -1, 0],  # pit12?, pit21?, breeze11 is false
    #                      [-1, -1, 1],  # pit12?, pit21?, breeze11 is true
    #                      [-1, -1, -1], # pit12?, pit21?, breeze11?
    #                      [1, -1, -1]   # pit12 is true, pit21?, breeze11?
    #                     ])

    #    X_masked = torch.masked.MaskedTensor(X, mask=X >= 0)
    #    print(X_masked)


    #    my_tensors = pits_model.predict_proba(X_masked)

    #    print ("Tensors:", my_tensors)


    #    # Let's do this again but through functions


    #    self.build_model()

    #    exit(0)