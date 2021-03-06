# Game Strategies Project

## Intro
Prerequisites:
1. Numpy
1. Matplotlib
1. Click

## Task
We have been set the task of coming up with a strategy for a simple card game. A standard deck of cards is shuffled and, one-by-one, the cards are turned over. At any point in the game, you may tell the dealer to stop. Once they have stopped, the next card that is turned over will determine the result of the game. If the card is black, then the game is lost, and if the card is red, the game is won.

## main()
Our strategy for the game is simulated by our first function **red_percentage_strat**. We specify a minimum fraction of red cards, which is the required argument for this function (*min_red_fraction*). If the percentage of remaining cards that are red is larger than our minimum fraction of red cards at any point, then the game is halted. The next card is turned over and we find out if we win or lose (where 1 represents a win and 0 represents a loss). If, however, the number of red cards remaining eventually decreases to 1, then the game is automatically halted and the next card that is turned over determines a win or a loss.

The **main()** function takes as arguments minimum red fraction (*threshold*, default=0.5) for our strategy, as well as the number of times the game is repeated to calculate one win frequency (*repeats*, default=100), and finally the sample size (*sample*, default = 100), i.e. the number of frequencies computed.

This function finds the frequency of wins for each group of game repetitions, doing this *n* times (sample size=*n*) for the given minimum red fraction. The function then uses this data to form a histogram, plotting binned frequencies of wins against their associated relative likelihoods. The final step for this function is to compute and return a high-confidence interval (minimum 95%) for this histogram in order to provide a range of win frequencies that our strategy win probability is highly likely to fall within.

### Histogram Analysis of Win Frequencies

![Win Frequencies Histogram](graphs/win_freq_histograms/confidence_histogram_50.png)
|:--:|
| *Histogram computed using game repeats=1000, sample size=10000 and minimum red threshold=0.5. The frequency range 0.470500 - 0.533533 represents a 95.38% confidence interval.* |

![Win Frequencies Histogram](graphs/win_freq_histograms/confidence_histogram_60.png)
|:--:|
| *Histogram computed using game repeats=1000, sample size=10000 and minimum red threshold=0.6. The frequency range 0.469770 - 0.533066 represents a 95.77% confidence interval.* |

![Win Frequencies Histogram](graphs/win_freq_histograms/confidence_histogram_70.png)
|:--:|
| *Histogram computed using game repeats=1000, sample size=10000 and minimum red threshold=0.7. The frequency range 0.467951 - 0.527918 represents a 95.58% confidence interval.* |

![Win Frequencies Histogram](graphs/win_freq_histograms/confidence_histogram_80.png)
|:--:|
| *Histogram computed using game repeats=1000, sample size=10000 and minimum red threshold=0.8. The frequency range 0.467308 - 0.529785 represents a 95.99% confidence interval.* |

![Win Frequencies Histogram](graphs/win_freq_histograms/confidence_histogram_90.png)
|:--:|
| *Histogram computed using game repeats=1000, sample size=10000 and minimum red threshold=0.9. The frequency range 0.466200 - 0.528764 represents a 95.68% confidence interval.* |

![Win Frequencies Histogram](graphs/win_freq_histograms/confidence_histogram_100.png)
|:--:|
| *Histogram computed using game repeats=1000, sample size=10000 and minimum red threshold=1.0. The frequency range 0.468761 - 0.529014 represents a 95.32% confidence interval.* |

We can see that for each different minimum red threshold value, the histograms take the shape of a Normal distribution, each centred approximately around the frequency 0.5. All of the confidence intervals that have been generated are over very similar ranges. The most favourable frequency range for odds of winning is 0.470500 - 0.533533, which occurs when the minimum red threshold is 0.5. It could be argued that this suggests that the first strategy will yield the highest frequency of wins, however the difference in ranges for the thresholds is negligable enough to say that this difference may just be down to random chance.

## **strategy_outcome_breakdown_graph()**
The function **strategy_outcome_breakdown_graph()** is used to analyse the occurrence of each of 4 different possible outcomes of our game strategy:


1. Halts: More Than One Red Card Left (Win)
1. Halts: One Red Card Left (Win)
1. Halts: More Than One Red Card Left (Lose)
1. Halts: One Red Card Left (Lose)


We use the **red_percentage_strat_index** function, which is a similar to our **red_percentage_strat** function, however it has been modified so the function returns the final card flipped over (win or loss) as well as the number of red cards remaining. Using each pair of values for card colour and remaining red cards, we may sort each game simulation into one of the 4 outcome types listed above.

**strategy_outcome_breakdown_graph()** takes as an argument the number of repeats for the game (*sob_repeats*, default=10000). The function repeats the game *n* times (*sob_repeats=n*), logging each different type of outcome and adding them to the relevant count of each outcome type. The counts are then each divided by the total number of games played, in order to find out their frequancies of occurence. This is done for every single minimum red fraction from 0.5 up to, and including, 1.0. We then plot a graph showing how the relative frequency of each outcome type is affected by changes in the minimum red fraction used for our strategy.

### Graphical Analysis of Relative Frequencies of Different Outcomes

![Frequency Graph of Different Outcomes](graphs/outcome_freq_red_strategies.png)

We can see from the graph that when the minimum red threshold is set to 0.5, the outcome with the highest frequency of occurence is *1) Halts: More Than One Red Card Left (Win)*, followed by *3) Halts: More Than One Red Card Left (Lose)*. This shows that for the lower red threshold values, we generally halt the game before we only have one red left, as it is much easier to satisfy the lower red threshold parameter. However, as this parameter increases in value, we can see that these outcome types *1)* and *3)* decrease in frequency, while the outcome types *2)* and *4)* increase. This is because the higher the minimum red threshold parameter, the less likely we are to satisfy the conditions of our strategy and halt the game before we only have one red card remaining.

Once the minimum red threshold has been increased to 0.85, the changes in frequency plateau. Outcome types *1)* and *2)* plateau at approximately 0.25, with outcome type *2)* now having a slightly higher frequency. Outcome type *3)* has decreased to a frequency of approximately 0, whereas outcome type *4)* has now increased to approximately 0.5.

All of the outcome types maintain these frequencies until the minimum red threshold reaches about 0.99. At this point, the frequency of outcome type *2)* increases to roughly 0.5, while the frequency of outcome *1)* decreases to approximately 0.

The sum of frequencies for outcome types *1)* and *3)* fluctuates around 0.5 through all of the values for the minimum red threshold, further supporting the conclusions from our **main()** function. Although the frequency of occurrence for our outcome types may change as we adjust our strategy, each of our different strategies have about a 50% chance of winning.
