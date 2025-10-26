# WumpusDriver.py

# Import Project classes.

import Global

from EnvironmentC import EnvironmentC
from NaiveAgentC import NaiveAgentC
from MovePlanningAgentC import MovePlanningAgentC
from EpisodeControllerC import EpisodeControllerC


# main

def main():

    if Global._display: print ("Ready Player 1")

    # Initialize the Agent.

    #myAgent = NaiveAgentC()
    myAgent = MovePlanningAgentC(Global._start_room)

    # Initialize the environment.

    myEnvironment = EnvironmentC()

    # Initialize the game controller and play the episode.

    episodeController = EpisodeControllerC(myAgent, myEnvironment)
    episodeController.playEpisode()



# Release the Wumpus!

main()


#mcp - an intermediary orchestration system to connect AI / agents to back-end databases and tools 
#    - similar to an enterprise service bus
#    - by Antropic - open-source 



