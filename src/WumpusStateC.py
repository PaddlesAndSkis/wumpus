# Import Project classes.

from CharacterStateA import CharacterStateA


class WumpusStateC(CharacterStateA):


     def __init__(self, location):

        # Call the super class.

        super().__init__(location)

        # No other attributes for WumpusState other than 
        # the super class.
