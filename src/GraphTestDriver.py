# GraphTestDriver

# Import libraries.

import networkx as nx

G = nx.DiGraph()

def main():

    start_node = (1, 1)
    direction = "east"
    
    # Create the initial node.

    create_initial_node(start_node, direction) 

    # Add the new node.

    move1_node = (2, 1)
    add_node(start_node, move1_node, direction)

    move2_node = (2, 2)
    direction = "north"
    add_node(move1_node, move2_node, direction)

    move3_node = (2, 3)
    direction = "north"
    add_node(move2_node, move3_node, direction)


    # Print the nodes and edges.

    print ("\nNodes:", G.nodes)
    print ("\nEdges:", G.edges)

    source = move3_node
    dest   = start_node

    create_exit_plan(source, dest)
    

    # Once you reach (1, 1) you can climb out - don't need to go from West to North to East.
    # That is what is meant in the assignment where you can remove the last few turns in the list
    # as they are superfluous.

    # Need to keep track of the actions that went through the graph.  Store them in the nodes?


def add_new_node_works(current_node, direction):

    # Add nodes.

    a = (1, 1)
    b = (2, 1)

    a_node_north = str(a) + "-north"
    a_node_south = str(a) + "-south"
    a_node_east  = str(a) + "-east"
    a_node_west  = str(a) + "-west"

    b_node_north = str(b) + "-north"
    b_node_south = str(b) + "-south"
    b_node_east  = str(b) + "-east"
    b_node_west  = str(b) + "-west"

    G.add_node(a_node_north, node=a, direction="north")
    G.add_node(a_node_south, node=a, direction="south")
    G.add_node(a_node_east,  node=a, direction="east")
    G.add_node(a_node_west,  node=a, direction="west")

    G.add_node(b_node_north, node=b, direction="north")
    G.add_node(b_node_south, node=b, direction="south")
    G.add_node(b_node_east,  node=b, direction="east")
    G.add_node(b_node_west,  node=b, direction="west")



    # Add edges.

    G.add_edge(a_node_north, a_node_west,  action="TurnLeft")
    G.add_edge(a_node_north, a_node_east,  action="right")
    G.add_edge(a_node_east,  a_node_north, action="TurnLeft")
    G.add_edge(a_node_east,  a_node_south, action="right")
    G.add_edge(a_node_south, a_node_east,  action="TurnLeft")
    G.add_edge(a_node_south, a_node_west,  action="right")
    G.add_edge(a_node_west,  a_node_south, action="TurnLeft")
    G.add_edge(a_node_west,  a_node_north, action="right")

    G.add_edge(b_node_north, b_node_west,  action="TurnLeft")
    G.add_edge(b_node_north, b_node_east,  action="right")
    G.add_edge(b_node_east,  b_node_north, action="TurnLeft")
    G.add_edge(b_node_east,  b_node_south, action="right")
    G.add_edge(b_node_south, b_node_east,  action="TurnLeft")
    G.add_edge(b_node_south, b_node_west,  action="right")
    G.add_edge(b_node_west,  b_node_south, action="TurnLeft")
    G.add_edge(b_node_west,  b_node_north, action="right")

    # Forward

    G.add_edge(a_node_east,  b_node_east,  action="forward")
    G.add_edge(b_node_west,  a_node_west,  action="forward")




    print ("Nodes:", G.nodes)
    print ("Edges:", G.edges)

    test_node = str(a) + "-north"

    print ("Testing the test node:", test_node)

    if test_node in G:
        print ("Node", test_node, "is in the graph")
    else:
        print ("Node", test_node, "is not in the graph")


    print (G.nodes[test_node]["direction"])
    print (G.nodes[test_node]["node"])

    add_node("hi", "there", "east")


def create_initial_node(start_node, direction):

    add_node(start_node, start_node, direction)



def add_node(current_node, new_node, direction):

    node_north = str(new_node) + "-north"
    node_south = str(new_node) + "-south"
    node_east  = str(new_node) + "-east"
    node_west  = str(new_node) + "-west"

    G.add_node(node_north, node=new_node, direction="north")
    G.add_node(node_south, node=new_node, direction="south")
    G.add_node(node_east,  node=new_node, direction="east")
    G.add_node(node_west,  node=new_node, direction="west")

    # Add edges and the action that would get you there.

    G.add_edge(node_north, node_west,  action="TurnLeft")
    G.add_edge(node_north, node_east,  action="TurnRight")
    G.add_edge(node_east,  node_north, action="TurnLeft")
    G.add_edge(node_east,  node_south, action="TurnRight")
    G.add_edge(node_south, node_east,  action="TurnLeft")
    G.add_edge(node_south, node_west,  action="TurnRight")
    G.add_edge(node_west,  node_south, action="TurnLeft")
    G.add_edge(node_west,  node_north, action="TurnRight")

    # Forward

    if (current_node != new_node):

        # Add the Forward direction.  North will point North and the
        # opposite will be true.

        current_north = str(current_node) + "-north"
        current_south = str(current_node) + "-south"
        current_east  = str(current_node) + "-east"
        current_west  = str(current_node) + "-west"

        if (direction == "north"):
            G.add_edge(current_north,  node_north,  action="Forward")
            G.add_edge(node_south,  current_south,  action="Forward")
        elif (direction == "east"):
            G.add_edge(current_east,  node_east,  action="Forward")
            G.add_edge(node_west,  current_west,  action="Forward")
        elif (direction == "south"):
            G.add_edge(current_south,  node_south,  action="Forward")
            G.add_edge(node_north,  current_north,  action="Forward")
        elif (direction == "west"):
            G.add_edge(current_west,  node_west,  action="Forward")
            G.add_edge(node_east,  current_east,  action="Forward")


def create_exit_plan(source, dest):

    source_node = str(source) + "-north"
    dest_node = str(dest) + "-east"

    print ("\nShortest Dijkstra path:", nx.shortest_path(G, source_node, dest_node, weight=None, method='dijkstra'))
    print ("\nShortest A* path:", nx.astar_path(G, source_node, dest_node, heuristic=None, weight='manhattan_distance'))

    short_path = nx.astar_path(G, source_node, dest_node, heuristic=None, weight='manhattan_distance')

    # Print out the nodes.

    for node in short_path:

        print (G.nodes[node]["node"], " ", G.nodes[node]["direction"])

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
        print (edge, " ", G.edges[edge]["action"])
        action_plan.append(G.edges[edge]["action"])

    print ("The agent's action plan:", action_plan)

# Test graph.

main()




 #   c = (3,3)

 #   c_node = str(c) + "-north"

#    print (c_node)

