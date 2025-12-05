# EpisodeControllerC.py

# Import Project classes.

import Global

from AgentA import AgentA
from EnvironmentC import EnvironmentC


class EpisodeControllerC():
    
    # Constructor.

    def __init__(self, agent, environment):
        
        # The Episode Controller requires an Agent and an Environment.

        self.agent = agent
        self.environment = environment


    # playEpisode

    def playEpisode(self):

        # Display the initial board.

        if Global._display: self.environment.display_initial_episode()

        # Execute the episode until it is no longer active.

        agent_move = 0
        
        while (self.environment.is_active_episode()):

            # Increase the agent_move to track the number of movements in the episode.
            
            agent_move = agent_move + 1
            
            if Global._display: print (">>----- Agent Move", agent_move, "----->>")
            
            # Get the pre-action Percepts to notify the Agent.

            pre_action_percepts = self.environment.get_percepts()

            # Notify the Agent of the pre-action percepts.

            self.agent.percept(pre_action_percepts)

            # The Agent will now select its next action.

            action = self.agent.action()

            # Take the action selected by the Agent in the Environment.

            post_action_percepts = self.environment.take_action(action)
           
            # Determine if this is still an active episode after the action
            # has been taken (e.g., the Agent hasn't fallen into a pit or
            # has been eaten by the Wumpus).

            if (self.environment.is_active_episode()):

                # Notify the Agent of the post-action percepts.

                self.agent.percept(post_action_percepts)

            # Display the game board after each action.

            if Global._display: self.environment.display_board()


        # Print the final score for the Agent.

        print ("Episode Complete: the Agent's final score is:", self.environment.get_Agent_Score(), "in", agent_move, "moves.")
