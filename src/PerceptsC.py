# PerceptsC.py

class PerceptsC():

    # Constructor

    def __init__(self, stench=False, breeze=False, glitter=False, bump=False, scream=False, move=(), direction=None):

        # Set object attributes.

        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter
        self.bump = bump
        self.scream = scream
        self.move = move
        self.direction = direction


    # Getters and Setters.

    def get_stench(self) -> bool:
        return self.stench 

    def set_stench(self, stench):
        self.stench = stench

    def get_breeze(self) -> bool:
        return self.breeze 

    def set_breeze(self, breeze):
        self.breeze = breeze 

    def get_glitter(self) -> bool:
        return self.glitter

    def set_glitter(self, glitter):
        self.glitter = glitter 

    def get_bump(self) -> bool:
        return self.bump

    def set_bump(self, bump):
        self.bump = bump

    def get_scream(self) -> bool:
        return self.scream

    def set_scream(self, scream):
        self.scream = scream


    def get_move(self) -> tuple([int, int]):
        return self.move

    def set_move(self, move):
        self.move = move

    def get_direction(self) -> str:
        return self.direction

    def set_direction(self, direction):
        self.direction = direction


    # print

    def print(self):

        # Add to the PerceptsC class

        percepts_list = []

        if (self.get_stench()):
            percepts_list.append("Stench")

        if (self.get_breeze()):
            percepts_list.append("Breeze")

        if (self.get_glitter()):
            percepts_list.append("Glitter")

        if (self.get_bump()):
            percepts_list.append("Bump")

        if (self.get_scream()):
            percepts_list.append("Scream")

        if (self.get_move()):
            percepts_list.append("Move")

        if (self.get_direction()):
            percepts_list.append("Direction")

        print (percepts_list)


