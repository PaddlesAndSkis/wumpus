
# Import classes and libraries.

from EnvironmentC import EnvironmentC
from NaiveAgentC import NaiveAgentC
from GameControllerC import GameControllerC

# main

def main():

    print ("Welcome Player 1")

    # Initialize the Agent.

    #agent_loc = (1, 1)
    #myAgent = NaiveAgentC(agent_loc)
    myAgent = NaiveAgentC()

    # Initialize the environment.

    myEnvironment = EnvironmentC()

    # Initialize the game controller and play the episode.

    gameController = GameControllerC(myAgent, myEnvironment)
    gameController.playEpisode()



# Start the program.

main()
