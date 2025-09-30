
class WumpusStateC:


    def __init__(self, location):

        # General.

        self.location = location
        self.isAlive = True


    # Getters and Setters.

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def get_isAlive(self):
        return self.isAlive

    def set_isAlive(self, isAlive):
        self.isAlive = isAlive

