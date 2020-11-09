# Game Strategies Project

## **main()** Function: (thresh=0.5, repeats=1000, sample=10000)
Our main strategy for the game is our first function **red_percentage_strat**. We specify a minimum fraction of red cards, which is the main argument for this function (*min_red_fraction*). If the number of red cards remaining, divided by the total number of remaining cards, is larger than our minimum fraction of red cards at any point, then the game is halted, the next card is turned over and we find out if we win or lose (where 1 represents a win and 0 represents a loss). If, however, the number of red cards remaining eventually decreases to 1, then the game is automatically halted and the next card that is turned over determines a win or a loss.

This code is used to execute the **main()** function, which takes as arguments minimum red fraction (default = 0.5) for our strategy, as well as the number of times the game is repeated (default = 100), and finally the sample size (default = 100).

This function finds the frequency of wins for each group of game repetitions, doing this **n** times (sample size = n) for the given minimum red fraction. The function then uses this data to form a histogram, plotting binned frequencies of wins against their associated relative likelihoods. The final step for this function is to find a high-confidence interval for this histogram in order to provide a range of win frequencies that our strategy win probability is likely to fall within.

![](confidence.png)
*Histogram computed using game repeats=1000, sample size=10000 and minimum red threshold*

## **strategy_outcome_breakdown_graph()** Function: (n=100000)
The function **strategy_outcome_breakdown_graph()** is used to analyse the occurrence of each of 4 different possible outcomes of our game strategy:

1. Halts: More Than One Red Card Left (Win)
1. Halts: One Red Card Left (Win)
1. Halts: More Than One Red Card Left (Lose)
1. Halts: One Red Card Left (Lose)

We use our **red_percentage_strat**function, with *return_index=True* so the function returns the final card flipped over (win or loss) as well as this card’s index.

When we use **red_percentage_strat** in this way, it can be used to log the index of the card turned over at the end of each game. Using each index, we may sort each outcome into one of the 4 outcome types below:

takes as an argument the *number of repeats* for the game (default = 10000).



The function repeats the game m times (number of repeats = m), logging each different type of outcome, adding them to the relevant count of each outcome type, and then uses these counts to find relative frequencies. This is done for every single minimum red fraction for 0.5 up to, and including, 1.0. We then plot a graph showing how the relative frequency of each outcome type is affected by changes in the minimum red fraction used for our strategy.
