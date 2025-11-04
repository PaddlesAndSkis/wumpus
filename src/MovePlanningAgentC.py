# MovePlanningAgentC.py

# Import libraries.

import random
import networkx as nx

# Import Project classes.

import Global

from AgentA import AgentA

class MovePlanningAgentC(AgentA):
    
    # Constructor.

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

            self.__add_node_to_graph(self.location, new_location, direction)
            
            # Update the Agent's location and direction.

            self.location  = new_location
            self.direction = direction

        # Print the percepts.

        if Global._display: self.print_percepts()


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

                self.exit_plan = self.__create_exit_plan(self.location, (1, 1), self.direction)

            elif (self.location == Global._start_room) and (self.has_gold == True):

                # The climb action is handled via the Agent's exit plan and the environment.

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

        # The start node is the special case - both the current and new nodes will be the
        # same start node.

        self.__add_node_to_graph(start_node, start_node, direction)


    # __add_node_to_graph

    def __add_node_to_graph(self, current_node, new_node, direction):

        # Add four nodes to the graph, one for each direction the Agent
        # can face - north, east, south and west.

        node_north = str(new_node) + "-" + Global._north
        node_south = str(new_node) + "-" + Global._south
        node_east  = str(new_node) + "-" + Global._east
        node_west  = str(new_node) + "-" + Global._west

        self.G.add_node(node_north, node=new_node, direction=Global._north)
        self.G.add_node(node_south, node=new_node, direction=Global._south)
        self.G.add_node(node_east,  node=new_node, direction=Global._east)
        self.G.add_node(node_west,  node=new_node, direction=Global._west)

        # Add the edges between the nodes and the action that would get you there.

        self.G.add_edge(node_north, node_west,  action=Global._turnLeft_action)
        self.G.add_edge(node_north, node_east,  action=Global._turnRight_action)
        self.G.add_edge(node_east,  node_north, action=Global._turnLeft_action)
        self.G.add_edge(node_east,  node_south, action=Global._turnRight_action)
        self.G.add_edge(node_south, node_east,  action=Global._turnLeft_action)
        self.G.add_edge(node_south, node_west,  action=Global._turnRight_action)
        self.G.add_edge(node_west,  node_south, action=Global._turnLeft_action)
        self.G.add_edge(node_west,  node_north, action=Global._turnRight_action)

        # Adding the Forward edges if there are two different nodes (i.e., not the
        # initial start node).

        if (current_node != new_node):

            # Add the Forward direction.  The direction of the node will point
            # to the same direction of the new node and the opposite will be true.
            # e.g., (1,1)-East will have an edge with (2,1)-East and (2,1)-West will
            # have an edge with (1,1)-West.

            current_north = str(current_node) + "-" + Global._north
            current_south = str(current_node) + "-" + Global._south
            current_east  = str(current_node) + "-" + Global._east
            current_west  = str(current_node) + "-" + Global._west

            # Determine the current direction and add the edges as indicated above in
            # the comment.

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


        if Global._debug: print ("\nNodes:", self.G.nodes)
        if Global._debug: print ("\nEdges:", self.G.edges)


    # __create_exit_plan

    def __create_exit_plan(self, source, dest, direction):
        
        source_node = str(source) + "-" + direction
        dest_node = str(dest) + "-" + Global._east

        if Global._display: print ("Status:\t\t\t*** Agent is creating an exit plan from", source_node, "to", dest)

        if Global._debug:   print ("\nShortest Dijkstra path:", nx.shortest_path(self.G, source_node, dest_node, weight=None, method='dijkstra'))
        if Global._display: print ("\nShortest A* path:", nx.astar_path(self.G, source_node, dest_node, heuristic=None, weight='manhattan_distance'))

        short_path = nx.astar_path(self.G, source_node, dest_node, heuristic=None, weight='manhattan_distance')

        # Print out the nodes if in debug mode.

        if Global._debug:

            for node in short_path:

                print (self.G.nodes[node]["node"], " ", self.G.nodes[node]["direction"])

        # The Agent only has to reach (1,1) in order to climb out,  Therefore, remove all
        # other nodes past the first (1,1) in the path.

        first_home_node = next(filter(lambda node: "(1, 1)" in node, short_path), None)

        first_home_node_idx = short_path.index(first_home_node)

        if Global._display: print ("Index of (1,1) is: ", first_home_node, "at node", first_home_node_idx, "in the path.")

        new_short_path = short_path[:first_home_node_idx+1]

        if Global._display: print ("New short_path =", new_short_path)

        # Build the edges from the path.

        path_edges = []
    
        for i in range(len(new_short_path) - 1):

            # Get the current and new nodes.

            node1 = new_short_path[i]
            node2 = new_short_path[i+1]

            # Add the edge.

            path_edges.append((node1, node2))

        action_plan = []

        # Iterate through the edges to build the action plan by finding the edge in the graph's
        # set of edges and getting the associated "action" with that particular edge.
        #
        # As this is a directed graph, and when we added the next set of nodes the directions between
        # the nodes were bi-directional (e.g., North-West = Left and West-North = Right), the
        # action associated with that edge will be the correct action to take to traverse that edge
        # from the current node to the next node in the edge pair.

        for edge in path_edges:
            if Global._debug: print (edge, " ", self.G.edges[edge]["action"])
            action_plan.append(self.G.edges[edge]["action"])

        # Finally, append the Climb action.

        action_plan.append(Global._climb_action)

        if Global._display: print ("Status:\t\t\t*** The Agent's exit plan is:", action_plan)

        return action_plan
