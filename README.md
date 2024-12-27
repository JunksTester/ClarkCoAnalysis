# ClarkCoAnalysis
Analysis of the ballots from the 2024 Presidential election in Clark Co. Nevada.

Data taken from (https://elections.clarkcountynv.gov/electionresultsTV/cvr/24G/24G_CVRExport_NOV_Final_Confidential.zip)

Uses python3 with the numpy and matplotlib libraries.

(The following is taken from the python code)

We are given the Clark Co. Nevada ballot data
We want to check if the data has been manipulated
How do we do this?

Hypothesis -- If we can control for the location (precinct) and compare tabulators,
             then, we propose, that manipulation looks like a multi-modal 
             (multiple peaks) distribution. If the data is unimodal (one peak) 
             then we propose that the data is unmanipulated.

Motivation -- It is a well known test in statistics when looking for fraud or cheating,
             especially in sports, class or test grades, that if the distribution is
             unimodal (one peak) then it has one origin. Multiple peaks indicates that
             there are sub-populations of groups that:
                  Subpopulation 1: Didn't cheat
                  Subpopulation 2: Did cheat

Method     -- We will sort the Clark Co. Nevada data according to precinct number
             and tabulator number. Then we will compute the margin of REP%-DEM%
             per tabulator per precinct as compared to a constant tabulator that
             most (if not all) precincts used. By doing this we are keeping any
             precinct demographic effects constant and only sensitive to two things.
             
             We are sensitive to:
                  Sensitivity 1: Voting type (Early, Day-of, Mail)
                  Sensitivity 2: Tabulator

             By controlling for the voting type, since it is marked on the ballots,
             we can make this analysis only sensitive to individual tabulators.

Results    -- Our results, which are best shown with the attached histogram plot,
             show that the `Early Voting' and `Election Day' votes have been manipulated.
             The multimodal nature of the manipulation is observable so we do not need to
             compute additional statistical tests to prove its existence.
             We also find that the `Mail' votes are not manipulated.
             We find that the manipulation in `Early Voting' and `Election Day' are
             effectively identical and that they have three distributions:
                  Distribution A: The central unmanipulated distribution.
                                  It has a mean of roughly +0.4% , favoring REP
                  Distribution B: The left, manipulated to bias DEM distribution.
                                  It has a mean of roughly -0.7% , favoring DEM
                  Distribution C: The right, manipulated to bias REP distribution.
                                  It has a mean of roughly +1.2% , favoring REP
             
             We also find, as better explained in the discussion section below, by using
             the population differences of these distributions (A,B,C) we can estimate 
             that roughly 80000 votes were manipulated in Clark Co. Nevada.

Discussion -- The original hypothesis of 'peak searching' lacks a method for determining how much 
             and in what way the votes were manipulated. It only knows if they were or weren't.
             So it is unable to determine if a significant amount of votes were changed
             between the presidential candidates.

             Since the control tabulator, ("5"), was a `Mail' voting tabulator, 
             we expect a bias in the margin per tabulator.
             We do see this in the manipulated histograms. It is about +0.4% , favoring REP.

             Since there are different voting methods we expect a bias here. 
             We don't expect this to create additional peaks in the data. Only biases.

             This +0.4% bias contradicts the raw, total, votes which indicate that REP dominated
             in the `Early Voting' and `Election Day' voting by almost 20%.

             One possible explanation of this is that, since the histograms we see are for percentages, 
             that the population in the precincts in Distribution A and C compared to Distribution B must
             be different. We expect that Distribution A and C must correspond to high population
             precincts while Distribution B is of low population.

             This is found to be the cause. Distribution B, which favors DEM,
             has the smallest voting population, of 7541 votes, compared to population of
             390441 votes for Distribution A and population of 168555 votes for Distribution C.

             There is a way that votes could organically split like this. If officials sorted
             votes by party affiliation then we would see multiple distributions where this sorting
             was applied. However, if this was the case, then the sorting should have the same populations.
             We observe that they do not. This is problematic and further indication of manipulation.

             If we assume that the sorting hypothesis was true, that the two outlier distributions, 
             Distribution B and Distribution C, originally came from one distribution, similar to Distribution A,
             then they must have split evenly. Then the difference between Distribution B and Distribution C
             can be used to estimate the number of votes manipulated.
             We find that (168555-7541)/2 = 80507 votes were manipulated (with no rounding needed).
             This means that roughly 80000 votes were flipped or changed in someway in
             Clark Co. Nevada if the sorted votes hypothesis is true. Regardless of the sorted votes hypothesis we
             know that manipulation happened. The sorted votes hypothesis simply gives a way to estimate the magnitude.

             We do not know if the sorted votes hypothesis is true or specifically 
             how this manipulation was done with the current analysis. We only know that it did happen.
             More investigation is needed.

             Other studies which look at different metrics, such as voting margins of 
             candidates on the same ballot, are needed to confirm the magnitude 
             of manipulation of votes and their direction. Such as, were the 80000 from DEM to REP?
             Are the 80000 simply votes that were thrown out? A combination of things?
             This study does not know.


Thank you.

################################################################
############### EXPLANATION , METHODOLOGY END ##################
################################################################
