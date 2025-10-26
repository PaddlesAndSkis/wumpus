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

        self.has_gold  = False
        self.location  = location
        self.direction = Global._east
        self.exit_plan = []

        # Add the initial location as the root of the path tree.

        self.G = nx.DiGraph()
        self.__create_initial_node(self.location, self.direction)
        

    # percept

    def percept(self, percepts):

        # For the Move Planning Agent, it will use the Percepts for grabbing the gold and
        # climbing out of the cave.

        # Call the super class to register the percepts.

        super().percept(percepts)

        new_location = self.percepts.get_move()
        direction    = self.percepts.get_direction()

        if (len(new_location) != 0):

            # Add the new node.

            self.__add_node(self.location, new_location, direction)
            
            # Update the Agent's location and direction.

            self.location  = new_location
            self.direction = direction

        # Print the percepts.

        if Global._display: self.print_percepts()


    # action

    def action(self) -> str:
 
        action = None

        print ("SELF EXIT PLAN ", self.exit_plan)
        if (len(self.exit_plan) > 0):

            print ("Exit plan    : ", self.exit_plan)

            action = self.exit_plan[0]

            print ("Action: ", action)

            self.exit_plan.pop(0)

            print ("Exit plan now: ", self.exit_plan)

        
        else:

            # For the Move Planning Agent, use its sensors to read the percepts to see if the gold 
            # is in the current room or if they can climb out the cave with the gold.

            if (self.percepts.get_glitter()) and (self.has_gold == False):

                print ("****** ATTEMPTING TO GLITTER ********")
                print ("****** ATTEMPTING TO GLITTER ********")
                print ("****** ATTEMPTING TO GLITTER ********")

                # Glitter has been sensed.  Action the Grab.

                action = Global._grab_action

                # Update the Agent's gold attribute.

                self.has_gold = True

                # Create the Exit plan that will be actioned the next time the Agent needs
                # to action.

                self.exit_plan = self.__create_exit_plan(self.location, (1, 1), self.direction)

            elif (self.location == Global._start_room) and (self.has_gold == True):

                # Climb out!

                print ("****** ATTEMPTING TO CLIMB ********  LOCAITON:", self.location)
                print ("****** ATTEMPTING TO CLIMB ******** HAS GOLD: ", self.has_gold)
                print ("****** ATTEMPTING TO CLIMB ********")
                print ("****** ATTEMPTING TO CLIMB ********")
                print ("****** ATTEMPTING TO CLIMB ********")

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


    
    def __create_initial_node(self, start_node, direction):

        self.__add_node(start_node, start_node, direction)



    def __add_node(self, current_node, new_node, direction):

        node_north = str(new_node) + "-north"
        node_south = str(new_node) + "-south"
        node_east  = str(new_node) + "-east"
        node_west  = str(new_node) + "-west"

        self.G.add_node(node_north, node=new_node, direction="north")
        self.G.add_node(node_south, node=new_node, direction="south")
        self.G.add_node(node_east,  node=new_node, direction="east")
        self.G.add_node(node_west,  node=new_node, direction="west")

        # Add edges and the action that would get you there.

        self.G.add_edge(node_north, node_west,  action="TurnLeft")
        self.G.add_edge(node_north, node_east,  action="TurnRight")
        self.G.add_edge(node_east,  node_north, action="TurnLeft")
        self.G.add_edge(node_east,  node_south, action="TurnRight")
        self.G.add_edge(node_south, node_east,  action="TurnLeft")
        self.G.add_edge(node_south, node_west,  action="TurnRight")
        self.G.add_edge(node_west,  node_south, action="TurnLeft")
        self.G.add_edge(node_west,  node_north, action="TurnRight")

        # Forward

        if (current_node != new_node):

            # Add the Forward direction.  North will point North and the
            # opposite will be true.

            current_north = str(current_node) + "-north"
            current_south = str(current_node) + "-south"
            current_east  = str(current_node) + "-east"
            current_west  = str(current_node) + "-west"

            if (direction == "north"):
                self.G.add_edge(current_north,  node_north,  action="Forward")
                self.G.add_edge(node_south,  current_south,  action="Forward")
            elif (direction == "east"):
                self.G.add_edge(current_east,  node_east,  action="Forward")
                self.G.add_edge(node_west,  current_west,  action="Forward")
            elif (direction == "south"):
                self.G.add_edge(current_south,  node_south,  action="Forward")
                self.G.add_edge(node_north,  current_north,  action="Forward")
            elif (direction == "west"):
                self.G.add_edge(current_west,  node_west,  action="Forward")
                self.G.add_edge(node_east,  current_east,  action="Forward")


        print ("\nNodes:", self.G.nodes)
        print ("\nEdges:", self.G.edges)


    def __create_exit_plan(self, source, dest, direction):

        source_node = str(source) + "-" + direction
        dest_node = str(dest) + "-east"

        print ("\nShortest Dijkstra path:", nx.shortest_path(self.G, source_node, dest_node, weight=None, method='dijkstra'))
        print ("\nShortest A* path:", nx.astar_path(self.G, source_node, dest_node, heuristic=None, weight='manhattan_distance'))

        short_path = nx.astar_path(self.G, source_node, dest_node, heuristic=None, weight='manhattan_distance')

        # Print out the nodes.

        for node in short_path:

            print (self.G.nodes[node]["node"], " ", self.G.nodes[node]["direction"])

        # Build the edges from the path.

        path_edges = []
    
        for i in range(len(short_path) - 1):
            u = short_path[i]
            v = short_path[i+1]
            path_edges.append((u, v))

        action_plan = []

        # Iterate through the edges to build the action plan by finding the edge in the graph's
        # set of edges and getting the associated "action" with that particular edge.
        #
        # As this is a directed graph, and when we added the next set of nodes the directions between
        # the nodes were bi-directional (e.g., North-West = Left and West-North = Right), the
        # action associated with that edge will be the correct action to take to traverse that edge
        # from the current node to the next node in the edge pair.

        for edge in path_edges:
            print (edge, " ", self.G.edges[edge]["action"])
            action_plan.append(self.G.edges[edge]["action"])

        # Finally, append the Climb action.

        action_plan.append("Climb")

        print ("The agent's action plan:", action_plan)

        return action_plan



    def __add_initial_node(self, initial_location):

        # Add the 4 nodes.

        self.path_tree.add_node(initial_location, direction=Global._north)
        self.path_tree.add_node(initial_location, direction=Global._east)
        self.path_tree.add_node(initial_location, direction=Global._south)
        self.path_tree.add_node(initial_location, direction=Global._west)

        # Add the 8 edges.
        attributes.get("direction") == target_name

        self.path_tree.add_edge(self.location, new_location)
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






