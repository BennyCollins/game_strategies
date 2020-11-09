#! /usr/bin/env python

# Data Science Bookcamp
# Task 1 Frequency Analysis for Strategry Outcomes

import numpy as np
import matplotlib.pyplot as plt
import click


def red_percentage_strat_cards_remain(min_red_fraction):
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
    return shuffled_deck[i+1], red_cards_remaining


def game_repetitions_red_remaining_list(fraction_of_red, number_of_repeats):
    red_card_index_list = []
    black_card_index_list = []
    for i in range(number_of_repeats):
        card_colour, red_cards_remaining = red_percentage_strat_cards_remain(
            fraction_of_red)
        if card_colour == 1:
            red_card_index_list.append(red_cards_remaining)
        else:
            black_card_index_list.append(red_cards_remaining)
    return red_card_index_list, black_card_index_list


def strategy_outcome_breakdown(fraction_of_red, number_of_repeats):
    success_index_list, failure_index_list = game_repetitions_red_remaining_list(
        fraction_of_red, number_of_repeats)
    red_more_than_one_successes = len(
        [red_cards_remaining for red_cards_remaining in success_index_list if red_cards_remaining > 1])
    one_red_left_successes = len(
        success_index_list) - red_more_than_one_successes
    red_more_than_one_failures = len(
        [red_cards_remaining for red_cards_remaining in failure_index_list if red_cards_remaining > 1])
    one_red_left_failures = len(failure_index_list) - \
        red_more_than_one_failures
    results = np.array([red_more_than_one_successes, one_red_left_successes,
                        red_more_than_one_failures, one_red_left_failures])
    result_frequencies = results / number_of_repeats
    return result_frequencies


def s_o_b_ranged_threshold(number_of_repeats):
    red_more_than_one_successes_list = []
    one_red_left_successes_list = []
    red_more_than_one_failures_list = []
    one_red_left_failures_list = []
    fractions_of_red_list = []
    for n in range(50, 101):
        fraction_of_red = n / 100
        result_frequencies = strategy_outcome_breakdown(
            fraction_of_red, number_of_repeats)
        red_more_than_one_successes_list.append(result_frequencies[0])
        one_red_left_successes_list.append(result_frequencies[1])
        red_more_than_one_failures_list.append(result_frequencies[2])
        one_red_left_failures_list.append(result_frequencies[3])
        fractions_of_red_list.append(fraction_of_red)
    result_frequency_dict = {'A': red_more_than_one_successes_list, 'B': one_red_left_successes_list,
                             'C': red_more_than_one_failures_list, 'D': one_red_left_failures_list}
    return result_frequency_dict, fractions_of_red_list


def generate_strategy_outcome_breakdown_graph(number_of_repeats):
    result_frequency_dict, fractions_of_red_list = s_o_b_ranged_threshold(
        number_of_repeats)
    plt.plot(fractions_of_red_list,
             result_frequency_dict['A'], '-', label='A) Halts: More Than One Red Card Left (Win)')
    plt.plot(fractions_of_red_list,
             result_frequency_dict['B'], ':', label='B) Halts: One Red Card Left (Win)')
    plt.plot(fractions_of_red_list,
             result_frequency_dict['C'], '-.', label='C) Halts: More Than One Red Card Left (Lose)')
    plt.plot(fractions_of_red_list,
             result_frequency_dict['D'], '--', label='D) Halts: One Red Card Left (Lose)')


@click.command()
@click.option('--sob_repeats', default=100000, help='Number of repeats.')
def strategy_outcome_breakdown_graph(sob_repeats):
    generate_strategy_outcome_breakdown_graph(sob_repeats)
    plt.xlabel('Minimum Reds Percentage')
    plt.ylabel('Outcome Frequencies')
    plt.title()
    plt.suptitle('Outcomes Frequencies for Different Strategies', fontsize=14, fontweight='bold')
    plt.title(f"Game Repeats={sob_repeats}", fontsize=8)
    plt.legend()
    if sob_repeats >= 100000:
        plt.savefig("outcome_freq_red_strategies.png")
        plt.show()
    else:
        plt.show()


if __name__ == '__main__':
    strategy_outcome_breakdown_graph()
