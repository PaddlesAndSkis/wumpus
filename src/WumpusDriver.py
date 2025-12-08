# WumpusDriver.py

# Import Project classes.

import Global
import warnings

from EnvironmentC import EnvironmentC
from NaiveAgentC import NaiveAgentC
from MovePlanningAgentC import MovePlanningAgentC
from ProbAgentC import ProbAgentC
from EpisodeControllerC import EpisodeControllerC


# main

def main():

    # Filter out all warnings.

    warnings.filterwarnings("ignore")

    # Set local variables.

    number_of_episodes = 1000 #1000
    episode_wins = 0
    episode_scares = 0
    episode_total_score = 0

    print ("Ready Player 1")
    print ("--------------")
    print ("Starting the game... there are", number_of_episodes, "episodes to play.")

    for i in range(number_of_episodes):

        # Initialize the Agent.

        # For Project 1, use the Naive Agent (does not store location)
        # For Project 2, use the Move Planning Agent (stores location)

     #   myAgent = NaiveAgentC()
     #   myAgent = MovePlanningAgentC(Global._start_room)
        myAgent = ProbAgentC(Global._start_room)

        # Initialize the environment.

        myEnvironment = EnvironmentC()

        # Initialize the game controller  and play the episode.

        episodeController = EpisodeControllerC(myAgent, myEnvironment)
        episodeScore, episodeMoves = episodeController.playEpisode()

        # Print the final score for the Agent.

        if Global._display: print ("Episode Complete: the Agent's final score is:", episodeScore, "in", episodeMoves, "moves.")

        # Capture the wins.

        if (episodeScore > 0):
            episode_wins = episode_wins + 1

        # Capture the times the Agent was too scared to continue.

        if ((episodeScore < 0) and (episodeScore > -10)):
            episode_scares = episode_scares + 1

        episode_total_score = episode_total_score + episodeScore
        if Global._display: print ("episode_total_score:", episode_total_score)

        # Print out a status message every 100 episodes.

        if ((i != 0) and ((i % 100) == 0)):
            print ("Completed", i, "episodes...")


    print ("\nStats:")
    print ("------")
    print ("Number of episodes:", number_of_episodes)
    print ("Number of episode wins:", episode_wins)
    win_format = f"% of wins: {(episode_wins / number_of_episodes) * 100:.2f}"
    print (win_format)
    print ("Number of times Agent was too scared or climbed out quickly:", episode_scares)
    scare_format = f"% times Agent was too scared or climbed out quickly: {(episode_scares / number_of_episodes) * 100:.2f}"
    print (scare_format)
    print ("Average score:", (episode_total_score / number_of_episodes))
    print ("\nNote: for the Naive Agent, instead of being scared with reason, it is just simply climbing out")
    print ("        for the Move Planning Agent, it cannot climb out without having the gold")
    print ("        for the Probability Agent, it can climb out without having the gold if the next move is too dangerous for it")


# Release the Wumpus!

main()
