#! /usr/bin/env python

#Data Science Bookcamp
#Task 1 Confidence Intervals for Probability of Strategy Success

import numpy as np
import matplotlib.pyplot as plt
import click


def red_percentage_strat(min_red_fraction):
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
    return shuffled_deck[i+1]


def game_repetitions_win_mean(percentage, number_of_repeats):
    win_count = np.array([red_percentage_strat(percentage) for i in range(number_of_repeats)])
    return win_count.mean()


def generate_histogram(red_threshold, number_of_repeats, sample_size):
    freq_array = np.array([game_repetitions_win_mean(red_threshold, number_of_repeats) for i in range(sample_size)])
    likelihoods, bin_edges, patches = plt.hist(freq_array, bins='auto', edgecolor='black', density=True)
    bin_width = bin_edges[1] - bin_edges[0]
    return likelihoods, bin_width, bin_edges, patches


def compute_high_confidence_interval(likelihoods, bin_width, bin_edges, patches):
    peak_index = likelihoods.argmax()
    area = likelihoods[peak_index] * bin_width
    start_index, end_index = peak_index, peak_index + 1
    while area < 0.95:
        if start_index > 0:
            start_index -= 1
        if end_index < likelihoods.size -1:
            end_index += 1
        area = likelihoods[start_index: end_index + 1].sum() * bin_width
    for i in range(start_index, end_index):
        patches[i].set_facecolor('yellow')
    start_range, end_range = bin_edges[start_index], bin_edges[end_index]
    range_string = f"{start_range:.6f} - {end_range:.6f}"
    print(f"The frequency range {range_string} represents a {100 * area:.2f}% confidence interval.")
    return start_index, end_index


@click.command()
@click.option("--threshold",default=1.0, help="Red threshold")
@click.option("--repeats", default=1000, help="Number of games")
@click.option("--sample", default=10000, help="Sample size")
def main(threshold, repeats, sample):
    likelihoods, bin_width, bin_edges, patches = generate_histogram(threshold, repeats, sample)
    start_index, end_index = compute_high_confidence_interval(likelihoods, bin_width, bin_edges, patches)
    plt.xlabel('Binned Frequency')
    plt.ylabel('Relative Likelihood')
    plt.suptitle('Relative Likelihoods of Win Frequencies', fontsize=14, fontweight='bold')
    plt.title(f"Min Red Threshold={threshold}, Game Repeats={repeats}, Sample Size={sample}", fontsize=8)
    if sample * repeats >= 10000:
        if threshold == 0.5:
            plt.savefig("confidence_histogram_50.png")
        if threshold == 0.6:
            plt.savefig("confidence_histogram_60.png")
        if threshold == 0.7:
            plt.savefig("confidence_histogram_70.png")
        if threshold == 0.8:
            plt.savefig("confidence_histogram_80.png")
        if threshold == 0.9:
            plt.savefig("confidence_histogram_90.png")
        if threshold == 1.0:
            plt.savefig("confidence_histogram_100.png")
        plt.show()
    else:
        plt.show()


if __name__ == '__main__':
    main()
