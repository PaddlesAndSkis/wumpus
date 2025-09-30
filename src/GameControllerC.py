from AgentA import AgentA
from EnvironmentC import EnvironmentC

class GameControllerC():
    
    # Constructor.

    def __init__(self, agent, environment):

        self.agent = agent
        self.environment = environment


    def playEpisode(self):

        # Display the inital board.

        self.environment.display_board()

        while (self.environment.get_active_episode()):

#        for i in range(4):
            next_move = self.agent.select_next_move()

            self.environment.action_next_move(next_move)

            self.environment.display_board()



#        self.agent.forward()

#        self.environment.set_agent_loc(self.agent.get_agent_loc())
#        self.environment.display_board()

#        self.agent.turnRight()
#        self.agent.forward()

#        self.environment.set_agent_loc(self.agent.get_agent_loc())
#        self.environment.display_board()

#        self.agent.turnLeft()
 #       self.agent.forward()

 #       self.environment.set_agent_loc(self.agent.get_agent_loc())
 #       self.environment.display_board()



