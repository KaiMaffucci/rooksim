"""
Rook Game Simulation
Made with assistance from Github Copilot 

Game class:
    - Manages players, game flow, bidding, tricks, and scoring.
    - Handles file output for results and play-by-play.

Player class:
    - Represents a player with hand, tricks taken, and partner.
    - Subclasses for different character behaviors.

Card format: [Suit][Number], e.g., R12, G7, Y5, B14, X20 (rook).
"""

import random
import math

random.seed(69)

COUNTER_RANKS = ('5', '10', '14', '20')  # Counter cards in Rook

# Utility functions
# n choose r
def C(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

# Probability of t trumps in u draws from n total cards with h trumps
def prob_trumps(t, u, n=27, h=9):
    return C(t, u) * C(n - t, h - u) / C(n, h)

# Player base class
class Player:

    def __init__(self):
        # All essential attributes for a player
        self.partner = 0
        self.max_bid = 25
        self.current_bid = 0
        self.pref_trump = ''
        self.score = 0
        self.hand = []
        self.taken = []
        self.pts_taken = 0
        self.passing = False

    # Returns the name of the player class
    def get_name(self):
        return type(self).__name__

    # Calculates the trump suit based on the player's hand
    def calc_trump(self):
        suit_totals = {'R': 0, 'G': 0, 'Y': 0, 'B': 0}
        for card in self.hand:
            if card[0] in suit_totals:
                suit_totals[card[0]] += int(card[1:])
        self.pref_trump = max(suit_totals, key=lambda k: (suit_totals[k], random.random()))

    # Algorithm for bidding process
    def bid(self):
        if self.current_bid == 0:
            self.calculate_max_bid()
            self.current_bid = 70
        else:
            if self.current_bid + 5 <= self.max_bid and self.current_bid + 5 <= 120:
                self.current_bid += 5
            else:
                self.passing = True

# Character classes

# Karapet, a more conservative player
class Karapet(Player):

    # Karapet's method of calculating the maximum bid
    def calculate_max_bid(self):

        # Calculate the preferred trump suit based on the hand
        self.calc_trump()
        # Add points for high cards in trump suit in hand
        self.max_bid += sum(self.hand.count(f"{suit}{num}") * val
                            for suit in 'RGYB'
                            for num, val in [('14', 10), ('11', 5), ('12', 5), ('13', 5), ('10', 10)])
        
        if 'X20' in self.hand:
            self.max_bid += 20
        
        # Add points for 5-9 cards in trump suit
        num_5_9_trump = sum(1 for c in self.hand if c[0] == self.pref_trump and 5 <= int(c[1:]) <= 9)
        self.max_bid += (num_5_9_trump // 2) * 5

        # Add points to bid based on number of trumps elsewhere
        trumps_in_hand = sum(1 for card in self.hand if card[0] == self.pref_trump or card == 'X20')
        trumps_elsewhere = 9 - trumps_in_hand + (0 if 'X20' in self.hand else 1)
        for i in range(1, trumps_elsewhere + 1):
            if prob_trumps(trumps_elsewhere, i) > 0.5:
                self.max_bid += 5 * i
                break

    # Karapet's method of choosing cards for the nest
    def choose_nest(self):
        cards_for_nest = []
        for _ in range(5):
            non_trump_non_5 = [c for c in self.hand if c[0] != self.pref_trump and c[1:] != '5']
            candidates = non_trump_non_5 or [c for c in self.hand if c[0] == self.pref_trump] or self.hand
            lowest = min(candidates, key=lambda x: int(x[1:]))
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)
        return cards_for_nest

    # Karapet's method of choosing a card to play
    def play_card(self, trick, lead, trump):

        # If trick is empty (Karapet is leading)
        if not trick:

            # 1. Tries to play the lowest non-trump, non-counter card
            non_trump_non_counter = [c for c in self.hand if c[0] != trump and c[1:] not in COUNTER_RANKS]
            if non_trump_non_counter:
                return min(non_trump_non_counter, key=lambda x: int(x[1:]))
            non_counter = [c for c in self.hand if c[1:] not in COUNTER_RANKS]
            
            # 2. If there are no non-trump, non-counter cards, play the lowest non-counter card
            if non_counter:
                return min(non_counter, key=lambda x: int(x[1:]))
            
            # 3. If no non-counter cards, play the lowest trump card
            trump_cards = [c for c in self.hand if c[0] == trump]
            if trump_cards:
                return min(trump_cards, key=lambda x: int(x[1:]))
            
            # 4. If no trumps, play the lowest card in hand
            return min(self.hand, key=lambda x: int(x[1:]))
        
        # If Karapet is not leading, play a card based on the lead suit
        else:

            # 1. Play the lowest non-counter card of the lead suit if available
            lead_cards = [c for c in self.hand if c[0] == lead and c[1:] not in COUNTER_RANKS]
            if lead_cards:
                return min(lead_cards, key=lambda x: int(x[1:]))

            # 2. If no non-counter lead cards, play the lowest counter card of the lead suit
            lead_counters = [c for c in self.hand if c[0] == lead]
            if lead_counters:
                return min(lead_counters, key=lambda x: int(x[1:]))
            
            # 3. If no cards match leading suit, play the lowest non-counter, non-trump card
            non_trump_non_counter = [c for c in self.hand if c[0] != trump and c[1:] not in COUNTER_RANKS]
            if non_trump_non_counter:
                return min(non_trump_non_counter, key=lambda x: int(x[1:]))
            
            # 4. If no non-trump, non-counter cards, play lowest non-counter trump
            non_counter = [c for c in self.hand if c[1:] not in COUNTER_RANKS]
            if non_counter:
                return min(non_counter, key=lambda x: int(x[1:]))
            
            # 5. If no non-counter trumps, play lowest trump card (only counters available at this point)
            trump_cards = [c for c in self.hand if c[0] == trump]
            if trump_cards:
                return min(trump_cards, key=lambda x: int(x[1:]))
            
            # 6. If no trumps, play the lowest card in hand
            return min(self.hand, key=lambda x: int(x[1:]))

# Papa, a midrange player who plays more caculatedly
class Papa(Player):

    # Papa's method of calculating the maximum bid
    def calculate_max_bid(self):

        # Calculate the preferred trump suit based on the hand
        self.calc_trump()

        # Add points for high cards in trump suit in hand
        self.max_bid += sum(self.hand.count(f"{suit}{num}") * val
                            for suit in 'RGYB'
                            for num, val in [('14', 10), ('11', 5), ('12', 5), ('13', 5), ('10', 10)])
        # Add points for 5-9 cards in trump suit
        num_5_9_trump = sum(1 for c in self.hand if c[0] == self.pref_trump and 5 <= int(c[1:]) <= 9)
        self.max_bid += (num_5_9_trump // 2) * 5
        
        if 'X20' in self.hand:
            self.max_bid += 20

        # Add points to bid based on number of trumps elsewhere
        trumps_in_hand = sum(1 for card in self.hand if card[0] == self.pref_trump or card == 'X20')
        trumps_elsewhere = 9 - trumps_in_hand + (0 if 'X20' in self.hand else 1)
        for i in range(1, trumps_elsewhere + 1):
            if prob_trumps(trumps_elsewhere, i) > 0.5:
                self.max_bid += 5 * i
                break

    # Papa's method of choosing cards for the nest
    def choose_nest(self):

        cards_for_nest = []

        # Lowest 5 non-trump cards
        for _ in range(5):
            non_trump = [c for c in self.hand if c[0] != self.pref_trump]
            candidates = non_trump or [c for c in self.hand if c[0] == self.pref_trump] or self.hand
            lowest = min(candidates, key=lambda x: int(x[1:]))
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)

        return cards_for_nest

    # Papa's method of choosing a card to play
    def play_card(self, trick, lead, trump):

        # If Papa is leading, play highest card, regardless of suit
        if not trick:
            return max(self.hand, key=lambda x: int(x[1:]))

        else:
            # 1. Lowest lead card in hand that is still higher than the highest card in the trick
            lead_cards = [c for c in self.hand if c[0] == lead]
            if lead_cards:
                highest_in_trick = max((c for c in trick if c[0] == lead), default='R0', key=lambda x: int(x[1:]))
                higher = [c for c in lead_cards if int(c[1:]) > int(highest_in_trick[1:])]
                if higher:
                    return min(higher, key=lambda x: int(x[1:]))
                # 2. If no higher lead cards, play the lowest lead card
                return min(lead_cards, key=lambda x: int(x[1:]))
            
            # 3. If no lead cards, play highest trump card
            trump_cards = [c for c in self.hand if c[0] == trump]
            if trump_cards:
                return max(trump_cards, key=lambda x: int(x[1:]))
            
            # 4. If no trumps, play the Rook
            if 'X20' in self.hand:
                return 'X20'
            
            # 5. If no Rook, play the lowest non-counter card
            non_counter = [c for c in self.hand if c[0] != trump and c[1:] not in COUNTER_RANKS]
            if non_counter:
                return min(non_counter, key=lambda x: int(x[1:]))
            
            # 6. If no non-counter cards, play the lowest card in hand
            return min(self.hand, key=lambda x: int(x[1:]))

# HH (Hideous Hog), a very aggressive player
class HH(Player):

    # HH's method of calculating the maximum bid
    def calculate_max_bid(self):

        # Calculate the preferred trump suit based on the hand
        self.calc_trump()

        # Add points to bid for high cards in trump suit in hand
        self.max_bid += sum(self.hand.count(f"{suit}{num}") * val
                            for suit in 'RGYB'
                            for num, val in [('14', 10), ('11', 5), ('12', 5), ('13', 5), ('10', 10)])
        
        # Add points to bid for 5-9 cards in trump suit
        for c in self.hand:
            if c[0] == self.pref_trump and 5 <= int(c[1:]) <= 9 and random.randint(1, 2) == 1:
                self.max_bid += 5
        
        if 'X20' in self.hand:
            self.max_bid += 20

        trumps_in_hand = sum(1 for card in self.hand if card[0] == self.pref_trump or card == 'X20')
        trumps_elsewhere = 9 - trumps_in_hand + (0 if 'X20' in self.hand else 1)
        for i in range(1, trumps_elsewhere + 1):
            if prob_trumps(trumps_elsewhere, i) > 0.5:
                self.max_bid += 5 * i
                break

    # HH's method of choosing cards for the nest
    def choose_nest(self):

        cards_for_nest = []

        # Chooses as many 5s as possible, then fills with lowest cards
        for card in [c for c in self.hand if c[0] != self.pref_trump and c[1:] == '5']:
            cards_for_nest.append(card)
            self.hand.remove(card)
            if len(cards_for_nest) == 5:
                return cards_for_nest
        while len(cards_for_nest) < 5:
            non_trump = [c for c in self.hand if c[0] != self.pref_trump]
            candidates = non_trump or [c for c in self.hand if c[0] == self.pref_trump] or self.hand
            lowest = min(candidates, key=lambda x: int(x[1:]))
            cards_for_nest.append(lowest)
            self.hand.remove(lowest)
        
        return cards_for_nest

    # HH's method of choosing a card to play
    def play_card(self, trick, lead, trump):

        # If HH is leading, play the highest card in hand
        if not trick:
            return max(self.hand, key=lambda x: int(x[1:]))
        
        # 1. If HH is not leading, first he slams the Rook if he has it
        if 'X20' in self.hand:
            return 'X20'
        
        # 2. If HH is not leading, play the highest card of the lead suit
        lead_cards = [c for c in self.hand if c[0] == lead]
        if lead_cards:
            return max(lead_cards, key=lambda x: int(x[1:]))

        # 3. If no lead cards, play the highest trump card
        trump_cards = [c for c in self.hand if c[0] == trump]
        if trump_cards:
            return max(trump_cards, key=lambda x: int(x[1:]))
        
        # 4. If no trumps, play the lowest non-counter card
        non_counter = [c for c in self.hand if c[1:] not in COUNTER_RANKS]
        if non_counter:
            return min(non_counter, key=lambda x: int(x[1:]))
        
        # 5. If no non-counter cards, play the lowest card in hand
        return min(self.hand, key=lambda x: int(x[1:]))

# RR (Rueful Rabbit), an unpredictable player who stumbles into success every once in a while
class RR(Player):

    # RR's method of calculating the maximum bid
    def calculate_max_bid(self):

        # Calculate the preferred trump suit based on the hand
        self.calc_trump()

        # Add points to bid for high cards in trump suit in hand
        self.max_bid += sum(self.hand.count(f"{suit}{num}") * val
                            for suit in 'RGYB'
                            for num, val in [('14', 10), ('11', 5), ('12', 5), ('13', 5), ('10', 10)])
        
        self.max_bid += random.randint(0, 5) * 5
        
        if 'X20' in self.hand:
            self.max_bid += 20

        # Add points based on trumps elsewhere
        trumps_in_hand = sum(1 for card in self.hand if card[0] == self.pref_trump or card == 'X20')
        trumps_elsewhere = 9 - trumps_in_hand + (0 if 'X20' in self.hand else 1)
        for i in range(1, trumps_elsewhere + 1):
            if prob_trumps(trumps_elsewhere, i) > 0.5:
                self.max_bid += 5 * i
                break

    # RR's method of choosing cards for the nest
    def choose_nest(self):
        cards_for_nest = []
        for _ in range(5):
            card = random.choice(self.hand)
            cards_for_nest.append(card)
            self.hand.remove(card)
        return cards_for_nest

    # RR's method of choosing a card to play
    def play_card(self, trick, lead, trump):

        # If RR is leading, play a random card from hand
        if not trick:
            return random.choice(self.hand)
        
        # If RR is not leading, randomly pick another player's strategy
        choice = random.choice([Karapet, Papa, HH])
        return choice.play_card(self, trick, lead, trump) # fix type conflict?

# TODO: Add comments to the code below

# Game class
class Game:

    # Initializes the game with players, scores, and files for output
    def __init__(self):
        self.games_played = 0
        self.tricks_played = 0
        self.p1 = Player()
        self.p2 = Player()
        self.p3 = Player()
        self.p4 = Player()
        self.assign_characters()
        self.p1.partner, self.p3.partner = 3, 1
        self.p2.partner, self.p4.partner = 4, 2
        self.nest = []
        self.current_trick = []
        self.leading_suit = ''
        self.bid_winner = 0
        self.leading_player = 0
        self.winning_bid = 0
        self.trump = ''
        self.karapet_t1 = self.karapet_t2 = self.karapet_t3 = 0
        self.papa_t1 = self.papa_t2 = self.papa_t3 = 0
        self.hh_t1 = self.hh_t2 = self.hh_t3 = 0
        self.rr_t1 = self.rr_t2 = self.rr_t3 = 0
        with open("winners.txt", "w"), open("plays.txt", "w"):
            pass
        self.winner_file = open("winners.txt", "a")
        self.plays_file = open("plays.txt", "a")

    # Assigns character classes to players randomly
    def assign_characters(self):
        players = [Karapet(), Papa(), HH(), RR()]
        random.shuffle(players)
        self.p1, self.p2, self.p3, self.p4 = players

    # Deals cards to players and sets up the nest
    def deal(self):
        deck = [f"{suit}{str(i).zfill(2)}" for suit in 'RGYB' for i in range(5, 15)]
        deck.append('X20')
        random.shuffle(deck)
        for _ in range(9):
            self.p1.hand.append(deck.pop())
            self.p2.hand.append(deck.pop())
            self.p3.hand.append(deck.pop())
            self.p4.hand.append(deck.pop())
        self.nest = [deck.pop() for _ in range(5)]

    # Handles the bidding process where players bid until at least 3 pass
    def all_bid(self):
        while sum(p.passing for p in [self.p1, self.p2, self.p3, self.p4]) < 3:
            for p in [self.p1, self.p2, self.p3, self.p4]:
                if not p.passing:
                    p.bid()
        for idx, p in enumerate([self.p1, self.p2, self.p3, self.p4], 1):
            self.plays_file.write(f"P{idx} {p.get_name()} max bid: {p.max_bid}\n")
        bids = [self.p1.current_bid, self.p2.current_bid, self.p3.current_bid, self.p4.current_bid]
        self.winning_bid = max(bids)
        self.bid_winner = bids.index(self.winning_bid) + 1
        self.plays_file.write(f"Winning bidder: P{self.bid_winner} {self.winning_bid}\n{'-'*50}\n")

    # Sets up the nest based on the winning bidder's choice
    def setup_nest(self):
        winner = [self.p1, self.p2, self.p3, self.p4][self.bid_winner - 1]
        winner.hand.extend(self.nest)
        self.nest = winner.choose_nest()
        if len({len(self.p1.hand), len(self.p2.hand), len(self.p3.hand), len(self.p4.hand)}) != 1:
            print("Error: hand sizes differ at nest creation")
            for p in [self.p1, self.p2, self.p3, self.p4]:
                print(type(p), len(p.hand), p.hand)
            exit()

    # Plays a trick in the game
    def play_trick(self):

        self.leading_suit = ''
        trimester = (self.tricks_played % 9) // 3 + 1
        order = [self.p1, self.p2, self.p3, self.p4]
        idx = (self.leading_player - 1) % 4 if self.leading_player else 0
        trick = []
        for i in range(4):
            player = order[(idx + i) % 4]
            card = player.play_card(trick, self.leading_suit, self.trump)
            trick.append(card)
            if i == 0:
                self.leading_suit = card[0]
        self.current_trick = trick
        if None in trick:
            print("Error: None in current trick")
            print("Leading player:", self.leading_player)
            for p in [self.p1, self.p2, self.p3, self.p4]:
                print(type(p), len(p.hand), p.hand)
            exit()

        # Determine winner
        def card_value(card):
            if card == 'X20':
                return (2, 20)
            suit = card[0]
            num = int(card[1:])
            if suit == self.trump:
                return (1, num)
            if suit == self.leading_suit:
                return (0, num)
            return (-1, num)
        winner_idx = max(range(4), key=lambda i: card_value(trick[i]))
        self.leading_player = (idx + winner_idx) % 4 + 1
        winner = order[(idx + winner_idx) % 4]
        winner.taken.extend(trick)

        # Update trimester win counts
        name = winner.get_name()
        if name == "Karapet":
            setattr(self, f"karapet_t{trimester}", getattr(self, f"karapet_t{trimester}") + 1)
        elif name == "Papa":
            setattr(self, f"papa_t{trimester}", getattr(self, f"papa_t{trimester}") + 1)
        elif name == "HH":
            setattr(self, f"hh_t{trimester}", getattr(self, f"hh_t{trimester}") + 1)
        elif name == "RR":
            setattr(self, f"rr_t{trimester}", getattr(self, f"rr_t{trimester}") + 1)

        # Write to file
        for idx, p in enumerate([self.p1, self.p2, self.p3, self.p4], 1):
            self.plays_file.write(f"P{idx} hand: {p.hand}\n")
        self.plays_file.write(f"Leader: P{self.leading_player}\n")
        self.plays_file.write(f"Trick {self.tricks_played}: {trick}\n")
        self.plays_file.write(f"Winner: P{self.leading_player}\tTrimester: {trimester}\n{'-'*50}\n")
        
        # Remove cards from hands
        for card in trick:
            for p in [self.p1, self.p2, self.p3, self.p4]:
                if card in p.hand:
                    p.hand.remove(card)
        if len({len(self.p1.hand), len(self.p2.hand), len(self.p3.hand), len(self.p4.hand)}) != 1:
            print("Error: hand sizes differ")
            for p in [self.p1, self.p2, self.p3, self.p4]:
                print(type(p), len(p.hand), p.hand)
            exit()
        self.tricks_played += 1
        self.current_trick = []

    # Plays a round of the game
    # Deals cards, handles bidding, sets up the nest, and plays tricks until all cards are played
    def play_round(self):

        self.deal()
        self.all_bid()
        self.setup_nest()
        self.plays_file.write(f"Trump: {self.trump}\nNest: {self.nest}\n")
        while self.p1.hand:
            self.play_trick()

        # Add nest to last trick winner
        winner = [self.p1, self.p2, self.p3, self.p4][self.leading_player - 1]
        winner.taken.extend(self.nest)

        # Calculate points
        for p in [self.p1, self.p2, self.p3, self.p4]:
            p.pts_taken = sum(5 if c[1:] == '5' else 10 if c[1:] in ('10', '14') else 0 for c in p.taken)
        
        # Scoring (TODO: try to make look better? Might not be possible)
        if self.bid_winner in (1, 3):
            if self.p1.pts_taken + self.p3.pts_taken >= self.winning_bid:
                self.p1.score += self.p1.pts_taken + self.p3.pts_taken
                self.p3.score += self.p3.pts_taken + self.p1.pts_taken
            else:
                self.p1.score -= self.winning_bid
                self.p3.score -= self.winning_bid
            self.p2.score += self.p2.pts_taken + self.p4.pts_taken
            self.p4.score += self.p4.pts_taken + self.p2.pts_taken
        else:
            if self.p2.pts_taken + self.p4.pts_taken >= self.winning_bid:
                self.p2.score += self.p2.pts_taken + self.p4.pts_taken
                self.p4.score += self.p4.pts_taken + self.p2.pts_taken
            else:
                self.p2.score -= self.winning_bid
                self.p4.score -= self.winning_bid
            self.p1.score += self.p1.pts_taken + self.p3.pts_taken
            self.p3.score += self.p3.pts_taken + self.p1.pts_taken
        
        # End if any player is too negative
        if any(p.score <= -100000 for p in [self.p1, self.p2, self.p3, self.p4]):
            self.winner_file.write("A player's score is -100000 or less! Let's put an end to this madness!\n")
            for idx, p in enumerate([self.p1, self.p2, self.p3, self.p4], 1):
                self.winner_file.write(f"P{idx} {type(p)} score: {p.score}\n")
                self.winner_file.write(f"P{idx} {type(p)} bid: {p.max_bid}\n")
            exit()
        
        # Reset for next round
        for p in [self.p1, self.p2, self.p3, self.p4]:
            p.hand.clear()
            p.taken.clear()
            p.pts_taken = 0
        self.nest.clear()
        self.bid_winner = 0
        self.leading_player = 0
        self.winning_bid = 0
        self.trump = ''
        self.leading_suit = ''

    # Runs the game until a player reaches 300 points
    # Writes the winners to a file and resets scores for the next game
    def run(self):
        while all(p.score < 300 for p in [self.p1, self.p2, self.p3, self.p4]):
            self.play_round()
        self.winner_file.write("This game's winners:")
        for p in [self.p1, self.p2, self.p3, self.p4]:
            if p.score >= 300:
                self.winner_file.write(f" {p.get_name()}")
        self.winner_file.write("\n")
        for p in [self.p1, self.p2, self.p3, self.p4]:
            p.score = 0
        self.assign_characters()

    # Ends the game, writing final trimester data and closing files
    def end(self):
        self.plays_file.write("Trick trimester data:\n")
        self.plays_file.write(f"Karapet: {self.karapet_t1} {self.karapet_t2} {self.karapet_t3}\n")
        self.plays_file.write(f"Papa: {self.papa_t1} {self.papa_t2} {self.papa_t3}\n")
        self.plays_file.write(f"HH: {self.hh_t1} {self.hh_t2} {self.hh_t3}\n")
        self.plays_file.write(f"RR: {self.rr_t1} {self.rr_t2} {self.rr_t3}\n")
        self.winner_file.close()
        self.plays_file.close()
