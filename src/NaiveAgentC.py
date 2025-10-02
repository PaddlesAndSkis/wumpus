# Import libraries.

import random

from AgentA import AgentA

class NaiveAgentC(AgentA):
    

    def select_next_move(self, percepts):
 
        percepts_list = []

        if (percepts.get_stench()):
            percepts_list.append("Stench")

        if (percepts.get_breeze()):
            percepts_list.append("Breeze")

        if (percepts.get_glitter()):
            percepts_list.append("Glitter")

        if (percepts.get_bump()):
            percepts_list.append("Bump")

        if (percepts.get_scream()):
            percepts_list.append("Scream")

        print("Agent senses...", percepts_list)

        possible_moves = [ 'Forward', 'TurnLeft', 'TurnRight', 'Shoot', 'Grab', 'Climb' ]
        
        random_move = random.randint(0, 5)

        print ("Next Move: ", possible_moves[random_move])
        
        return possible_moves[random_move]





