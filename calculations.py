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
n: number of draws (sample size)
k: number of observed successes in draw/sample
returns the probability of observing k successes in n draws
"""
def hyper(N, K, n, k):

    # test code: print parameters
    #print(f"hyper(N={N}, K={K}, n={n}, k={k})")

    if k > K or n > N or k > n:
        return 0
    if N - K <= n - k:
        return 1 / C(N, n)  # if all remaining cards are drawn, probability is 1
    return (C(K, k) * C(N - K, n - k)) / C(N, n)

"""
Probability of a hand with a certain amount of cards of a certain type being drawn
d_0: initial deck size
t_0: initial number of that type of card in the deck
d_r: total cards removed from the deck, from nest or tricks
h: hand size
t_h: number of cards of certain type in the hand
returns the probability of drawing t_h cards of that type in a hand of size h
"""
def prob(d_0, t_0, d_r, h, t_h, t_r_lower_bound=0):
     
    d_n = d_0 - d_r  # remaining deck size

    upper_limit = min(d_r, t_0) # maximum number of cards of that type that can be removed
    total_prob = 0

    # iterate through all possible numbers of that type of card removed
    for t_r_i in range(t_r_lower_bound, upper_limit + 1):
        t_n_i = t_0 - t_r_i  # remaining cards of that type
        total_prob += hyper(d_0, t_0, d_r, t_r_i) * hyper(d_n, t_n_i, h, t_h)

    return total_prob    

"""
Same as prob, but calculates the probability of drawing at least one card of that type in hand
"""
def prob_range(d_0, t_0, d_r, h, t_h, t_r_lower_bound=0):
    
    total_prob = 0
    # iterate through all possible numbers of that type of card in the hand
    for t_h_i in range(t_h, h + 1):
        total_prob += prob(d_0, t_0, d_r, h, t_h_i, t_r_lower_bound)
    return total_prob

"""
Calculates all scenarios for all players for the start of a given trimester
trim = which trimester is about to begin (1 means start of game)
"""
def all_scenarios_for_trimester(trim):
    
    d_0 = 41
    t_0 = 21 # number of cards for Karapet scenario 1
    d_r = 5 + (trim - 1)*3*4 # nest and tricks removed if trimester warrants it
    h = 9 - (trim - 1)*3 # hand size based on trimester

    # Karapet leading scenario 1
    prob_for_one_or_more = prob_range(d_0, t_0, d_r, h, 1)
    print(f"Trimester {trim}:")
    print(f"Probability of drawing at least one card of that type in hand: {prob_for_one_or_more:.4f}")

    # TODO: add other scenarios here

    return 0



if __name__ == "__main__":

    # Rook (Kentucky Discard) deck size
    """
    d_0 = 41
    t_0 = 21 # number of cards for Karapet scenario 1
    d_r = 5 # only nest removed
    h = 9 # hand size
    
    karapet_leading_scenario_1 = prob_range(d_0, t_0, d_r, h, 1)
    print(f"Probability of drawing at least one card of that type in hand: {karapet_leading_scenario_1:.4f}")
    """
    
    # calculate probability of drawing at least one card of that type in hand
    """all_scenarios_for_trimester(1)
    all_scenarios_for_trimester(2)
    all_scenarios_for_trimester(3)"""

    # probability that a player has at least one low card (5-9) in hand in trimester 1
    d_0 = 41
    t_0 = 4*5  # 5-9 cards in the deck
    d_r = 5  # nest removed
    h = 9  # hand size
    t_h = 1  # at least one low card in hand
    prob_low_card = prob_range(d_0, t_0, d_r, h, t_h)
    print(f"Probability of drawing at least one low card (5-9) in hand: {prob_low_card:.4f}")
    
    # probability that a player has at least one high card (10-14 + rook) in hand in trimester 1
    t_0 = 4*5 + 1  # 10-14 cards + rook in the deck
    t_h = 1  # at least one high card in hand
    prob_high_card = prob_range(d_0, t_0, d_r, h, t_h)
    print(f"Probability of drawing at least one high card (10-14 + rook) in hand: {prob_high_card:.4f}")

    # same probabilities for trimester 2, except we assume target cards were removed from each trick in the last semester (so 3 less target cards)
    d_r = 5 + 3*4  # nest and tricks removed
    h = 6  # hand size
    t_0 = 4*5  # 5-9 cards in the deck
    prob_low_card_trimester_2 = prob_range(d_0, t_0, d_r, h, t_h)
    print(f"Probability of drawing at least one low card (5-9) in hand in trimester 2: {prob_low_card_trimester_2:.9f}")
    prob_low_card_trimester_2 = prob_range(d_0, t_0, d_r, h, t_h, 3) # lower bound is 3 because we assume 3 low cards were removed during each previous trick
    print(f"Probability of drawing at least one low card (5-9) in hand in trimester 2 (assuming 3 were played already): {prob_low_card_trimester_2:.9f}")
    
    t_0 = 4*5 + 1  # 10-14 cards + rook in the deck
    prob_high_card_trimester_2 = prob_range(d_0, t_0, d_r, h, t_h)
    print(f"Probability of drawing at least one high card (10-14 + rook) in hand in trimester 2: {prob_high_card_trimester_2:.4f}")
    prob_high_card_trimester_2 = prob_range(d_0, t_0, d_r, h, t_h, 3)  # lower bound is 3 because we assume 3 high cards were removed during each previous trick
    print(f"Probability of drawing at least one high card (10-14 + rook) in hand in trimester 2 (assuming 3 were played already): {prob_high_card_trimester_2:.4f}")
    
    # same probabilities for trimester 3
    d_r = 5 + 6*4  # nest and tricks removed
    h = 3  # hand size
    t_0 = 4*5  # 5-9 cards in the deck
    prob_low_card_trimester_3 = prob_range(d_0, t_0, d_r, h, t_h)
    print(f"Probability of drawing at least one low card (5-9) in hand in trimester 3: {prob_low_card_trimester_3:.4f}")
    prob_low_card_trimester_3 = prob_range(d_0, t_0, d_r, h, t_h, 6)  # lower bound is 6 because we assume 6 low cards were removed during each previous trick 
    print(f"Probability of drawing at least one low card (5-9) in hand in trimester 3 (assuming 6 were played already): {prob_low_card_trimester_3:.4f}")
    
    t_0 = 4*5 + 1  # 10-14 cards + rook in the deck
    prob_high_card_trimester_3 = prob_range(d_0, t_0, d_r, h, t_h)
    print(f"Probability of drawing at least one high card (10-14 + rook) in hand in trimester 3: {prob_high_card_trimester_3:.4f}")
    prob_high_card_trimester_3 = prob_range(d_0, t_0, d_r, h, t_h, 6)  # lower bound is 6 because we assume 6 high cards were removed during each previous trick
    print(f"Probability of drawing at least one high card (10-14 + rook) in hand in trimester 3 (assuming 6 were played already): {prob_high_card_trimester_3:.4f}")
