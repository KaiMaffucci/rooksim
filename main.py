from game_logic import *

def main():

    
    game = Game()

    # play 100 games while recording the winner of each game in a text file
    for i in range(100):
        game.run()


    """
    # test code
    game.deal()

    # testing each player's bidding strategy to make sure the numbers make sense
    game.all_bid()
    print(game.p1, game.p1.max_bid)
    print(game.p2, game.p2.max_bid)
    print(game.p3, game.p3.max_bid)
    print(game.p4, game.p4.max_bid)
    """

main()