# GameControllerC.py

# Import Project classes.

import Global

from AgentA import AgentA
from EnvironmentC import EnvironmentC


class GameControllerC():
    
    # Constructor.

    def __init__(self, agent, environment):
        
        # The Game Controller requires an Agent and an Environment.

        self.agent = agent
        self.environment = environment


    # playEpisode

    def playEpisode(self):

        # Display the initial board.

        if Global._display: self.environment.display_initial_episode()

        # Execute the episode until it is no longer active.

        while (self.environment.is_active_episode()):

            if Global._display: print (">>--------------------")
            
            # Get the pre-action Percepts to notify the Agent.

            pre_action_percepts = self.environment.get_percepts()

            # Notify the Agent of the pre-action percepts.

            self.agent.percept(pre_action_percepts)

            # The Agent will now select its next action.

            action = self.agent.action()

            # Take the action selected by the Agent in the Environment.

            post_action_percepts = self.environment.take_action(action)
           
            # Notify the Agent of the post-action percepts.

            self.agent.percept(post_action_percepts)

            # Display the game board after each action.

            if Global._display: self.environment.display_board()


        # Print the final score for the Agent.

        print ("Episode Complete: the Agent's final score is: ", self.environment.get_Agent_Score())
