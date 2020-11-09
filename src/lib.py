def red_percentage_strat(min_red_fraction, return_index=False):
    import numpy as np
    BLACK = 0
    RED = 1
    black_cards = 26 * [BLACK]
    red_cards = 26 * [RED]
    unshuffled_deck = black_cards + red_cards
    shuffled_deck = np.random.permutation(unshuffled_deck)
    red_cards_remaining = 26
    total_cards_remaining = 52
    for i, card in enumerate(shuffled_deck):
        red_cards_remaining -= card
        total_cards_remaining -= 1
        if red_cards_remaining > 1:
            if red_cards_remaining / total_cards_remaining > min_red_fraction:
                break
        else:
            break
    return i+1, shuffled_deck[i+1] if return_index else shuffled_deck[i+1]
