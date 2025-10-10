# NaiveAgentC.py

# Import libraries.

import random

# Import Project classes.

import Global

from AgentA import AgentA

class NaiveAgentC(AgentA):
    
    # select_next_action

    def select_next_action(self, percepts) -> str:
 
        # For the Naive Agent, the percepts will be received but not used
        # in selecting the next action.  The algorithm for selecting the next
        # action is random.

        # Define a list of possible actions.

        possible_actions = [ 'Forward', 'TurnLeft', 'TurnRight', 'Shoot', 'Grab', 'Climb' ]
        
        # Randomly select one of the possible actions.

        agent_action = random.randint(0, 5)

        if Global._display: print ("Selected Action:\t", possible_actions[agent_action])
        
        # Return the randomly selected action.

        return possible_actions[agent_action]





