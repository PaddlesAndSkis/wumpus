
# Import Project classes.

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

#Use Jupyter notebook for submission
#Use OO design
#Use 4x4 board 
#Use good visualization 
#Shoot without arrow -10 / -1 ; shoot with arrow -10 / -11
#Show percepts in your visualization for debugging but don't over do it'
#Set a flag for visualization on/off
#Set pit probability for future debugging / training
#Number your rows and columns from 1..4 for consistency
#Try to avoid nested if statements; use functions such as

#def isAdjacent(self, node) -> bool


#gold and pit can be on same 

#mcp - an intermediary orchestration system to connect AI / agents to back-end databases and tools 
#    - similar to an enterprise service bus
#    - by Antropic - open-source 



