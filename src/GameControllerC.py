# Import Project classes.

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

            print (">>--------------------")
            
            # Get the Percepts to notify the Agent.

            myPercepts = self.environment.get_percepts()

            # The Agent will select its next move based on the Percepts.

            next_move = self.agent.select_next_move(myPercepts)

            myActionPercepts = self.environment.action_next_move(next_move)

            # Add to the PerceptsC class

            percepts_list = []

            if (myActionPercepts.get_stench()):
                percepts_list.append("Stench")

            if (myActionPercepts.get_breeze()):
                percepts_list.append("Breeze")

            if (myActionPercepts.get_glitter()):
                percepts_list.append("Glitter")

            if (myActionPercepts.get_bump()):
                percepts_list.append("Bump")

            if (myActionPercepts.get_scream()):
                percepts_list.append("Scream")



            print ("Post-action Percepts:\t", percepts_list)
            self.environment.display_board()

        # Get the final score for the Agent.

        agent_score = self.environment.get_Agent_Score()

        print ("The Agent's final score is: ", agent_score)
