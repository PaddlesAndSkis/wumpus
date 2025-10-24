# MovePlanningAgentC.py

# Import libraries.

import random
import networkx as nx

# Import Project classes.

import Global

from AgentA import AgentA

class MovePlanningAgentC(AgentA):
    

    def __init__(self, location):

        # Set the state for having the Gold and its location.

        # The Agent should only be notified of its original location and can update it as it
        # builds the graph.

        self.has_gold = False
        self.location = location

        # Add the initial location as the root of the path tree.

     #   self.path_tree = nx.Graph()
        self.path_tree = nx.DiGraph(): 
        self.__add_initial_node(location)
        
      #  self.path_tree.add_node(location)


    # percept

    def percept(self, percepts):

        # For the Move Planning Agent, it will use the Percepts for grabbing the gold and
        # climbing out of the cave.

        # Call the super class to register the percepts.

        super().percept(percepts)

        new_location = self.percepts.get_move()

        if (len(new_location) != 0):
            self.__add_node_to_path(new_location)

        # Print the percepts.

        if Global._display:
            self.print_percepts()


    # action

    def action(self) -> str:
 
        action = None

        # For the Move Planning Agent, use its sensors to read the percepts to see if the gold 
        # is in the current room or if they can climb out the cave with the gold.

        if (self.percepts.get_glitter()) and (self.has_gold == False):

            # Glitter has been sensed.  Action the Grab.

            action = Global._grab_action

        elif (self.location == Global._start_room) and (self.has_gold == True):

            # Climb out!

            action = Global._climb_action
        else:
      
            # Randomly select one of the possible actions from the action set (minus
            # Grab and Climb).

            agent_action = random.randint(0, 3)

            if Global._display: print ("Action:\t\t\t", Global._action_array[agent_action])
        
            action = Global._action_array[agent_action]

        # Return the selected action.

        return action


    # Private methods.


    def __add_initial_node(self, initial_location):

        # Add the 4 nodes.

        self.path_tree.add_node(initial_location, direction=Global._north)
        self.path_tree.add_node(initial_location, direction=Global._east)
        self.path_tree.add_node(initial_location, direction=Global._south)
        self.path_tree.add_node(initial_location, direction=Global._west)

        # Add the 8 edges.
        attributes.get("direction") == target_name

        self.path_tree.add_edge(self.location, new_location, facing=)
        self.path_tree.add_edge(self.location, new_location)
        self.path_tree.add_edge(self.location, new_location)
        self.path_tree.add_edge(self.location, new_location)
        self.path_tree.add_edge(self.location, new_location)
        self.path_tree.add_edge(self.location, new_location)
        self.path_tree.add_edge(self.location, new_location)
        self.path_tree.add_edge(self.location, new_location)




    def __add_node_to_path(self, new_location):

        self.path_tree.add_node(new_location)
        self.path_tree.add_edge(self.location, new_location)

        if Global._display: 
            print ("Added node:", new_location)
            print ("Added edge:", self.location, " ", new_location)

            print ("Nodes now:", self.path_tree.nodes)
            print ("Edges now:", self.path_tree.edges)

        self.location = new_location

      #  G.add_node((1,1))
      #  G.add_node((1,2))

      #  G.add_edge((1,1),(1,2))

      #  print (G.nodes)
      #  print (G.edges)






