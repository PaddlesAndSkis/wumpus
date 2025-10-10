# AgentA.py

# Import libraries.

import Global

from abc import ABC, abstractmethod


class AgentA(ABC):


    # Constructor.

    def __init__(self):

        # Do nothing.

        self.percepts = None

        # Define the set of actions an Agent can take.

        self.action_set = [ 'Forward', 'TurnLeft', 'TurnRight', 'Shoot', 'Grab', 'Climb' ]



    def print_percepts(self):

        if Global._display:
            print ("Percepts:\t", end='')
            self.percepts.print()


    # percept

    @abstractmethod
    def percept(self, percepts):

        self.percepts = percepts

    
    # action

    @abstractmethod
    def action(self) -> str:

        # Implement an algorithm for selecting an action to take based on the percepts.
        
        # Return nil for the abstract class.
        
        return nil
    

