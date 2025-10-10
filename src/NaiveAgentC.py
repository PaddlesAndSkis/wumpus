# NaiveAgentC.py

# Import libraries.

import random

# Import Project classes.

import Global

from AgentA import AgentA

class NaiveAgentC(AgentA):
    
    # percept

    def percept(self, percepts):

        # For the Naive Agent that isn't using Percepts, just
        # call the super class.

        super().percept(percepts)

        # Print the percepts.

        if Global._display:
            self.print_percepts()


    # action

    def action(self) -> str:
 
        # For the Naive Agent, the percepts will be received but not used
        # in selecting the action to take.  The algorithm for selecting the
        # action to take is random.
        
        # Randomly select one of the possible actions from the action set.

        agent_action = random.randint(0, 5)

        if Global._display: print ("Selected Action:\t", Global._action_set[agent_action])
        
        # Return the randomly selected action.

        return Global._action_set[agent_action]





