#! /usr/bin/env python

#Data Science Bookcamp
#Task 1 Confidence Intervals For Probability of Strategy Success

import numpy as np
import matplotlib.pyplot as plt
import click
from lib import red_percentage_strat


def game_repetitions_win_mean(percentage, number_of_repeats):
    win_count = np.array([red_percentage_strat(percentage) for i in range(number_of_repeats)])
    return win_count.mean()


def win_frequencies(red_threshold, iterations):
    win_frequencies = []
    for i in range(1, iterations):
        win_frequencies.append(game_repetitions_win_mean(red_threshold, i))
    return win_frequencies


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


def generate_histogram(red_threshold, number_of_repeats, sample_size):
    freq_array = np.array([game_repetitions_win_mean(red_threshold, number_of_repeats) for i in range(sample_size)])
    likelihoods, bin_edges, patches = plt.hist(freq_array, bins='auto', edgecolor='black', density=True)
    bin_width = bin_edges[1] - bin_edges[0]
    return likelihoods, bin_width, bin_edges, patches


@click.command()
@click.option("--threshold",default=0.5, help="Red threshold")
@click.option("--repeats", default=100, help="Number of games")
@click.option("--sample", default=100, help="Sample size")
def main(threshold, repeats, sample):
    likelihoods, bin_width, bin_edges, patches = generate_histogram(threshold, repeats, sample)
    start_index, end_index = compute_high_confidence_interval(likelihoods, bin_width, bin_edges, patches)
    plt.xlabel('Binned Frequency')
    plt.ylabel('Relative Likelihood')
    if sample * repeats >= 100000:
        plt.savefig("confidence.png")
        plt.show()
    else:
        plt.show()


if __name__ == '__main__':
    main()
