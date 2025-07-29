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


if __name__ == "__main__":

    # Karapet vs The Hog

    # probability that a player has at least one low card (5-9) in hand in trimester 1
    d_0 = 41
    t_0 = 4*5  # 5-9 cards in the deck
    d_r = 5  # nest removed
    h = 9  # hand size
    prob_low_card = prob_range(d_0, t_0, d_r, h, 1)
    print("Karapet")
    print(f"T1: Probability of drawing at least one low card (5-9) in hand: {(prob_low_card * 100):.2f}%")
    # probability of 4 or more low cards in hand
    prob_low_card_3 = prob_range(d_0, t_0, d_r, h, 4)
    print(f"T3: Probability of drawing at least 4 low cards (5-9) in hand: {(prob_low_card_3*100):.2f}%")
    # probability of 7 or more low cards in hand
    prob_low_card_3 = prob_range(d_0, t_0, d_r, h, 7)
    print(f"T3: Probability of drawing at least 7 low cards (5-9) in hand: {(prob_low_card_3*100):.2f}%")

    print("The Hog")
    # probability that a player has at least one high card (10-14 + rook) in hand in trimester 1
    t_0 = 4*5 + 1  # 10-14 cards + rook in the deck
    prob_high_card = prob_range(d_0, t_0, d_r, h, 1)
    print(f"T1: Probability of drawing at least one high card (10-14 + rook) in hand: {(prob_high_card*100):.2f}%")
    # probability of 4 or more high cards in hand
    prob_high_card_3 = prob_range(d_0, t_0, d_r, h, 4)
    print(f"T2: Probability of drawing at least 4 high cards (10-14 + rook) in hand: {(prob_high_card_3*100):.2f}%")
    # probability of 7 or more high cards in hand
    prob_high_card_3 = prob_range(d_0, t_0, d_r, h, 7)
    print(f"T3: Probability of drawing at least 7 high cards (10-14 + rook) in hand: {(prob_high_card_3*100):.2f}%")

    print("Papa comes for the hog")
    print("T1: Papa is just as likely to have a high card as the hog.")
    prob_papa = prob_range(d_0, t_0, d_r, h, 2)
    print(f"T2: Probability of drawing at least 2 high cards (10-14 + rook) in hand: {(prob_papa*100):.2f}%")
    prob_papa_3 = prob_range(d_0, t_0, d_r, h, 4)
    print(f"T3: Probability of drawing at least 4 high cards (10-14 + rook) in hand: {(prob_papa_3*100):.2f}%")
