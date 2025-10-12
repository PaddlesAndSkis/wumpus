# WumpusStateC.py

# Import Project classes.

from CharacterStateA import CharacterStateA


class WumpusStateC(CharacterStateA):

    # Constructor.

    def __init__(self, location):

        # Call the super class to set the location.

        super().__init__(location)

        # No other attributes required for WumpusState other than 
        # what is provided in the super class (location, isAlive).
