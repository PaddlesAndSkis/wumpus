
# Import classes and libraries.

from EnvironmentC import EnvironmentC
from NaiveAgentC import NaiveAgentC
from GameControllerC import GameControllerC

# main

def main():

    print ("Ready Player 1")

    # Initialize the Agent.

    myAgent = NaiveAgentC()

    # Initialize the environment.

    myEnvironment = EnvironmentC()

    # Initialize the game controller and play the episode.

    gameController = GameControllerC(myAgent, myEnvironment)
    gameController.playEpisode()



# Release the Wumpus!

main()
