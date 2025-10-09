class PerceptsC():

    def __init__(self, stench=False, breeze=False, glitter=False, bump=False, scream=False):

        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter
        self.bump = bump
        self.scream = scream


    # Getters and Setters.

    def get_stench(self):
        return self.stench 

    def set_stench(self, stench):
        self.stench = stench

    def get_breeze(self):
        return self.breeze 

    def set_breeze(self, breeze):
        self.breeze = breeze 

    def get_glitter(self):
        return self.glitter

    def set_glitter(self, glitter):
        self.glitter = glitter 

    def get_bump(self):
        return self.bump

    def set_bump(self, bump):
        self.bump = bump

    def get_scream(self):
        return self.scream

    def set_scream(self, scream):
        self.scream = scream


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

        print (percepts_list)


