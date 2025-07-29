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

    # read file and count occurrences of each player's name anywhere in the file
    with open("winners.txt", "r") as f:

        content = f.read()

        # Count individual wins for each player
        karapet_wins = content.count("Karapet")
        papa_wins = content.count("Papa")
        hh_wins = content.count("HH")
        rr_wins = content.count("RR")

        # Print individual wins
        print("Karapet wins: ", karapet_wins)
        print("Papa wins: ", papa_wins)
        print("Hog wins: ", hh_wins)
        print("Rabbit wins: ", rr_wins)

        # Count wins for each pair of players
        karapet_papa_wins = content.count("Karapet Papa") + content.count("Papa Karapet")
        karapet_hh_wins = content.count("Karapet HH") + content.count("HH Karapet")
        karapet_rr_wins = content.count("Karapet RR") + content.count("RR Karapet")
        papa_hh_wins = content.count("Papa HH") + content.count("HH Papa")
        papa_rr_wins = content.count("Papa RR") + content.count("RR Papa")
        hh_rr_wins = content.count("HH RR") + content.count("RR HH")

        # Print pair wins
        print("Karapet and Papa wins: ", karapet_papa_wins)
        print("Karapet and Hog wins: ", karapet_hh_wins)
        print("Karapet and Rabbit wins: ", karapet_rr_wins)
        print("Papa and Hog wins: ", papa_hh_wins)
        print("Papa and Rabbit wins: ", papa_rr_wins)
        print("Hog and Rabbit wins: ", hh_rr_wins)

    print("Total simulation time for", games_to_play, "games:", elapsed_time, "sec")
    print("Simulation time per game:", (elapsed_time / games_to_play) * 10**3, "ms")

    trimester_1_wins = {"Karapet": 0, "Papa": 0, "HH": 0, "RR": 0}
    trimester_2_wins = {"Karapet": 0, "Papa": 0, "HH": 0, "RR": 0}
    trimester_3_wins = {"Karapet": 0, "Papa": 0, "HH": 0, "RR": 0}
    total_trimester_wins = {"Karapet": 0, "Papa": 0, "HH": 0, "RR": 0}

    # read plays file, print last 5 lines
    with open("plays.txt", "r") as f:
        plays = f.readlines()
        last_lines = plays[-5:] if len(plays) >= 5 else plays
        for line in last_lines:

            print(line.strip())

            if "Karapet" in line:

                # Increment Karapet's wins in each trimester based on the first number in the line
                trimester_1_wins["Karapet"] += int(line.split()[1])
                trimester_2_wins["Karapet"] += int(line.split()[2])
                trimester_3_wins["Karapet"] += int(line.split()[3])
                total_trimester_wins["Karapet"] += int(line.split()[1]) + int(line.split()[2]) + int(line.split()[3])
            
            elif "Papa" in line:

                # Increment Papa's wins in each trimester based on the first number in the line
                trimester_1_wins["Papa"] += int(line.split()[1])
                trimester_2_wins["Papa"] += int(line.split()[2])
                trimester_3_wins["Papa"] += int(line.split()[3])
                total_trimester_wins["Papa"] += int(line.split()[1]) + int(line.split()[2]) + int(line.split()[3])
            
            elif "HH" in line:
                # Increment HH's wins in each trimester based on the first number in the line
                trimester_1_wins["HH"] += int(line.split()[1])
                trimester_2_wins["HH"] += int(line.split()[2])
                trimester_3_wins["HH"] += int(line.split()[3])
                total_trimester_wins["HH"] += int(line.split()[1]) + int(line.split()[2]) + int(line.split()[3])
            
            elif "RR" in line:
                # Increment RR's wins in each trimester based on the first number in the line
                trimester_1_wins["RR"] += int(line.split()[1])
                trimester_2_wins["RR"] += int(line.split()[2])
                trimester_3_wins["RR"] += int(line.split()[3])
                total_trimester_wins["RR"] += int(line.split()[1]) + int(line.split()[2]) + int(line.split()[3])
    
    total_trimesters_played = sum(total_trimester_wins.values())
    print("\nTotal trimesters played:", total_trimesters_played)

    print("\nTotal trimester wins:")
    for player, wins in total_trimester_wins.items():
        print(f"{player}: {wins}")

    total_trimester_1_wins = sum(trimester_1_wins.values())
    total_trimester_2_wins = sum(trimester_2_wins.values())
    total_trimester_3_wins = sum(trimester_3_wins.values())

    # Print trimester wins
    print("\nTrimester 1 wins:")
    for player, wins in trimester_1_wins.items():
        print(f"{player}: {wins}")
        # calculate and print percentage of wins for each player in trimester 1
        if total_trimesters_played > 0:
            percentage = (wins / total_trimester_1_wins) * 100
            print(f"{player} win percentage in trimester 1: {percentage:.2f}%")
    
    print("\nTrimester 2 wins:")
    for player, wins in trimester_2_wins.items():
        print(f"{player}: {wins}")
        # calculate and print percentage of wins for each player in trimester 2
        if total_trimesters_played > 0:
            percentage = (wins / total_trimester_2_wins) * 100
            print(f"{player} win percentage in trimester 2: {percentage:.2f}%")
    
    print("\nTrimester 3 wins:")
    for player, wins in trimester_3_wins.items():
        print(f"{player}: {wins}")
        # calculate and print percentage of wins for each player in trimester 3
        if total_trimesters_played > 0:
            percentage = (wins / total_trimester_3_wins) * 100
            print(f"{player} win percentage in trimester 3: {percentage:.2f}%")
    

main()
