from game_logic import *

def main():
    
    game = Game()

    # play 100 games while recording the winner of each game in a text file
    for i in range(100):
        game.run()

    game.end()

    # read file line by line, and print the number of wins for each player
    with open("winner.txt", "r") as f:
        winner = f.readlines()
        karapet_wins = winner.count("Karapet\n")
        papa_wins = winner.count("Papa\n")
        hh_wins = winner.count("HH\n")
        rr_wins = winner.count("RR\n")
        print("Karapet wins: ", karapet_wins)
        print("Papa wins: ", papa_wins)
        print("Hog wins: ", hh_wins)
        print("Rabbit wins: ", rr_wins)

main()