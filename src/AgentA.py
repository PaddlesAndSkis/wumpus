# Import libraries.

from abc import ABC, abstractmethod

class AgentA(ABC):


    # Constructor.

    def __init__(self):

        # Do nothing.

        pass


    @abstractmethod
    def select_next_move(self):

        # Algorithm for selecting the next move.
        
        # Return nil for the abstract class.
        
        return nil


