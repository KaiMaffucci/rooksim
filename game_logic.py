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

idea: "lowest()" and "highest()" functions for cards


TODO: put different characters into seperate files?

note: not just the hog will get a really low negative score, all players are capable apparently
"""

# created with assistance from GitHub copilot

import random
import math





# game class
class Game:

    def assign_characters(self):

        # Assign each player to a random position
        players = [Karapet(), Papa(), HH(), RR()]
        random.shuffle(players)
        self.p1 = players[0]
        self.p2 = players[1]
        self.p3 = players[2]
        self.p4 = players[3]

    def __init__(self):

        # counts how many games have been played
        self.games_played = 0
        # counts how many tricks have been played in the round
        self.tricks_played = 0

        # later will specify certain characters
        # assume 1 & 3 will be partners, 2 & 4 will be partners
        self.p1 = Player()
        self.p2 = Player()
        self.p3 = Player()
        self.p4 = Player()

        # make each player a specific character
        self.assign_characters()

        # determine partners
        # p1 and p3 are partners
        self.p1.partner = 3
        self.p3.partner = 1
        # p2 and p4 are partners
        self.p2.partner = 4
        self.p4.partner = 2

        self.nest = [] # cards in the nest/kiddy
        self.current_trick = [] # cards in the current trick
        self.leading_suit = '' # suit of the first card played in a trick
        self.bid_winner = 0     # player who won the bid
        self.leading_player = 0 # 1-4, which player will lead the next trick
        self.winning_bid = 0 # the highest bid made by a player
        self.trump = '' # the trump suit for the round

        # trimester wins of each character
        self.karapet_t1 = 0
        self.karapet_t2 = 0
        self.karapet_t3 = 0
        self.papa_t1 = 0
        self.papa_t2 = 0
        self.papa_t3 = 0
        self.hh_t1 = 0
        self.hh_t2 = 0
        self.hh_t3 = 0
        self.rr_t1 = 0
        self.rr_t2 = 0
        self.rr_t3 = 0

        # create text file which will store the winner of each game
        # if there's a file already, overwrite it
        self.winner_file = open("winner.txt", "w")
        self.winner_file.close()
        # open the file again in append mode
        self.winner_file = open("winner.txt", "a")
        # write which game it is to winner file
        self.winner_file.write("Game " + str(self.games_played) + "\n")

        # create text file which will store all the play-by-plays
        # if there's a file already, overwrite it
        self.plays_file = open("plays.txt", "w")
        self.plays_file.close()
        # open the file again in append mode
        self.plays_file = open("plays.txt", "a")
        # write which game it is to plays file
        self.plays_file.write("Game " + str(self.games_played) + "\n")


    # deals starting hand and assigns partners
    def deal(self):
        
        # Rook deck
        # has 57-16=41 cards, 4 suits of 14 cards each, 1 rook
        # suits are red, green, yellow, black
        deck = []
        for i in range(5, 10):
            # make sure that if the card is less than 10, it has a 0 in front of it
            deck.append('R0' + str(i))
            deck.append('G0' + str(i))
            deck.append('Y0' + str(i))
            deck.append('B0' + str(i))
        for i in range(10, 15):
            deck.append('R' + str(i))
            deck.append('G' + str(i))
            deck.append('Y' + str(i))
            deck.append('B' + str(i))
        deck.append('X20') # rook

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


    # make players bid
    def all_bid(self):
        
        # bid loop until exactly 3 players are passing
        while self.p1.passing + self.p2.passing + self.p3.passing + self.p4.passing < 3:
            # p1 bids
            if not self.p1.passing:
                self.p1.bid()
            # p2 bids
            if not self.p2.passing:
                self.p2.bid()
            # p3 bids
            if not self.p3.passing:
                self.p3.bid()
            # p4 bids
            if not self.p4.passing:
                self.p4.bid()

        # print everyone's bids (test code)
        #print("P1 bid:", self.p1.max_bid)
        #print("P2 bid:", self.p2.max_bid)
        #print("P3 bid:", self.p3.max_bid)
        #print("P4 bid:", self.p4.max_bid)

        # record the bids in the plays file
        self.plays_file.write("P1 " + self.p1.get_name() + " max bid: " + str(self.p1.max_bid) + "\n")
        self.plays_file.write("P2 " + self.p2.get_name() + " max bid: " + str(self.p2.max_bid) + "\n")
        self.plays_file.write("P3 " + self.p3.get_name() + " max bid: " + str(self.p3.max_bid) + "\n")
        self.plays_file.write("P4 " + self.p4.get_name() + " max bid: " + str(self.p4.max_bid) + "\n")

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

        # record winning bidder and bid in the plays file
        self.plays_file.write("Winning bidder: P" + str(self.bid_winner) + " " + str(self.winning_bid) + "\n")
        self.plays_file.write("-" * 50 + "\n")
    

    # method to setup the nest
    def setup_nest(self):

        # whoever won the bid gets to take the nest (TODO: if a player gets the nest, they should also put 5 cards back)
        # if the bid winner is 1, they get the nest
        # depending on the player, they will choose different cards to put in the nest
        if self.bid_winner == 1:
            self.p1.hand.extend(self.nest)
            self.nest = self.p1.choose_nest()
        # if the bid winner is 2, they get the nest
        elif self.bid_winner == 2:
            self.p2.hand.extend(self.nest)
            self.nest = self.p2.choose_nest()
        # if the bid winner is 3, they get the nest
        elif self.bid_winner == 3:
            self.p3.hand.extend(self.nest)
            self.nest = self.p3.choose_nest()
        # if the bid winner is 4, they get the nest
        elif self.bid_winner == 4:
            self.p4.hand.extend(self.nest)
            self.nest = self.p4.choose_nest()
        else:
            print("Error: no bid winner found") # should never run
        
        # make sure that all hand sizes are still the same
        if len(self.p1.hand) != len(self.p2.hand) or len(self.p1.hand) != len(self.p3.hand) or len(self.p1.hand) != len(self.p4.hand):
            print("Error: hand sizes differ at nest creation")
            # print player hand stuff (test code)
            print(type(self.p1), len(self.p1.hand), self.p1.hand)
            print(type(self.p2), len(self.p2.hand), self.p2.hand)
            print(type(self.p3), len(self.p3.hand), self.p3.hand)
            print(type(self.p4), len(self.p4.hand), self.p4.hand)
            # exit the program
            exit()


    # play a single trick
    def play_trick(self):

        self.leading_suit = '' # reset the leading suit

        # calculate which third of the game we're in
        trimester = self.tricks_played % 9
        if trimester == 0 or trimester == 1 or trimester == 2:
            trimester = 1
        elif trimester == 3 or trimester == 4 or trimester == 5:
            trimester = 2
        elif trimester == 6 or trimester == 7 or trimester == 8:
            trimester = 3

        # if it's the first trick of the game, p1 leads
        if self.leading_player == 0:
            self.leading_player = 1
        # if it's not the first trick, the player who won the last trick leads
        # otherwise, the player who won the last trick leads
        if self.leading_player == 1:
            # turn order is 1-2-3-4
            self.current_trick.append(self.p1.play_card(self.current_trick, self.leading_suit, self.trump))
            self.leading_suit = self.current_trick[0][0]
            self.current_trick.append(self.p2.play_card(self.current_trick, self.leading_suit, self.trump))
            self.current_trick.append(self.p3.play_card(self.current_trick, self.leading_suit, self.trump))
            self.current_trick.append(self.p4.play_card(self.current_trick, self.leading_suit, self.trump))
        elif self.leading_player == 2:
            # turn order is 2-3-4-1
            self.current_trick.append(self.p2.play_card(self.current_trick, self.leading_suit, self.trump))
            self.leading_suit = self.current_trick[0][0]
            self.current_trick.append(self.p3.play_card(self.current_trick, self.leading_suit, self.trump))
            self.current_trick.append(self.p4.play_card(self.current_trick, self.leading_suit, self.trump))
            # add to the beginning of the list this time
            self.current_trick.insert(0, self.p1.play_card(self.current_trick, self.leading_suit, self.trump))
        elif self.leading_player == 3:
            # turn order is 3-4-1-2
            self.current_trick.append(self.p3.play_card(self.current_trick, self.leading_suit, self.trump))
            self.leading_suit = self.current_trick[0][0]
            self.current_trick.append(self.p4.play_card(self.current_trick, self.leading_suit, self.trump))
            self.current_trick.insert(0, self.p1.play_card(self.current_trick, self.leading_suit, self.trump))
            self.current_trick.insert(1, self.p2.play_card(self.current_trick, self.leading_suit, self.trump))
        elif self.leading_player == 4:
            # turn order is 4-1-2-3
            self.current_trick.append(self.p4.play_card(self.current_trick, self.leading_suit, self.trump))
            self.leading_suit = self.current_trick[0][0]
            self.current_trick.insert(0, self.p1.play_card(self.current_trick, self.leading_suit, self.trump))
            self.current_trick.insert(1, self.p2.play_card(self.current_trick, self.leading_suit, self.trump))
            self.current_trick.insert(2, self.p3.play_card(self.current_trick, self.leading_suit, self.trump))
        else:
            print("Error: no leading player found") # should never run

        # if there is a None in the current trick, print an error message (this should never happen)
        if None in self.current_trick:
            print("Error: None in current trick")
            # print leading player
            print("Leading player:", self.leading_player)
            # print current trick (test code)
            print(self.current_trick)
            # print hand stuff
            print(type(self.p1), len(self.p1.hand), self.p1.hand)
            print(type(self.p2), len(self.p2.hand), self.p2.hand)
            print(type(self.p3), len(self.p3.hand), self.p3.hand)
            print(type(self.p4), len(self.p4.hand), self.p4.hand)
            # exit the program
            exit()

        # determine winner of the trick
        highest = 'R0'
        for card in self.current_trick:
            if  card == 'X20' or highest == 'X20':
                highest = 'X20'
            else:
                if card[0] == self.trump and card[1:] > highest[1:]:
                    highest = card
                elif card[0] == self.leading_suit and card[1:] > highest[1:]:
                    highest = card

        # give the winner of the trick the cards in the trick,
        # set them as the leading player for the next trick,
        # and add to their corresponding trimester win count (TODO: make this look a lot better)
        if self.current_trick[0] == highest:

            self.leading_player = 1
            self.p1.taken.extend(self.current_trick)
            # add to the corresponding character trimester win count based on what trimester it is
            if self.p1.get_name() == "Karapet":
                if trimester == 1:
                    self.karapet_t1 += 1
                elif trimester == 2:
                    self.karapet_t2 += 1
                elif trimester == 3:
                    self.karapet_t3 += 1
            elif self.p1.get_name() == "Papa":
                if trimester == 1:
                    self.papa_t1 += 1
                elif trimester == 2:
                    self.papa_t2 += 1
                elif trimester == 3:
                    self.papa_t3 += 1
            elif self.p1.get_name() == "HH":
                if trimester == 1:
                    self.hh_t1 += 1
                elif trimester == 2:
                    self.hh_t2 += 1
                elif trimester == 3:
                    self.hh_t3 += 1
            elif self.p1.get_name() == "RR":
                if trimester == 1:
                    self.rr_t1 += 1
                elif trimester == 2:
                    self.rr_t2 += 1
                elif trimester == 3:
                    self.rr_t3 += 1

        elif self.current_trick[1] == highest:

            self.leading_player = 2
            self.p2.taken.extend(self.current_trick)

            # TODO: add to the corresponding character trimester win count based on what trimester it is
            if self.p2.get_name() == "Karapet":
                if trimester == 1:
                    self.karapet_t1 += 1
                elif trimester == 2:
                    self.karapet_t2 += 1
                elif trimester == 3:
                    self.karapet_t3 += 1
            elif self.p2.get_name() == "Papa":
                if trimester == 1:
                    self.papa_t1 += 1
                elif trimester == 2:
                    self.papa_t2 += 1
                elif trimester == 3:
                    self.papa_t3 += 1
            elif self.p2.get_name() == "HH":
                if trimester == 1:
                    self.hh_t1 += 1
                elif trimester == 2:
                    self.hh_t2 += 1
                elif trimester == 3:
                    self.hh_t3 += 1
            elif self.p2.get_name() == "RR":
                if trimester == 1:
                    self.rr_t1 += 1
                elif trimester == 2:
                    self.rr_t2 += 1
                elif trimester == 3:
                    self.rr_t3 += 1

        elif self.current_trick[2] == highest:

            self.leading_player = 3
            self.p3.taken.extend(self.current_trick)

            # add to the corresponding character trimester win count based on what trimester it is
            if self.p3.get_name() == "Karapet":
                if trimester == 1:
                    self.karapet_t1 += 1
                elif trimester == 2:
                    self.karapet_t2 += 1
                elif trimester == 3:
                    self.karapet_t3 += 1
            elif self.p3.get_name() == "Papa":
                if trimester == 1:
                    self.papa_t1 += 1
                elif trimester == 2:
                    self.papa_t2 += 1
                elif trimester == 3:
                    self.papa_t3 += 1
            elif self.p3.get_name() == "HH":
                if trimester == 1:
                    self.hh_t1 += 1
                elif trimester == 2:
                    self.hh_t2 += 1
                elif trimester == 3:
                    self.hh_t3 += 1
            elif self.p3.get_name() == "RR":
                if trimester == 1:
                    self.rr_t1 += 1
                elif trimester == 2:
                    self.rr_t2 += 1
                elif trimester == 3:
                    self.rr_t3 += 1

        elif self.current_trick[3] == highest:

            self.leading_player = 4
            self.p4.taken.extend(self.current_trick)

            # add to the corresponding character trimester win count based on what trimester it is
            if self.p4.get_name() == "Karapet":
                if trimester == 1:
                    self.karapet_t1 += 1
                elif trimester == 2:
                    self.karapet_t2 += 1
                elif trimester == 3:
                    self.karapet_t3 += 1
            elif self.p4.get_name() == "Papa":
                if trimester == 1:
                    self.papa_t1 += 1
                elif trimester == 2:
                    self.papa_t2 += 1
                elif trimester == 3:
                    self.papa_t3 += 1
            elif self.p4.get_name() == "HH":
                if trimester == 1:
                    self.hh_t1 += 1
                elif trimester == 2:
                    self.hh_t2 += 1
                elif trimester == 3:
                    self.hh_t3 += 1
            elif self.p4.get_name() == "RR":
                if trimester == 1:
                    self.rr_t1 += 1
                elif trimester == 2:
                    self.rr_t2 += 1
                elif trimester == 3:
                    self.rr_t3 += 1

        else:
            print("Error: no winner found") # should never run

        # write each players' hand to the plays file
        self.plays_file.write("P1 hand: " + str(self.p1.hand) + "\n")
        self.plays_file.write("P2 hand: " + str(self.p2.hand) + "\n")
        self.plays_file.write("P3 hand: " + str(self.p3.hand) + "\n")
        self.plays_file.write("P4 hand: " + str(self.p4.hand) + "\n")

        # write the leader of the trick to the plays file
        self.plays_file.write("Leader: P" + str(self.leading_player) + "\n")
        # write the trick to the plays file
        self.plays_file.write("Trick " + str(self.tricks_played) + ": " + str(self.current_trick) + "\n")
        # write the winner of the trick to the plays file
        self.plays_file.write("Winner: P" + str(self.leading_player) + "\tTrimester: " + str(trimester) + "\n")

        self.plays_file.write("-" * 50 + "\n")

        # clear the cards in the current trick from the players' hands
        # note: it would be more efficient to do this in each player's play_card method, but this is easier for now
        for card in self.current_trick:
            if card in self.p1.hand:
                self.p1.hand.remove(card)
            if card in self.p2.hand:
                self.p2.hand.remove(card)
            if card in self.p3.hand:
                self.p3.hand.remove(card)
            if card in self.p4.hand:
                self.p4.hand.remove(card)

        # if hand sizes differ, print an error message
        if len(self.p1.hand) != len(self.p2.hand) or len(self.p1.hand) != len(self.p3.hand) or len(self.p1.hand) != len(self.p4.hand):
            print("Error: hand sizes differ")
            # print current trick (test code)
            print(self.current_trick)
            # print player hand stuff (test code)
            print(type(self.p1), len(self.p1.hand), self.p1.hand)
            print(type(self.p2), len(self.p2.hand), self.p2.hand)
            print(type(self.p3), len(self.p3.hand), self.p3.hand)
            print(type(self.p4), len(self.p4.hand), self.p4.hand)
            # exit the program
            exit()

        self.tricks_played += 1

        # clear the current trick
        self.current_trick = []


    # play a single round
    def play_round(self):
        
        # deal cards to each player
        self.deal()

        # players bid
        self.all_bid()

        # setup the nest
        self.setup_nest()

        # write the trump color to the plays file
        self.plays_file.write("Trump: " + self.trump + "\n")
        # write the nest to the plays file
        self.plays_file.write("Nest: " + str(self.nest) + "\n")

        # play tricks until all players are out of cards
        # we only have to check the length of one player because they should all have the same number of cards
        tricks_played = 0
        while len(self.p1.hand) > 0:
            self.play_trick()
            tricks_played += 1
            #print("Trick", tricks_played, "played")
        
        # winner of the last trick adds the nest to their taken cards
        if self.leading_player == 1:
            self.p1.taken.extend(self.nest)
        elif self.leading_player == 2:
            self.p2.taken.extend(self.nest)
        elif self.leading_player == 3:
            self.p3.taken.extend(self.nest)
        elif self.leading_player == 4:
            self.p4.taken.extend(self.nest)
        else:
            print("Error: no leading player found") # should never run

        # calculate points taken by each player
        # note: could move parts of this to next block of code to be slightly more efficient
        self.p1.pts_taken = 0
        self.p2.pts_taken = 0
        self.p3.pts_taken = 0
        self.p4.pts_taken = 0
        for card in self.p1.taken:
            if card[1:] == '5':
                self.p1.pts_taken += 5
            elif card[1:] == '10':
                self.p1.pts_taken += 10
            elif card[1:] == '14':
                self.p1.pts_taken += 10
        for card in self.p2.taken:
            if card[1:] == '5':
                self.p2.pts_taken += 5
            elif card[1:] == '10':
                self.p2.pts_taken += 10
            elif card[1:] == '14':
                self.p2.pts_taken += 10
        for card in self.p3.taken:
            if card[1:] == '5':
                self.p3.pts_taken += 5
            elif card[1:] == '10':
                self.p3.pts_taken += 10
            elif card[1:] == '14':
                self.p3.pts_taken += 10
        for card in self.p4.taken:
            if card[1:] == '5':
                self.p4.pts_taken += 5
            elif card[1:] == '10':
                self.p4.pts_taken += 10
            elif card[1:] == '14':
                self.p4.pts_taken += 10
        
        # if the team with the highest bid took at least as many points as they bid, they get the points
        # team that lost the bid just gets whatever points they took
        if self.bid_winner == 1 or self.bid_winner == 3:
            if self.p1.pts_taken + self.p3.pts_taken >= self.winning_bid:
                self.p1.score += self.p1.pts_taken + self.p3.pts_taken
                self.p3.score += self.p3.pts_taken + self.p1.pts_taken
            else:
                self.p1.score -= self.winning_bid
                self.p3.score -= self.winning_bid
            self.p2.score += self.p2.pts_taken + self.p4.pts_taken
            self.p4.score += self.p4.pts_taken + self.p2.pts_taken
        elif self.bid_winner == 2 or self.bid_winner == 4:
            if self.p2.pts_taken + self.p4.pts_taken >= self.winning_bid:
                self.p2.score += self.p2.pts_taken + self.p4.pts_taken
                self.p4.score += self.p4.pts_taken + self.p2.pts_taken
            else:
                self.p2.score -= self.winning_bid
                self.p4.score -= self.winning_bid
            self.p1.score += self.p1.pts_taken + self.p3.pts_taken
            self.p3.score += self.p3.pts_taken + self.p1.pts_taken
        else:
            print("Error: no bid winner found") # should never run
        
        # print each players' score (test code)
        #print("P1 ", type(self.p1), "score:", self.p1.score)
        #print("P2 score:" , type(self.p2), self.p2.score)
        #print("P3 score:", type(self.p3), self.p3.score)
        #print("P4 score:", type(self.p4), self.p4.score)
        #print("---------------------------------------------")

        # if any of the players' scores are -100000 or less, exit the program
        if self.p1.score <= -100000 or self.p2.score <= -100000 or self.p3.score <= -100000 or self.p4.score <= -100000:
            print("A player's score is -100000 or less! Let's put an end to this madness!")
            # write info to file
            self.winner_file.write("A player's score is -100000 or less! Let's put an end to this madness!\n")
            # write player scores to file
            self.winner_file.write("P1 " + str(type(self.p1)) + " score: " + str(self.p1.score) + "\n")
            self.winner_file.write("P2 " + str(type(self.p2)) + " score: " + str(self.p2.score) + "\n")
            self.winner_file.write("P3 " + str(type(self.p3)) + " score: " + str(self.p3.score) + "\n")
            self.winner_file.write("P4 " + str(type(self.p4)) + " score: " + str(self.p4.score) + "\n")
            # write player bids and player types to file
            self.winner_file.write("P1 " + str(type(self.p1)) + " bid: " + str(self.p1.max_bid) + "\n")
            self.winner_file.write("P2 " + str(type(self.p2)) + " bid: " + str(self.p2.max_bid) + "\n")
            self.winner_file.write("P3 " + str(type(self.p3)) + " bid: " + str(self.p3.max_bid) + "\n")
            self.winner_file.write("P4 " + str(type(self.p4)) + " bid: " + str(self.p4.max_bid) + "\n")
            # exit the program
            exit()

        # nuke almost everything for new round
        # TODO: this would probably be better calling a method to do this for us
        self.nest = []
        self.p1.hand = []
        self.p2.hand = []
        self.p3.hand = []
        self.p4.hand = []
        self.p1.taken = []
        self.p2.taken = []
        self.p3.taken = []
        self.p4.taken = []
        self.p1.pts_taken = 0
        self.p2.pts_taken = 0
        self.p3.pts_taken = 0
        self.p4.pts_taken = 0
        self.bid_winner = 0
        self.leading_player = 0
        self.winning_bid = 0
        self.trump = ''
        self.leading_suit = ''


    # run whole game
    def run(self):

        # while none of the players' scores are 300 or more, play another round
        while self.p1.score < 300 and self.p2.score < 300 and self.p3.score < 300 and self.p4.score < 300:
            self.play_round()
        
        # determine the winner and store which player(s) (Papa, RR, etc) won
        self.winner_file.write("This game\'s winners:\n")
        if self.p1.score >= 300:
            self.winner_file.write(self.p1.get_name() + "\n")
        if self.p2.score >= 300:
            self.winner_file.write(self.p2.get_name() + "\n")
        if self.p3.score >= 300:
            self.winner_file.write(self.p3.get_name() + "\n")
        if self.p4.score >= 300:
            self.winner_file.write(self.p4.get_name() + "\n")
        
        self.winner_file.write("-" * 50 + "\n")
        
        # nuke scores for new game
        self.p1.score = 0
        self.p2.score = 0
        self.p3.score = 0
        self.p4.score = 0

        # assign characters again for variety
        self.assign_characters()
    
    # close the files
    def end(self):
        
        # write trick trimester data to plays file
        self.plays_file.write("Trick trimester data:\n")
        self.plays_file.write("Karapet: " + str(self.karapet_t1) + " " + str(self.karapet_t2) + " " + str(self.karapet_t3) + "\n")
        self.plays_file.write("Papa: " + str(self.papa_t1) + " " + str(self.papa_t2) + " " + str(self.papa_t3) + "\n")
        self.plays_file.write("HH: " + str(self.hh_t1) + " " + str(self.hh_t2) + " " + str(self.hh_t3) + "\n")
        self.plays_file.write("RR: " + str(self.rr_t1) + " " + str(self.rr_t2) + " " + str(self.rr_t3) + "\n")
        
        # close files
        self.winner_file.close()
        self.plays_file.close()

# player class
class Player:

    def __init__(self):

        self.partner = 0        # partner undeclared
        self.max_bid = 25       # no max bid (maximum amount the player is willing to bid) declared yet
        self.current_bid = 0    # no bid started yet
        self.pref_trump = ''    # no preferred trump suit declared yet
        self.score = 0          # everyone starts at 0 points
        self.hand = []          # empty hand, deck hasnt been dealt yet
        self.taken = []         # no tricks taken yet
        self.pts_taken = 0      # no points from tricks calculated yet
        self.passing = False    # whether the player is passing on bidding yet (for bidding phase, starts as false)

    # helper function to get just the name from the class
    def get_name(self):
        return str(type(self)).split('.')[-1][:-2]

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
            else:
                # pick a random trump suit if there is still a tie
                self.pref_trump = random.choice(['R', 'G', 'Y', 'B'])

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


# TODO: during bidding, have each player determine the most trumps their partner has
# and bid based on that information

# combinations function
def C(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

# determine probability of a player having a certain number of trumps
# t = number of trumps left in deck
# u = number of trumps in player's hand
# n = number of cards left in deck
# h = number of cards in player's hand
def prob_trumps(t, u, n=27, h=9):
    return C(t, u) * C(n - t, h - u) / C(n, h)
   


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
        if 'X20' in self.hand:
            self.max_bid += 20
        
        # determine the total number of trumps (rooks count as trump) in hand
        trumps_in_hand = 0
        rook_in_hand = False
        for card in self.hand:
            if card[0] == self.pref_trump:
                trumps_in_hand += 1
            elif card == 'X20':
                trumps_in_hand += 1
                rook_in_hand = True
        
        # determine number of trumps left (not in hand)
        trumps_elsewhere = 9 - trumps_in_hand
        # if the rook isn't in the hand, count it as a trump elsewhere
        if not rook_in_hand:
            trumps_elsewhere += 1

        # for each number of trumps Karapet's partner could have, calculate the probability of that happening
        # until we find one that is above %50
        # then add 5 to Karapet's bid for each
        for i in range(1, trumps_elsewhere + 1):
            if prob_trumps(trumps_elsewhere, i) > 0.5:
                self.max_bid += 5 * i
                break

    def choose_nest(self):

        # Karapet will reserve the five lowest non-trump and non-5 cards for the nest
        cards_for_nest = []
        # find the lowest card 5 times, but skip over 5s and trump cards
        for i in range(0, 5):
            lowest = 'X20'
            for card in self.hand:
                if card[0] != self.pref_trump and card[1:] != '5' and card[1:] < lowest[1:]:
                    lowest = card
            # if there are no more non-5s and non-trump cards, add the lowest trump card
            if lowest == 'X20':
                for card in self.hand:
                    if card[0] == self.pref_trump and card[1:] < lowest[1:]:
                        lowest = card
            # add chosen card to nest and remove it from hand
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)

        return cards_for_nest
        
    # play the card in a trick
    # information the player needs: the current trick, the leading suit, the trump suit
    def play_card(self, trick, lead, trump):
        
        # if Karapet is the first to play in a trick, he will play his lowest card not in trump or a counter
        if len(trick) == 0:
            lowest = 'X20' # TODO: change this to the first card in their hand
            for card in self.hand:
                if card[0] == lead and card[0] != trump and card[1:] < lowest[1:] and card[1:] != '5' and card[1:] != '10' and card[1:] != '14':
                    lowest = card
            # if a card wasn't picked, play lowest counter in suit
            if lowest == 'X20':
                for card in self.hand:
                    if card[0] == lead and card[1:] < lowest[1:] and card[1:] != '5' and card[1:] != '10' and card[1:] != '14':
                        lowest = card
            # if a card wasn't picked, play lowest non-counter non-trump not in suit led
            if lowest == 'X20':
                for card in self.hand:
                    if card[0] != trump and card[1:] < lowest[1:] and card[1:] != '5' and card[1:] != '10' and card[1:] != '14':
                        lowest = card
            # if a card wasn't picked, play lowest non-counter trump
            if lowest == 'X20':
                for card in self.hand:
                    if card[0] == trump and card[1:] < lowest[1:]  and card[1:] != '5' and card[1:] != '10' and card[1:] != '14':
                        lowest = card
            # if a card wasn't picked, play lowest counter (that's what's left to be picekd from)
            if lowest == 'X20':
                for card in self.hand:
                    if card[1:] < lowest[1:]:
                        lowest = card
            return lowest
        
        # Karapet focuses on minimizing loss rather than winning, so he will play the lowest card in his hand
        # that is in the leading suit but not trump suit or a counter (5, 10, 14).
        if lead in [card[0] for card in self.hand]:
            for card in self.hand:
                if card[0] == lead and card[1:] != '5' and card[1:] != '10' and card[1:] != '14':
                    return card
            
            # if he only has counters in the leading suit, he will play his lowest counter.
            lowest = 'X20'
            for card in self.hand:
                if card[0] == lead and card[1:] < lowest[1:]:
                    lowest = card
            return lowest
        # if he has no cards in the leading suit, he will play his lowest card not in the leading suit.
        else:
            lowest = 'X20'
            for card in self.hand:
                if card[0] != lead and card[1:] < lowest[1:]:
                    lowest = card
            return lowest
        

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
        if 'X20' in self.hand:
            self.max_bid += 20
        
        # determine the total number of trumps (rooks count as trump) in hand
        trumps_in_hand = 0
        rook_in_hand = False
        for card in self.hand:
            if card[0] == self.pref_trump:
                trumps_in_hand += 1
            elif card == 'X20':
                trumps_in_hand += 1
                rook_in_hand = True
        
        # determine number of trumps left (not in hand)
        trumps_elsewhere = 9 - trumps_in_hand
        # if the rook isn't in the hand, count it as a trump elsewhere
        if not rook_in_hand:
            trumps_elsewhere += 1

        # for each number of trumps Papa's partner could have, calculate the probability of that happening
        # until we find one that is above %50
        # then add 5 to Papa's bid for each
        for i in range(1, trumps_elsewhere + 1):
            if prob_trumps(trumps_elsewhere, i) > 0.5:
                self.max_bid += 5 * i
                break

    def choose_nest(self):

        # Papa will put in lowest cards not in trump suit
        cards_for_nest = []
        # find the lowest card 5 times, but skip over trump cards
        for i in range(0, 5):
            lowest = 'X20'
            for card in self.hand:
                if card[0] != self.pref_trump and card[1:] < lowest[1:]:
                    lowest = card
            # if there are no more non-trump cards, add the lowest trump card
            if lowest == 'X20':
                for card in self.hand:
                    if card[0] == self.pref_trump and card[1:] < lowest[1:]:
                        lowest = card
            # add chosen card to nest and remove it from hand
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)
        return cards_for_nest

    # play the card in a trick
    # note: we do NOT need to delete the chosen card, this is done in another method
    def play_card(self, trick, lead, trump):

        # if Papa is leading the trick, he will play his highest card (this could probably be better, but it'll work for now)
        if len(trick) == 0:
            highest = 'R0'
            for card in self.hand:
                if card[1:] > highest[1:]:
                    highest = card
            return highest

        # Papa is different: he will look at the cards in the trick
        # and try to either minimize loss or maximize gain.
        
        # first, look for cards in the leading suit
        if lead in [card[0] for card in self.hand]:

            # get the highest card in the trick
            highest = 'R0'
            for card in trick:
                if card[0] == lead and card[1:] > highest[1:]:
                    highest = card
            # he will first try to play his lowest card that is higher than the highest card in the trick
            lowest = 'X20'
            for card in self.hand:
                if card[0] == lead and card[1:] > highest[1:] and card[1:] < lowest[1:]:
                    lowest = card
            if lowest != 'X20':
                return lowest
            # if he has no cards higher than the highest card in the trick, he will play his lowest card in the leading suit
            else:
                lowest = 'X20'
                for card in self.hand:
                    if card[0] == lead and card[1:] < lowest[1:]:
                        lowest = card
                return lowest
        # if he has no cards in the leading suit, he will play his highest trump
        elif trump in [card[0] for card in self.hand]:
            highest = 'R0'
            for card in self.hand:
                if card[0] == trump and card[1:] > highest[1:]:
                    highest = card
            return highest
        # if he has no cards in the leading suit or trump but he DOES have rook, he plays the rook
        elif 'X20' in self.hand:
            return 'X20'
        # if nothing else, he will play his lowest card in general
        else:

            # tries non-counters first
            lowest = 'X20'
            for card in self.hand:
                if card[0] != trump and card[1:] != '5' and card[1:] != '10' and card[1:] != '14' and card[1:] < lowest[1:]:
                    lowest = card

            # will pick lowest overall card if no non-counters are found
            if lowest == 'X20':
                for card in self.hand:
                    if card[1:] < lowest[1:]:
                        lowest = card
                
            return lowest



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
                    if random.randint(1, 2) == 1: self.max_bid += 5 # made it so he only adds it roughly half the time because he keeps bidding too high
        # if HH has a rook, add 20
        if 'X20' in self.hand:
            self.max_bid += 20
        
        # determine the total number of trumps (rooks count as trump) in hand
        trumps_in_hand = 0
        rook_in_hand = False
        for card in self.hand:
            if card[0] == self.pref_trump:
                trumps_in_hand += 1
            elif card == 'X20':
                trumps_in_hand += 1
                rook_in_hand = True
        
        # determine number of trumps left (not in hand)
        trumps_elsewhere = 9 - trumps_in_hand
        # if the rook isn't in the hand, count it as a trump elsewhere
        if not rook_in_hand:
            trumps_elsewhere += 1

        # for each number of trumps HH's partner could have, calculate the probability of that happening
        # until we find one that is above %50
        # then add 5 to HH's bid for each
        for i in range(1, trumps_elsewhere + 1):
            if prob_trumps(trumps_elsewhere, i) > 0.5:
                self.max_bid += 5 * i
                break

    def choose_nest(self):

        # HH will prioritize 5s first (he thinks he's really skilled and will take the last trick)
        # but he won't prioritize 10s and 14s (he's not that stupid)
        cards_for_nest = []
        # add all the 5s to the nest
        # TODO: make it so he will prioritize non-trump 5s first
        for card in self.hand:
            if card[0] != self.pref_trump and card[1:] == '5':
                cards_for_nest.append(card)
                self.hand.remove(card)
        # nest needs to have a length of 5, so add the lowest cards not in trump to the nest until it does
        while len(cards_for_nest) < 5:
            lowest = 'X20'
            for card in self.hand:
                if card[0] != self.pref_trump and card[1:] < lowest[1:]:
                    lowest = card
            # if there are no more non-trump cards, add the lowest trump card
            if lowest == 'X20':
                for card in self.hand:
                    if card[0] == self.pref_trump and card[1:] < lowest[1:]:
                        lowest = card
            # add chosen card to nest and remove it from hand
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)
        
        return cards_for_nest

    # play the card in a trick
    def play_card(self, trick, lead, trump):
        
        # if HH is the first to play in a trick, he will play his highest card
        if len(trick) == 0:
            highest = 'R0'
            for card in self.hand:
                if card[1:] > highest[1:]:
                    highest = card
            return highest

        # HH will play the highest card in his hand that is in the leading suit.
        # HH will slam the rook down if he has it.
        if 'X20' in self.hand:
            return 'X20'
        # if he has a card in the leading suit, he will play his highest card in that suit.
        elif lead in [card[0] for card in self.hand]:
            highest = 'R0'
            for card in self.hand:
                if card[0] == lead and card[1:] > highest[1:]:
                    highest = card
            return highest
        # if he has no cards in the leading suit, he will play his highest trump.
        elif trump in [card[0] for card in self.hand]:
            highest = 'R0'
            for card in self.hand:
                if card[0] == trump and card[1:] > highest[1:]:
                    highest = card
            return highest
        # if he has neither of these things, he will play his lowest card.
        else:
            lowest = 'X20'
            for card in self.hand:
                if card[1:] < lowest[1:] and card[1:] != '5' and card[1:] != '10' and card[1:] != '14':
                    lowest = card
            if lowest == 'X20':
                for card in self.hand:
                    if card[1:] < lowest[1:]:
                        lowest = card
            return lowest


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
        if 'X20' in self.hand:
            self.max_bid += 20
        
        # determine the total number of trumps (rooks count as trump) in hand
        trumps_in_hand = 0
        rook_in_hand = False
        for card in self.hand:
            if card[0] == self.pref_trump:
                trumps_in_hand += 1
            elif card == 'X20':
                trumps_in_hand += 1
                rook_in_hand = True
        
        # determine number of trumps left (not in hand)
        trumps_elsewhere = 9 - trumps_in_hand
        # if the rook isn't in the hand, count it as a trump elsewhere
        if not rook_in_hand:
            trumps_elsewhere += 1

        # for each number of trumps RR's partner could have, calculate the probability of that happening
        # until we find one that is above %50
        # then add 5 to RR's bid for each
        for i in range(1, trumps_elsewhere + 1):
            if prob_trumps(trumps_elsewhere, i) > 0.5:
                self.max_bid += 5 * i
                break

    def choose_nest(self):

        # RR puts in 5 random cards
        cards_for_nest = []
        for i in range(0, 5):
            card = random.choice(self.hand)
            cards_for_nest.append(card)
            self.hand.remove(card)
        return cards_for_nest

    # play the card in a trick
    def play_card(self, trick, lead, trump):
        
        # if RR is the first to play in a trick, he will play a random card
        if len(trick) == 0:
            return random.choice(self.hand)

        # RR will randomly pick from any of the other players' strategies
        choice = random.randint(1, 3)
        if choice == 1:
            return Karapet.play_card(self, trick, lead, trump)
        elif choice == 2:
            return Papa.play_card(self, trick, lead, trump)
        elif choice == 3:
            return HH.play_card(self, trick, lead, trump)
