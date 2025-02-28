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
        
        self.p1 = Player()
        self.p2 = Player()
        self.p3 = Player()
        self.p4 = Player()

        # randomly choose player 1 to be Karapet or Greek. 2 will be the other
        if random.randint(1, 2) == 1:
            self.p1 = Karapet()
            self.p2 = Papa()
        else:
            self.p1 = Papa()
            self.p2 = Karapet()

        # randomly choose player 3 to be HH or RR. 4 will be the other
        if random.randint(1, 2) == 1:
            self.p3 = HH()
            self.p4 = RR()
        else:
            self.p3 = RR()
            self.p4 = HH() 


        self.nest = [] # cards in the nest/kiddy
        self.current_trick = [] # cards in the current trick
        self.leading_suit = '' # suit of the first card played in a trick
        self.bid_winner = 0     # player who won the bid
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
        deck.append('XXX') # rook

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

    # make players bid
    def all_bid(self):
        
        # bid loop until all players have passed
        while not (self.p1.passing and self.p2.passing and self.p3.passing and self.p4.passing):
            # player 1 bids
            self.p1.bid()
            # player 2 bids
            self.p2.bid()
            # player 3 bids
            self.p3.bid()
            # player 4 bids
            self.p4.bid()
        
        # determine the winning bid and bidder
        self.winning_bid = max(self.p1.current_bid, self.p2.current_bid, self.p3.current_bid, self.p4.current_bid)
        if self.p1.current_bid == self.winning_bid:
            self.bid_winner = 1
        elif self.p2.current_bid == self.winning_bid:
            self.bid_winner = 2
        elif self.p3.current_bid == self.winning_bid:
            self.bid_winner = 3
        elif self.p4.current_bid == self.winning_bid:
            self.bid_winner = 4
        else:
            print("Error: no bid winner found") # should never run

    # TODO: need method(?) for nest setup, before round starts
    def setup_nest(self):
        
        # whoever won the bid gets to take the nest (TODO: if a player gets the nest, they should also put 5 cards back)
        # if the bid winner is 1, they get the nest
        if self.bid_winner == 1:
            self.p1.hand.extend(self.nest)
        # if the bid winner is 2, they get the nest
        elif self.bid_winner == 2:
            self.p2.hand.extend(self.nest)
        # if the bid winner is 3, they get the nest
        elif self.bid_winner == 3:
            self.p3.hand.extend(self.nest)
        # if the bid winner is 4, they get the nest
        elif self.bid_winner == 4:
            self.p4.hand.extend(self.nest)
        else:
            print("Error: no bid winner found") # should never run
        
        # clear the nest
        self.nest = []


    # play a single trick
    def play_trick(self):
        pass

    # play a single round
    def play_round(self):
        
        # deal cards to each player
        self.deal()

        # players bid
        self.all_bid()

        # setup the nest
        self.setup_nest()

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

        self.partner = 0        # partner undeclared
        self.max_bid = 35        # no max bid (maximum amount the player is willing to bid) declared yet
        self.current_bid = 0    # no bid started yet
        self.pref_trump = ''    # no preferred trump suit declared yet
        self.score = 0          # everyone starts at 0 points
        self.hand = []          # empty hand, deck hasnt been dealt yet
        self.taken = []         # no tricks taken yet
        self.pts_taken = 0      # no points from tricks calculated yet
        self.passing = False    # whether the player is passing on bidding yet (for bidding phase, starts as false)

    # calculate the preferred trump suit
    def calc_trump(self):

        # get number of cards in each color
        # this will be the preferred trump suit
        # note: this is a very simplistic way of looking at things and will likely change
        red = 0
        green = 0
        yellow = 0
        black = 0
        for card in self.hand:
            if card[0] == 'R':
                red += int(card[1:])
            elif card[0] == 'G':
                green += int(card[1:])
            elif card[0] == 'Y':
                yellow += int(card[1:])
            elif card[0] == 'B':
                black += int(card[1:])
        # determine the preferred trump suit
        if red >= green and red >= yellow and red >= black:
            self.pref_trump = 'R'
        elif green >= red and green >= yellow and green >= black:
            self.pref_trump = 'G'
        elif yellow >= red and yellow >= green and yellow >= black:
            self.pref_trump = 'Y'
        elif black >= red and black >= green and black >= yellow:
            self.pref_trump = 'B'
        else:
            # if there is a tie, add up the numbers of the cards in each suit
            # and choose the suit with the highest total
            red_total = 0
            green_total = 0
            yellow_total = 0
            black_total = 0
            for card in self.hand:
                if card[0] == 'R':
                    red_total += int(card[1:])
                elif card[0] == 'G':
                    green_total += int(card[1:])
                elif card[0] == 'Y':
                    yellow_total += int(card[1:])
                elif card[0] == 'B':
                    black_total += int(card[1:])
            if red_total >= green_total and red_total >= yellow_total and red_total >= black_total:
                self.pref_trump = 'R'
            elif green_total >= red_total and green_total >= yellow_total and green_total >= black_total:
                self.pref_trump = 'G'
            elif yellow_total >= red_total and yellow_total >= green_total and yellow_total >= black_total:
                self.pref_trump = 'Y'
            elif black_total >= red_total and black_total >= green_total and black_total >= yellow_total:
                self.pref_trump = 'B'

    # player methods for playing the game
    def bid(self):
        
        # if no bid has been determined yet, calculate maximum bid
        # otherwise, bid up unless it would exceed the max bid
        if self.current_bid == 0:
            self.calculate_max_bid()
            self.current_bid = 70
        else:
            if self.current_bid + 5 <= self.max_bid and self.current_bid + 5 <= 120:
                self.current_bid += 5
            else:
                self.passing = True

    # play the card in a trick
    # this method will also (likely) be overridden
    def card(self):
        pass


