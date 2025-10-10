# AgentA.py

# Import libraries.

from abc import ABC, abstractmethod


class AgentA(ABC):


    # Constructor.

    def __init__(self):

        # Do nothing.

        pass

    
    # select_next_action

    @abstractmethod
    def select_next_action(self, percepts) -> str:

        # Implement an algorithm for selecting the next action.
        
        # Return nil for the abstract class.
        
        return nil
    

