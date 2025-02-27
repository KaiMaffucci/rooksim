from game_logic import *

def main():

    
    game = Game()

    # test code
    game.deal()
    print(game.p1.hand)
    print(game.p2.hand)
    print(game.p3.hand)
    print(game.p4.hand)
    print(game.nest)

main()