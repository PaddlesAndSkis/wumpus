# WumpusDriver.py

# Import Project classes.

import Global

from EnvironmentC import EnvironmentC
from NaiveAgentC import NaiveAgentC
from MovePlanningAgentC import MovePlanningAgentC
from ProbAgentC import ProbAgentC
from EpisodeControllerC import EpisodeControllerC


# main

def main():

    if Global._display: print ("Ready Player 1")

    # Initialize the Agent.

    # For Project 1, use the Naive Agent (does not store location)
    # For Project 2, use the Move Planning Agent (stores location)

    #myAgent = NaiveAgentC()
   # myAgent = MovePlanningAgentC(Global._start_room)
    myAgent = ProbAgentC(Global._start_room)
    
    # Initialize the environment.

    myEnvironment = EnvironmentC()

    # Initialize the game controller  and play the episode.

    episodeController = EpisodeControllerC(myAgent, myEnvironment)
    episodeController.playEpisode()



# Release the Wumpus!

main()