# Karapet: cautious, not a risk taker, looks to minimize loss moreso
class Karapet(Player):

    # calculate maximum bid
    # this player will bid cautiously
    def calculate_max_bid(self):
        
        self.calc_trump()

        # determine number of 14s in hand and add 10 for each
        self.max_bid += (self.hand.count('R14') + self.hand.count('G14') + self.hand.count('Y14') + self.hand.count('B14')) * 10
        # determine the number of 11-13s in hand and add 5 for each
        self.max_bid += (self.hand.count('R11') + self.hand.count('G11') + self.hand.count('Y11') + self.hand.count('B11')) * 5
        self.max_bid += (self.hand.count('R12') + self.hand.count('G12') + self.hand.count('Y12') + self.hand.count('B12')) * 5
        self.max_bid += (self.hand.count('R13') + self.hand.count('G13') + self.hand.count('Y13') + self.hand.count('B13')) * 5
        # determine the number of 10s in hand and add 10 for each
        self.max_bid += (self.hand.count('R10') + self.hand.count('G10') + self.hand.count('Y10') + self.hand.count('B10')) * 10
        # we will NOT be adding any for any other tricks, because Karapet is cautious and will not bid high
        # if Karapet has a rook, add 20
        if 'XXX' in self.hand:
            self.max_bid += 20

    def choose_nest(self):

        # Karapet will reserve the five lowest non-trump and non-5 cards for the nest
        cards_for_nest = []
        # find the lowest card 5 times, but skip over 5s and trump cards
        for i in range(0, 5):
            lowest = 'R15'
            for card in self.hand:
                if card[0] != self.pref_trump and card[1:] != '5' and card[1:] < lowest[1:]:
                    lowest = card
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)
        return cards_for_nest
        
    # play the card in a trick
    def card():
        pass


# Papa Greek: moderate player, tries to be optimal but this often makes him unlucky
class Papa(Player):

    # calculate maximum bid
    # this player will bid moderately
    def calculate_max_bid(self):
        
        self.calc_trump()

        # determine number of 14s in hand and add 10 for each
        self.max_bid += (self.hand.count('R14') + self.hand.count('G14') + self.hand.count('Y14') + self.hand.count('B14')) * 10
        # determine the number of 11-13s in hand and add 5 for each
        self.max_bid += (self.hand.count('R11') + self.hand.count('G11') + self.hand.count('Y11') + self.hand.count('B11')) * 5
        self.max_bid += (self.hand.count('R12') + self.hand.count('G12') + self.hand.count('Y12') + self.hand.count('B12')) * 5
        self.max_bid += (self.hand.count('R13') + self.hand.count('G13') + self.hand.count('Y13') + self.hand.count('B13')) * 5
        # determine the number of 10s in hand and add 10 for each
        self.max_bid += (self.hand.count('R10') + self.hand.count('G10') + self.hand.count('Y10') + self.hand.count('B10')) * 10
        # determine the number of 5-9s of trump color in hand, but save number because we will do math differently this time
        num_5_9_trump = 0
        for card in self.hand:
            if card[0] == self.pref_trump:
                if int(card[1:]) >= 5 and int(card[1:]) <= 9:
                    num_5_9_trump += 1
        # for every 2 5-9s in trump, add 5
        self.max_bid += (num_5_9_trump // 2) * 5
        # if Papa has a rook, add 20
        if 'XXX' in self.hand:
            self.max_bid += 20

    def choose_nest(self):

        # Papa will put in lowest cards not in trump suit
        cards_for_nest = []
        # find the lowest card 5 times, but skip over trump cards
        for i in range(0, 5):
            lowest = 'R15'
            for card in self.hand:
                if card[0] != self.pref_trump and card[1:] < lowest[1:]:
                    lowest = card
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)
        return cards_for_nest

    # play the card in a trick
    def card():
        pass


