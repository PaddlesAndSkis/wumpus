# GameControllerC.py

# Import Project classes.

import Global

from AgentA import AgentA
from EnvironmentC import EnvironmentC


class GameControllerC():
    
    # Constructor.

    def __init__(self, agent, environment):

        self.agent = agent
        self.environment = environment


    def playEpisode(self):

        # Display the initial board.

        if Global._display: self.environment.display_initial_episode()

        # Execute the episode until it is no longer active.

        while (self.environment.get_active_episode()):

            if Global._display: print (">>--------------------")
            
            # Get the pre-Action Percepts to notify the Agent.

            pre_action_percepts = self.environment.get_percepts()

            if Global._display:
                print ("Pre-Action Percepts:\t", end='')
                pre_action_percepts.print()

            # The Agent will select its next action based on the Percepts.

            next_action = self.agent.select_next_action(pre_action_percepts)

            # Get the post-Action Percepts to notify the Agent.

            post_action_percepts = self.environment.action_next_move(next_action)

            if Global._display:
                print ("Post-Action Percepts:\t", end='')
                post_action_percepts.print()

            # Display the game board.

            if Global._display: self.environment.display_board()


        # Print the final score for the Agent.

        print ("Episode Complete: the Agent's final score is: ", self.environment.get_Agent_Score())
