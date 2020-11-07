#! /usr/bin/env python

#Data Science Bookcamp
#Task 1

import numpy as np
import matplotlib.pyplot as plt
import click

BLACK = 0
RED = 1


def red_percentage_strat(percentage, return_index=False):

	black_cards = 26 * [BLACK]
	red_cards = 26 * [RED]
	unshuffled_deck = black_cards + red_cards
	shuffled_deck = np.random.permutation(unshuffled_deck)
	red_percentage = percentage

	red_cards_remaining = 26
	total_cards_remaining = 52
	for i, card in enumerate(shuffled_deck):
		red_cards_remaining -= card
		total_cards_remaining -= 1
		if red_cards_remaining > 1:
			if red_cards_remaining / total_cards_remaining > red_percentage:
				break
		else:
			break

	return i+1, shuffled_deck[i+1] if return_index else shuffled_deck[i+1]


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


def game_repetitions_index_list(fraction_of_red, number_of_repeats):
	red_card_index_list = []
	black_card_index_list = []
	for i in range(number_of_repeats):
		card_index, card_colour = red_percentage_strat(fraction_of_red, return_index=True)
		if card_colour == 1:
			red_card_index_list.append(card_index)
		else:
			black_card_index_list.append(card_index)
	return red_card_index_list, black_card_index_list


def strategy_outcome_breakdown(fraction_of_red, number_of_repeats):
	success_index_list, failure_index_list = game_repetitions_index_list(fraction_of_red, number_of_repeats)

	red_more_than_one_successes = len([index for index in success_index_list if index < 51])
	one_red_left_successes = len(success_index_list) - red_more_than_one_successes
	red_more_than_one_failures = len([index for index in failure_index_list if index < 51])
	one_red_left_failures = len(failure_index_list) - red_more_than_one_failures
	results = np.array([red_more_than_one_successes, one_red_left_successes, red_more_than_one_failures, one_red_left_failures])
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
		result_frequencies = strategy_outcome_breakdown(fraction_of_red, number_of_repeats)
		red_more_than_one_successes_list.append(result_frequencies[0])
		one_red_left_successes_list.append(result_frequencies[1])
		red_more_than_one_failures_list.append(result_frequencies[2])
		one_red_left_failures_list.append(result_frequencies[3])
		fractions_of_red_list.append(fraction_of_red)
	result_frequency_dict = {'A':red_more_than_one_successes_list, 'B':one_red_left_successes_list, 'C':red_more_than_one_failures_list, 'D':one_red_left_failures_list}
	return result_frequency_dict, fractions_of_red_list


def generate_strategy_outcome_breakdown_graph(number_of_repeats):
	result_frequency_dict, fractions_of_red_list = s_o_b_ranged_threshold(number_of_repeats)
	plt.plot(fractions_of_red_list, result_frequency_dict['A'], '-', label='A) Halts: More Than One Red Card Left (Win)')
	plt.plot(fractions_of_red_list, result_frequency_dict['B'], ':', label='B) Halts: One Red Card Left (Win)')
	plt.plot(fractions_of_red_list, result_frequency_dict['C'], '-.', label='C) Halts: More Than One Red Card Left (Lose)')
	plt.plot(fractions_of_red_list, result_frequency_dict['D'], '--', label='D) Halts: One Red Card Left (Lose)')


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


@click.command()
@click.option('--sob_repeats', default=10000, help='Number of repeats.')
def strategy_outcome_breakdown_graph(sob_repeats):
	generate_strategy_outcome_breakdown_graph(sob_repeats)
	plt.xlabel('Minimum Reds Percentage')
	plt.ylabel('Outcome Frequencies')
	plt.title('Outcomes Frequencies\nfor Different Strategies')
	plt.legend()
	if sob_repeats >= 1000000:
		plt.savefig("outcome_freq_red_strategies.png")
		plt.show()
	else:
		plt.show()


if __name__ == '__main__':
	# main()
	strategy_outcome_breakdown_graph()

