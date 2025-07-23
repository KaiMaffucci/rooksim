# TODO: this is insanely broken somehow, need to fix it

import math

# n choose r
def C(n, r):
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

"""
Hypergeometric distribution
key parameters:
N: population size
K: number of successes in the population
n: number of draws
k: number of observed successes
returns the probability of observing k successes in n draws
"""
def hypergeometric(N, K, n, k):
    if k > K or n > N or k > n:
        return 0
    return (C(K, k) * C(N - K, n - k)) / C(N, n)

# Probability of drawing a hand of all cards of a certain type (in one scenario)
def hand_prob(new_deck_size, cards_of_type, cards_of_type_taken_out, hand_size, cards_of_type_in_hand):
    return hypergeometric(new_deck_size, cards_of_type - cards_of_type_taken_out, hand_size, cards_of_type_in_hand)

# Probability that one hand scenario occurs given a deck scenario
def combined_prob_for_scenario(deck_size, cards_of_type, total_cards_taken_out, cards_of_type_taken_out, hand_size, cards_of_type_in_hand):
    
    return hypergeometric(deck_size, cards_of_type, total_cards_taken_out, cards_of_type_taken_out) * hand_prob(deck_size - total_cards_taken_out, cards_of_type, cards_of_type_taken_out, hand_size, cards_of_type_in_hand)

# Total probability of drawing a hand of all cards of a certain type
def total_hand_prob(deck_size, cards_of_type, total_cards_taken_out, hand_size, cards_of_type_in_hand):
    
    total_prob = 0
    for cards_of_type_currently_out in range(cards_of_type + 1):
        total_prob += combined_prob_for_scenario(deck_size, cards_of_type, total_cards_taken_out, cards_of_type_currently_out, hand_size, cards_of_type_in_hand)

    return total_prob

if __name__ == "__main__":

    # Rook (Kentucky Discard) deck size
    initial_deck_size = 41

    # Karapet leading, scenario 1, first trimester
    cards_of_type = 21 # in this case, number of non-counter, non-trumps
    total_cards_taken_out = 5 # just the nest, like in the start of the game
    hand_size = 9

    # Calculate the probability of drawing a hand with a card of the specified type
    probability = total_hand_prob(initial_deck_size, cards_of_type, total_cards_taken_out, hand_size, 1)
    print("Probability of drawing a hand fitting this scenario:", probability)