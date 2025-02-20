"""
general notes
-----------------------------------

game class, contains:
    players 1-4
    methods for playing the game - both setup (such as bidding) and taking tricks. write the needed methods by going through the order the game is played

player class contains:
    hand - list of strings
    tricks taken - list of strings
    methods for changing hand (note: each card is unique, this will make it easier to remove cards from hands)
    needs some way to keep track of who's the partner

    different characters will be utilized: Greek, Karapat, RR, HH probably, will have to see others from book first though

four colors: R G Y B
four numbers: 5-14
special cards: X (rook)
card examples: R12, G7, Y5, B14

deck const?

make sure to output stuff to file
"""

# game class
class Game:

    def __init__(self):

        # later will specify certain characters
        self.player1 = Player()
        self.player2 = Player()
        self.player3 = Player()
        self.player4 = Player()
        self.winning_mid = 0
        current_trick = []

    # TODO: need methods for gameplay

    # deals starting hand
    def deal():
        pass

    # make players bid
    def all_bid():
        pass

    # play a single trick
    def play_trick():
        pass

    # run whole game
    def run():
        pass


# player class
class Player:

    def __init__(self):

        self.hand = []          # empty hand, deck hasnt been dealt yet
        self.taken = []         # no tricks taken yet
        self.current_bid = 0    # no bid started yet
        self.partner = 0        # partner undeclared

    # player methods for playing the game
    def bid():
        pass

    # play the card in a trick
    def play():
        pass


# different characters will be their own child classes