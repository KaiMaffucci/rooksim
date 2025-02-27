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

calculate how many holes are in a hand -> part of bidding

may need benchmarking

"""


import random


# game class
class Game:

    def __init__(self):

        # later will specify certain characters
        # assume 1 & 3 will be partners, 2 & 4 will be partners
        # TODO: randomly assign them one of four unique characters
        self.p1 = Player()
        self.p2 = Player()
        self.p3 = Player()
        self.p4 = Player()

        self.nest = [] # cards in the nest/kiddy
        self.current_trick = [] # cards in the current trick
        self.leading_suit = '' # suit of the first card played in a trick
        self.leading_player = 0 # 1-4, which player will lead the next trick
        self.winning_bid = 0 # the highest bid made by a player
        self.trump = '' # the trump suit for the round


    # deals starting hand and assigns partners
    # TODO: write test cases
    def deal(self):
        
        # Rook deck
        # has 57-16=41 cards, 4 suits of 14 cards each, 1 rook
        # suits are red, green, yellow, black
        deck = []
        for i in range(5, 15):
            deck.append('R' + str(i))
            deck.append('G' + str(i))
            deck.append('Y' + str(i))
            deck.append('B' + str(i))
        deck.append('X')

        # shuffle deck
        random.shuffle(deck)

        # deal cards to each player
        for i in range(0, 9):
            self.p1.hand.append(deck.pop())
            self.p2.hand.append(deck.pop())
            self.p3.hand.append(deck.pop())
            self.p4.hand.append(deck.pop())
        
        # deal cards to the nest
        for i in range(0, 5):
            self.nest.append(deck.pop())
        
        # TODO: move this?
        # determine partners
        # p1 and p3 are partners
        self.p1.partner = 3
        self.p3.partner = 1
        # p2 and p4 are partners
        self.p2.partner = 4
        self.p4.partner = 2

    # make players bid (TODO)
    def all_bid(self):
        
        # bid loop until all players have passed
        while self.p1.passing == False or self.p2.passing == False or self.p3.passing == False or self.p4.passing == False:
            # player 1 bids
            self.p1.bid()
            # player 2 bids
            self.p2.bid()
            # player 3 bids
            self.p3.bid()
            # player 4 bids
            self.p4.bid()
        
        # determine the winning bid
        self.winning_bid = max(self.p1.current_bid, self.p2.current_bid, self.p3.current_bid, self.p4.current_bid)

        # TODO: determine the trump suit

        # TODO: need method(?) for nest setup, before round starts

    # play a single trick
    def play_trick(self):
        pass

    # play a single round
    def play_round(self):
        
        # deal cards to each player
        self.deal()

        # players bid
        self.all_bid()

        # play tricks until all players are out of cards
        while len(self.player1.hand) > 0:
            self.play_trick()
        
        # TODO: determine how many points are in each player's taken tricks
        
        # TODO: if the highest bid was met, add the points to the team's score
        # if not, subtract the points from the team's score


    # run whole game
    def run(self):
        
        # while none of the players' scores are 300 or more, play another round
        while self.p1.score < 300 and self.p2.score < 300 and self.p3.score < 300 and self.p4.score < 300:
            self.play_round()
        
        # determine the winner
        # TODO: work on better data storage/output
        if self.p1.score >= 300:
            print("Player 1 wins!")
        elif self.p2.score >= 300:
            print("Player 2 wins!")
        elif self.p3.score >= 300:
            print("Player 3 wins!")
        elif self.p4.score >= 300:
            print("Player 4 wins!")
        else:
            print("Error: no winner found")


# player class
class Player:

    def __init__(self):

        self.score = 0          # everyone starts at 0 points
        self.hand = []          # empty hand, deck hasnt been dealt yet
        self.taken = []         # no tricks taken yet
        self.pts_taken = 0      # no points from tricks calculated yet
        self.current_bid = 0    # no bid started yet
        self.partner = 0        # partner undeclared
        self.passing = False    # whether the player is passing on bidding yet (for bidding phase, starts as false)

    # player methods for playing the game
    def bid():
        pass

    # play the card in a trick
    def card():
        pass


# Hideous Hog: aggressive but skilled
class HH(Player):

    # player methods for playing the game
    def bid():
        pass

    # play the card in a trick
    def card():
        pass


# Papa Greek: moderate player, tries to be optimal but this often makes him unlucky
class Greek(Player):

    # player methods for playing the game
    def bid():
        pass

    # play the card in a trick
    def card():
        pass


# Karapet: cautious, not a risk taker, looks to minimize loss moreso
class Karapet(Player):

    # player methods for playing the game
    def bid():
        pass

    # play the card in a trick
    def card():
        pass


# Rueful Rabbit: wildcard, plays bad but still wins (last to be programmed)
class RR(Player):

    # player methods for playing the game
    def bid():
        pass

    # play the card in a trick
    def card():
        pass
