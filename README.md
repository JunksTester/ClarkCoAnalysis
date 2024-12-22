# ClarkCoAnalysis
Analysis of the ballots from the 2024 Presidential election in Clark Co. Nevada.

Uses python3 with the numpy and diptest libraries

(The following is taken from the python code)


# EXPLANATION , METHODOLOGY

We are given the Clark Co. Nevada ballot data
We want to check if the data has been manipulated
How do we do this?

Hypothesis -- we expect rates to follow a Poisson-like distribution
Recommend (https://en.wikipedia.org/wiki/Poisson_distribution)
Its wiki but its OK reading material

The gist is that, be it fundamental particle decays or rates of counting things, 
rates tend to look like the Poisson distribution in our universe.
This is to say, it has one mode (one peak) with a short tail on the left side and a long tail on the right.

We will compute rates of votes by the frequency of DEM / REP and REP / DEM for each tabulator.
In this way we are sensitive to specific tabulation machines or tabulators.
We do both of these rates so that we can be sensitive to the different tails of the distribution.

We do this because if the underlying data is described by one distribution of rates
which, we expect to be like a Poisson, then there should be one mode (one peak)
because the Poisson distribution (and those like it) is unimodal (one mode or one peak.) 
If we measure that there is not one mode (one peak) and instead multiple modes (or peaks)
then we know that the data is not consistent with one source for the rates.

This is because to get a rate distribution with two modes you would have to add 
(technically convolve, which is like adding for distributions)
two individual rate distributions together.

Example: If you conducted an experiment of the rate of rolling a '2' on random selection of 1000 d6 die 
         and 1000 d12 die, you would expect to see a peak at a rate of 1/6 , from the d6s, 
         and at 1/12 , from the d12s. Thus, it would not be unimodal.

Instead, multiple modes means multiple sources of rates.
But! What if the data has one source? We did one experiment! (or election)
Then multiple modes means either some of the data has been changed or some data was taken in different methods.

Since there are three methods of data taking that were done in Clark Co. , we will separate the rates
according to each type of tabulation: Mail , Early Voting , Election Day
By doing this our analysis cannot be contaminated by the separate hypothesis that multiple modes comes
from multiple methods.

We will measure modality using Hartigan's diptest (DOI: 10.1214/aos/1176346577)
This is a widely used statistical measure to test if a distribution is unimodal or not.
By using a statistical measure like this, which is narrow in scope and utility, the result should be accurate.

By doing things this way we don't need to care about the exact distribution or fitting it.
We also can keep ourself blind to what these numbers are and the results of the test by 
using the TamperCheck function below.

This is to say, this analysis was done in a way to keep the results unbiased.
Thank you.
