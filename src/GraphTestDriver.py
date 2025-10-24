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

    new_node = (2, 1)
    add_node(start_node, new_node, direction)

    next_node = (2, 2)
    direction = "north"
    add_node(new_node, next_node, direction)


    # Print the nodes and edges.

    print ("\nNodes:", G.nodes)
    print ("\nEdges:", G.edges)

    source_node = str(next_node) + "-north"
    dest_node = str(start_node) + "-east"

    print ("\nShortest Dijkstra path:", nx.shortest_path(G, source_node, dest_node, weight=None, method='dijkstra'))
    print ("\nShortest A* path:", nx.astar_path(G, source_node, dest_node, heuristic=None, weight='weight'))

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

    G.add_edge(a_node_north, a_node_west,  turn="left")
    G.add_edge(a_node_north, a_node_east,  turn="right")
    G.add_edge(a_node_east,  a_node_north, turn="left")
    G.add_edge(a_node_east,  a_node_south, turn="right")
    G.add_edge(a_node_south, a_node_east,  turn="left")
    G.add_edge(a_node_south, a_node_west,  turn="right")
    G.add_edge(a_node_west,  a_node_south, turn="left")
    G.add_edge(a_node_west,  a_node_north, turn="right")

    G.add_edge(b_node_north, b_node_west,  turn="left")
    G.add_edge(b_node_north, b_node_east,  turn="right")
    G.add_edge(b_node_east,  b_node_north, turn="left")
    G.add_edge(b_node_east,  b_node_south, turn="right")
    G.add_edge(b_node_south, b_node_east,  turn="left")
    G.add_edge(b_node_south, b_node_west,  turn="right")
    G.add_edge(b_node_west,  b_node_south, turn="left")
    G.add_edge(b_node_west,  b_node_north, turn="right")

    # Forward

    G.add_edge(a_node_east,  b_node_east,  turn="forward")
    G.add_edge(b_node_west,  a_node_west,  turn="forward")




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

    # Add edges.

    G.add_edge(node_north, node_west,  turn="left")
    G.add_edge(node_north, node_east,  turn="right")
    G.add_edge(node_east,  node_north, turn="left")
    G.add_edge(node_east,  node_south, turn="right")
    G.add_edge(node_south, node_east,  turn="left")
    G.add_edge(node_south, node_west,  turn="right")
    G.add_edge(node_west,  node_south, turn="left")
    G.add_edge(node_west,  node_north, turn="right")

    # Forward

    if (current_node != new_node):

        # Add the Forward direction.  North will point North and the
        # opposite will be true.

        current_north = str(current_node) + "-north"
        current_south = str(current_node) + "-south"
        current_east  = str(current_node) + "-east"
        current_west  = str(current_node) + "-west"

        if (direction == "north"):
            G.add_edge(current_north,  node_north,  turn="forward")
            G.add_edge(node_south,  current_south,  turn="forward")
        elif (direction == "east"):
            G.add_edge(current_east,  node_east,  turn="forward")
            G.add_edge(node_west,  current_west,  turn="forward")
        elif (direction == "south"):
            G.add_edge(current_south,  node_south,  turn="forward")
            G.add_edge(node_north,  current_north,  turn="forward")
        elif (direction == "west"):
            G.add_edge(current_west,  node_west,  turn="forward")
            G.add_edge(node_east,  current_east,  turn="forward")




# Test graph.

main()




 #   c = (3,3)

 #   c_node = str(c) + "-north"

#    print (c_node)