# Hideous Hog: aggressive but skilled
# this one may see revisions
class HH(Player):

    # calculate maximum bid
    # this player will bid aggressively
    def calculate_max_bid(self):

        self.calc_trump()

        # determine number of 14s in hand and add 10 for each
        self.max_bid += (self.hand.count('R14') + self.hand.count('G14') + self.hand.count('Y14') + self.hand.count('B14')) * 10
        # determine the number of 11-13s in hand and add 5 for each
        self.max_bid += (self.hand.count('R11') + self.hand.count('G11') + self.hand.count('Y11') + self.hand.count('B11')) * 5
        self.max_bid += (self.hand.count('R12') + self.hand.count('G12') + self.hand.count('Y12') + self.hand.count('B12')) * 5
        self.max_bid += (self.hand.count('R13') + self.hand.count('G13') + self.hand.count('Y13') + self.hand.count('B13')) * 5
        # determine the number of 10s in hand and add 10 for each
        self.max_bid += (self.hand.count('R10') + self.hand.count('G10') + self.hand.count('Y10') + self.hand.count('B10')) * 10
        # determine the number of 5-9s of trump in hand and add 5 for each (HH is a narcissist and thinks he can win with anything)
        for card in self.hand:
            if card[0] == self.pref_trump:
                if int(card[1:]) >= 5 and int(card[1:]) <= 9:
                    self.max_bid += 5
        # if HH has a rook, add 20
        if 'XXX' in self.hand:
            self.max_bid += 20

    def choose_nest(self):

        # HH will prioritize 5s first (he thinks he's really skilled and will take the last trick)
        # but he won't prioritize 10s and 14s (he's not that stupid)
        cards_for_nest = []
        # add all the 5s to the nest
        for card in self.hand:
            if card[1:] == '5':
                cards_for_nest.append(card)
                self.hand.remove(card)
        # nest needs to have a length of 5, so add the lowest cards not in trump to the nest until it does
        while len(cards_for_nest) < 5:
            lowest = 'R15'
            for card in self.hand:
                if card[0] != self.pref_trump and card[1:] < lowest[1:]:
                    lowest = card
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)
        
        return cards_for_nest

    # play the card in a trick
    def card():
        pass


# Rueful Rabbit: wildcard, plays bad but still wins (last to be programmed)
class RR(Player):

    # calculate maximum bid
    # this player will bid unpredictably
    def calculate_max_bid(self):

        self.calc_trump()

        # determine number of 14s in hand and add 10 for each
        self.max_bid += (self.hand.count('R14') + self.hand.count('G14') + self.hand.count('Y14') + self.hand.count('B14')) * 10
        # determine the number of 11-13s in hand and add 5 for each
        self.max_bid += (self.hand.count('R11') + self.hand.count('G11') + self.hand.count('Y11') + self.hand.count('B11')) * 5
        self.max_bid += (self.hand.count('R12') + self.hand.count('G12') + self.hand.count('Y12') + self.hand.count('B12')) * 5
        self.max_bid += (self.hand.count('R13') + self.hand.count('G13') + self.hand.count('Y13') + self.hand.count('B13')) * 5
        # determine the number of 10s in hand and add 10 for each
        self.max_bid += (self.hand.count('R10') + self.hand.count('G10') + self.hand.count('Y10') + self.hand.count('B10')) * 10
        # add a random multiple of 5 between 0 and 25 (RR is unpredictable)
        self.max_bid += random.randint(0, 5) * 5
        # if RR has a rook, add 20
        if 'XXX' in self.hand:
            self.max_bid += 20

    def choose_nest(self):

        # RR puts in 5 random cards
        cards_for_nest = []
        for i in range(0, 5):
            card = random.choice(self.hand)
            cards_for_nest.append(card)
            self.hand.remove(card)
        return cards_for_nest

    # play the card in a trick
    def card():
        pass
