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
        self.__create_start_node_in_graph(self.location, self.direction)
        

    # percept

    def percept(self, percepts):

        # For the Move Planning Agent, it will use the Percepts for grabbing the gold and
        # climbing out of the cave.

        # Call the super class to register the percepts.

        super().percept(percepts)

        new_location = self.percepts.get_move()
        direction    = self.percepts.get_direction()

        if (len(new_location) != 0):

            # Add the new node to the graph.

            self.__add_node_to_graph(self.location, new_location, direction)
            
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


    # __create_start_node_in_graph
    
    def __create_start_node_in_graph(self, start_node, direction):

        self.__add_node_to_graph(start_node, start_node, direction)


    # __add_node

    def __add_node_to_graph(self, current_node, new_node, direction):

        node_north = str(new_node) + "-" + Global._north
        node_south = str(new_node) + "-" + Global._south
        node_east  = str(new_node) + "-" + Global._east
        node_west  = str(new_node) + "-" + Global._west

        self.G.add_node(node_north, node=new_node, direction=Global._north)
        self.G.add_node(node_south, node=new_node, direction=Global._south)
        self.G.add_node(node_east,  node=new_node, direction=Global._east)
        self.G.add_node(node_west,  node=new_node, direction=Global._west)

        # Add edges and the action that would get you there.

        self.G.add_edge(node_north, node_west,  action=Global._turnLeft_action)
        self.G.add_edge(node_north, node_east,  action=Global._turnRight_action)
        self.G.add_edge(node_east,  node_north, action=Global._turnLeft_action)
        self.G.add_edge(node_east,  node_south, action=Global._turnRight_action)
        self.G.add_edge(node_south, node_east,  action=Global._turnLeft_action)
        self.G.add_edge(node_south, node_west,  action=Global._turnRight_action)
        self.G.add_edge(node_west,  node_south, action=Global._turnLeft_action)
        self.G.add_edge(node_west,  node_north, action=Global._turnRight_action)

        # Forward

        if (current_node != new_node):

            # Add the Forward direction.  North will point North and the
            # opposite will be true.

            current_north = str(current_node) + "-" + Global._north
            current_south = str(current_node) + "-" + Global._south
            current_east  = str(current_node) + "-" + Global._east
            current_west  = str(current_node) + "-" + Global._west

            if (direction == Global._north):
                self.G.add_edge(current_north,  node_north,  action=Global._forward_action)
                self.G.add_edge(node_south,  current_south,  action=Global._forward_action)
            elif (direction == Global._east):
                self.G.add_edge(current_east,  node_east,  action=Global._forward_action)
                self.G.add_edge(node_west,  current_west,  action=Global._forward_action)
            elif (direction == Global._south):
                self.G.add_edge(current_south,  node_south,  action=Global._forward_action)
                self.G.add_edge(node_north,  current_north,  action=Global._forward_action)
            elif (direction == Global._west):
                self.G.add_edge(current_west,  node_west,  action=Global._forward_action)
                self.G.add_edge(node_east,  current_east,  action=Global._forward_action)


        print ("\nNodes:", self.G.nodes)
        print ("\nEdges:", self.G.edges)


    # __create_exit_plan

    def __create_exit_plan(self, source, dest, direction):

        source_node = str(source) + "-" + direction
        dest_node = str(dest) + "-" + Global._east

        print ("\nShortest Dijkstra path:", nx.shortest_path(self.G, source_node, dest_node, weight=None, method='dijkstra'))
        print ("\nShortest A* path:", nx.astar_path(self.G, source_node, dest_node, heuristic=None, weight='manhattan_distance'))

        short_path = nx.astar_path(self.G, source_node, dest_node, heuristic=None, weight='manhattan_distance')

        # Print out the nodes.

        for node in short_path:

            print (self.G.nodes[node]["node"], " ", self.G.nodes[node]["direction"])

        # The Agent only has to reach (1,1) in order to climb out,  Therefore, remove all
        # other nodes past the first (1,1) in the path.

        first_home_node = next(filter(lambda node: "(1, 1)" in node, short_path), None)

        first_home_node_idx = short_path.index(first_home_node)

        print ("Index of (1,1) is: ", first_home_node, "at", first_home_node_idx)

        new_short_path = short_path[:first_home_node_idx+1]

        print ("new short_path =", new_short_path)

        # Build the edges from the path.

        path_edges = []
    
        for i in range(len(new_short_path) - 1):
            u = new_short_path[i]
            v = new_short_path[i+1]
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

        action_plan.append(Global._climb_action)

        print ("The agent's action plan:", action_plan)

        return action_plan
