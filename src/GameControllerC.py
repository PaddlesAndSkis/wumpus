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

        self.environment.display_initial_episode()

        # Execute the episode until it is not activate.

        while (self.environment.get_active_episode()):

            print (">>--------------------")
            
            # Get the pre-Action Percepts to notify the Agent.

            pre_action_percepts = self.environment.get_percepts()

            # The Agent will select its next move based on the Percepts.

            next_move = self.agent.select_next_move(pre_action_percepts)

            post_action_percepts = self.environment.action_next_move(next_move)

            # Add to the PerceptsC class

            post_action_percepts_list = []

            if (post_action_percepts.get_stench()):
                post_action_percepts_list.append("Stench")

            if (post_action_percepts.get_breeze()):
                post_action_percepts_list.append("Breeze")

            if (post_action_percepts.get_glitter()):
                post_action_percepts_list.append("Glitter")

            if (post_action_percepts.get_bump()):
                post_action_percepts_list.append("Bump")

            if (post_action_percepts.get_scream()):
                post_action_percepts_list.append("Scream")

            print ("Post-action Percepts:\t", post_action_percepts_list)

            # Display the game board.

            # Why are these not seeming to show up.

            self.environment.display_board(pre_action_percepts, post_action_percepts)

        # Get the final score for the Agent.

        agent_score = self.environment.get_Agent_Score()

        print ("The Agent's final score is: ", agent_score)
