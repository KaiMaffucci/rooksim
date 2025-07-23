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
    if k > K or n > N or k > n:
        return 0
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
def prob(d_0, t_0, d_r, h, t_h):
     
    d_n = d_0 - d_r  # remaining deck size

    upper_limit = min(d_r, t_0) # maximum number of cards of that type that can be removed
    total_prob = 0

    # iterate through all possible numbers of that type of card removed
    for t_r_i in range(upper_limit + 1):
        t_n_i = t_0 - t_r_i  # remaining cards of that type
        total_prob += hyper(d_0, t_0, d_r, t_r_i) * hyper(d_n, t_n_i, h, t_h)

    return total_prob    


if __name__ == "__main__":

    # Rook (Kentucky Discard) deck size
    d_0 = 41
    t_0 = 21 # number of cards for Karapet scenario 1
    d_r = 5 # only nest removed
    h = 9 # hand size
    
    prob_for_one_or_more = 0
    # calculate probability of drawing at least one card of that type in hand
    for t_h in range(1, h + 1):
        prob_value = prob(d_0, t_0, d_r, h, t_h)
        prob_for_one_or_more += prob_value

    print(f"Probability of drawing at least one card of that type in hand: {prob_for_one_or_more:.4f}")