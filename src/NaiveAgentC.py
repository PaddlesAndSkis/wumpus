# Import libraries.

import random

from AgentA import AgentA

class NaiveAgentC(AgentA):
    

    def select_next_move(self):

        possible_moves = [ 'Forward', 'TurnLeft', 'TurnRight', 'Shoot', 'Grab', 'Climb' ]
        
        random_move = random.randint(0, 5)

        print ("Next Move: ", possible_moves[random_move])
        
        return possible_moves[random_move]





