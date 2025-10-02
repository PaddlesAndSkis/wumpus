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

            # Get the Percepts to notify the Agent.

            myPercepts = self.environment.get_percepts()

            # The Agent will select its next move based on the Percepts.

            next_move = self.agent.select_next_move(myPercepts)

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



