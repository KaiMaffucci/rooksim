from game_logic import *
from time import time
import sys

def main():

    # If a command line argument is passed, play that number of games
    try:
        games_to_play = int(sys.argv[-1])
    except:
        games_to_play = 100 # Default

    start_time = time()
    game = Game()

    # play games while recording the winner of each game in a text file
    for i in range(games_to_play):
        game.games_played += 1
        game.run()
        
    game.end()
    elapsed_time = time() - start_time

    # read file line by line, and print the number of wins for each player 
    with open("winner_individuals.txt", "r") as f:
        winner = f.readlines()
        karapet_wins = winner.count("Karapet\n")
        papa_wins = winner.count("Papa\n")
        hh_wins = winner.count("HH\n")
        rr_wins = winner.count("RR\n")
        print("Karapet wins: ", karapet_wins)
        print("Papa wins: ", papa_wins)
        print("Hog wins: ", hh_wins)
        print("Rabbit wins: ", rr_wins)

    print("Total simulation time for", games_to_play, "games:", elapsed_time, "sec")
    print("Simulation time per game:", (elapsed_time / games_to_play) * 10**3, "ms")

    # read plays file, print last 5 lines
    with open("plays.txt", "r") as f:
        plays = f.readlines()
        for line in plays[-5:]:
            print(line.strip())
main()
