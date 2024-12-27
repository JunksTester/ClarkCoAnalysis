#Written by anonymous so that all can replicate and be anonymous and knowledgable!
#Uses python3 on a windows machine
#################################################################
################## EXPLANATION , METHODOLOGY ####################
#################################################################
#
#We are given the Clark Co. Nevada ballot data
#We want to check if the data has been manipulated
#How do we do this?
#
#Hypothesis -- If we can control for the location (precinct) and compare tabulators,
#              then, we propose, that manipulation looks like a multi-modal 
#              (multiple peaks) distribution. If the data is unimodal (one peak) 
#              then we propose that the data is unmanipulated.
#
#Motivation -- It is a well known test in statistics when looking for fraud or cheating,
#              especially in sports, class or test grades, that if the distribution is
#              unimodal (one peak) then it has one origin. Multiple peaks indicates that
#              there are sub-populations of groups that:
#                   Subpopulation 1: Didn't cheat
#                   Subpopulation 2: Did cheat
#
#Method     -- We will sort the Clark Co. Nevada data according to precinct number
#              and tabulator number. Then we will compute the margin of REP%-DEM%
#              per tabulator per precinct as compared to a constant tabulator that
#              most (if not all) precincts used. By doing this we are keeping any
#              precinct demographic effects constant and only sensitive to two things.
#              
#              We are sensitive to:
#                   Sensitivity 1: Voting type (Early, Day-of, Mail)
#                   Sensitivity 2: Tabulator
#
#              By controlling for the voting type, since it is marked on the ballots,
#              we can make this analysis only sensitive to individual tabulators.
#
#Results    -- Our results, which are best shown with the attached histogram plot,
#              show that the `Early Voting' and `Election Day' votes have been manipulated.
#              The multimodal nature of the manipulation is observable so we do not need to
#              compute additional statistical tests to prove its existence.
#              We also find that the `Mail' votes are not manipulated.
#              We find that the manipulation in `Early Voting' and `Election Day' are
#              effectively identical and that they have three distributions:
#                   Distribution A: The central unmanipulated distribution.
#                                   It has a mean of roughly +0.4% , favoring REP
#                   Distribution B: The left, manipulated to bias DEM distribution.
#                                   It has a mean of roughly -0.7% , favoring DEM
#                   Distribution C: The right, manipulated to bias REP distribution.
#                                   It has a mean of roughly +1.2% , favoring REP
#              
#              We also find, as better explained in the discussion section below, by using
#              the population differences of these distributions (A,B,C) we can estimate 
#              that roughly 80000 votes were manipulated in Clark Co. Nevada.
#
#Discussion -- The original hypothesis of 'peak searching' lacks a method for determining how much 
#              and in what way the votes were manipulated. It only knows if they were or weren't.
#              So it is unable to determine if a significant amount of votes were changed
#              between the presidential candidates.
#
#              Since the control tabulator, ("5"), was a `Mail' voting tabulator, 
#              we expect a bias in the margin per tabulator.
#              We do see this in the manipulated histograms. It is about +0.4% , favoring REP.
#
#              Since there are different voting methods we expect a bias here. 
#              We don't expect this to create additional peaks in the data. Only biases.
#
#              This +0.4% bias contradicts the raw, total, votes which indicate that REP dominated
#              in the `Early Voting' and `Election Day' voting by almost 20%.
#
#              One possible explanation of this is that, since the histograms we see are for percentages, 
#              that the population in the precincts in Distribution A and C compared to Distribution B must
#              be different. We expect that Distribution A and C must correspond to high population
#              precincts while Distribution B is of low population.
#
#              This is found to be the cause. Distribution B, which favors DEM,
#              has the smallest voting population, of 7541 votes, compared to population of
#              390441 votes for Distribution A and population of 168555 votes for Distribution C.
#
#              There is a way that votes could organically split like this. If officials sorted
#              votes by party affiliation then we would see multiple distributions where this sorting
#              was applied. However, if this was the case, then the sorting should have the same populations.
#              We observe that they do not. This is problematic and further indication of manipulation.
#
#              If we assume that the sorting hypothesis was true, that the two outlier distributions, 
#              Distribution B and Distribution C, originally came from one distribution, similar to Distribution A,
#              then they must have split evenly. Then the difference between Distribution B and Distribution C
#              can be used to estimate the number of votes manipulated.
#              We find that (168555-7541)/2 = 80507 votes were manipulated (with no rounding needed).
#              This means that roughly 80000 votes were flipped or changed in someway in
#              Clark Co. Nevada if the sorted votes hypothesis is true. Regardless of the sorted votes hypothesis we
#              know that manipulation happened. The sorted votes hypothesis simply gives a way to estimate the magnitude.
#
#              We do not know if the sorted votes hypothesis is true or specifically 
#              how this manipulation was done with the current analysis. We only know that it did happen.
#              More investigation is needed.
#
#              Other studies which look at different metrics, such as voting margins of 
#              candidates on the same ballot, are needed to confirm the magnitude 
#              of manipulation of votes and their direction. Such as, were the 80000 from DEM to REP?
#              Are the 80000 simply votes that were thrown out? A combination of things?
#              This study does not know.
#
#
#Thank you.
#
#################################################################
################ EXPLANATION , METHODOLOGY END ##################
#################################################################

import numpy as np #pip install numpy
import diptest as dt #pip install diptest
import csv
import matplotlib.pyplot as plt #for figure creation

FILENAME = '24G_CVRExport_NOV_Final_Confidential.csv'#put your csv file name and/or file path here

#arrays for presidential vote results
#the type is element number 5 (starting at 0) in the csv row
#first column in mail , "Mail" in the csv
#second is early , "Early Voting"
#third is election day , "Election Day"
#
DEM = [0,0,0]
REP = [0,0,0]
TRD = [0,0,0]

#we make a python dictionary object
#to keep track of REP , DEM , 3RD PARTY votes
#per tabulation machine
tabulators = {}
#as an example for the format being used:
#tabulators = {5:["MAIL",0,0,0]}
#so we've added a first tabulator, 5 
#the first entry will tell us what type of tabulator it is ("MAIL")
#the three entries after have 0 votes for all three of REP, DEM, THIRD
#the tabulation number is element 1 in the csv row

#we make a python dictionary object
#to keep track of REP , DEM , 3RD PARTY votes
#per precinct
prec = {}
#as an example for the format being used:
#prec = {1013:{5:["MAIL",0,0,0,0,0]}}
#so we've added a first precinct, 1013
#it has a sub-dictionary of the tabulator number 5 
#the subdictionary has an array with that indicates mail votes
#the second entry will tell us what type of tabulator it is ("MAIL")
#the three entries after have 0 votes for all three of REP, DEM, THIRD
#the second-to-last entry is the rate of REP/TOT votes
#the last entry is the percentage margin of REP%-DEM%
#the precinct number is the first four numbers of element 6 in the csv row

#precinct controlled tabulator rates
EDrates = [] #election day
EVrates = [] #early voting
Mrates = [] #mail

#Population of votes in Distribution C and Distribution BaseException
DistAPop = 0
DistBPop = 0
DistCPop = 0

#count of the number of lines processed
linecnt = 0
#use this to omit problematic lines

#this is the tabulator number
#we have to do some parsing to get it
tnum = '="5"'.split("\"")[1] #this is an example!
#print(tnum) #this should say 5

#this is the precinct number
#we have to do some parsing to get it
pnum = '"1334 (1334|00)"'.split("\"")[1][0:4] #this is an example!
#print(pnum) #this should say 1334

#we use this to keep track of the number of '*' votes
#as I don't know what those mean!
starvotes = 0

#We will keep a dictionary for the rates
tabrates = {}
#in tabrates we will compute the following rates in a list object:
#0 = "MAIL" or "EARLY VOTING" or "ELECTION DAY" , the tabulator type
#1 = rate of DEM votes per REP votes
#2 = rate of REP votes per DEM votes (yes, they are inverse but we want both)

ntest = 0

with open(FILENAME,'r') as file: #opens the file
    csv_r = csv.reader(file) #opens a csv reader object , so we can read
    for row in csv_r: #gets a single csv row in the csv
        linecnt += 1
        if(linecnt > 4): #the first vote is on the 5th line
            tnum = row[1].split("\"")[1]
            pnum = row[6].split("\"")[0][0:4]
            if(row[16] == '*' or row[19] == '*' or row[17] == '*' or row[18] == '*' or row[20] == '*'): #omit the outlier * marked votes
                starvotes += 1
            else:
                if(tnum not in tabulators):
                    tabulators[tnum] = [row[5],int(row[19]),int(row[16]),int(row[17])+int(row[18])+int(row[20])]
                else:
                    tabulators[tnum] = [row[5],tabulators[tnum][1]+int(row[19]),
                                        tabulators[tnum][2]+int(row[16]),
                                        tabulators[tnum][3]+int(row[17])+int(row[18])+int(row[20])]
                if(pnum not in prec):
                    prec[pnum] = {tnum : [row[5],int(row[19]),int(row[16]),int(row[17])+int(row[18])+int(row[20])]}
                else:
                    if(tnum not in prec[pnum]):
                        if((int(row[19]) + int(row[16])+int(row[17])+int(row[18])+int(row[20])) > 0):
                            prec[pnum][tnum] = [row[5],int(row[19]),int(row[16]),int(row[17])+int(row[18])+int(row[20]),
                                                int(row[19])/(int(row[19]) + int(row[16])+int(row[17])+int(row[18])+int(row[20])),
                                                int(row[19])/(int(row[19]) + int(row[16])+int(row[17])+int(row[18])+int(row[20])) - int(row[16])/(int(row[19]) + int(row[16])+int(row[17])+int(row[18])+int(row[20]))]
                        else:
                            prec[pnum][tnum] = [row[5],int(row[19]),int(row[16]),int(row[17])+int(row[18])+int(row[20]),
                                                0.0,
                                                0.0]
                    else:
                        prec[pnum][tnum] = [row[5],prec[pnum][tnum][1]+int(row[19]),
                                        prec[pnum][tnum][2]+int(row[16]),
                                        prec[pnum][tnum][3]+int(row[17])+int(row[18])+int(row[20]),
                                        (prec[pnum][tnum][1]+int(row[19]))/(prec[pnum][tnum][1]+int(row[19]) + prec[pnum][tnum][2]+int(row[16]) + prec[pnum][tnum][3]+int(row[17])+int(row[18])+int(row[20])),
                                        (prec[pnum][tnum][1]+int(row[19]))/(prec[pnum][tnum][1]+int(row[19]) + prec[pnum][tnum][2]+int(row[16]) + prec[pnum][tnum][3]+int(row[17])+int(row[18])+int(row[20])) - (prec[pnum][tnum][2]+int(row[16]))/(prec[pnum][tnum][1]+int(row[19]) + prec[pnum][tnum][2]+int(row[16]) + prec[pnum][tnum][3]+int(row[17])+int(row[18])+int(row[20]))]
                if(row[5] == "Mail"):
                    if(int(row[19]) == 1):
                        REP[0] += 1
                    if(int(row[16]) == 1):
                        DEM[0] += 1
                    if(int(row[17]) == 1 or int(row[18]) == 1 or int(row[20]) == 1):
                        TRD[0] += 1
                if(row[5] == "Early Voting"):
                    if(int(row[19]) == 1):
                        REP[1] += 1
                    if(int(row[16]) == 1):
                        DEM[1] += 1
                    if(int(row[17]) == 1 or int(row[18]) == 1 or int(row[20]) == 1):
                        TRD[1] += 1
                if(row[5] == "Election Day"):
                    if(int(row[19]) == 1):
                        REP[2] += 1
                    if(int(row[16]) == 1):
                        DEM[2] += 1
                    if(int(row[17]) == 1 or int(row[18]) == 1 or int(row[20]) == 1):
                        TRD[2] += 1

#text output for the user , or for the log if you run
#python MyClarkCoAnalysis.py >>Output.log
print("##########\nVoting totals by type:\n##########")
print("\nMAIL   : REP = %i , DEM = %i , THIRD = %i"%(REP[0],DEM[0],TRD[0]))
print("\nEARLY  : REP = %i , DEM = %i , THIRD = %i"%(REP[1],DEM[1],TRD[1]))
print("\nDAY OF : REP = %i , DEM = %i , THIRD = %i"%(REP[2],DEM[2],TRD[2]))

print("##########\nNumber of '*' votes: %i\n##########"%starvotes)

print("\n##########\nVoting totals by tabulator:\n##########")
for item in tabulators:
    print("%i , %s\t\t: REP = %i , DEM = %i , THIRD = %i"%(int(item),tabulators[item][0],tabulators[item][1],tabulators[item][2],tabulators[item][3]))
    

#Uncomment this if you want to see EVERYTHING
#print("\n##########\nVoting totals by precinct:\n##########")
for item in prec:
    for tabs in prec[item]:
        #Uncomment this if you want to see EVERYTHING
        #print("PREC: %i , TAB: %i , %s\t\t: REP = %i , DEM = %i , THIRD = %i"%(int(item),int(tabs),prec[item][tabs][0],prec[item][tabs][1],prec[item][tabs][2],prec[item][tabs][3]))
        if int(tabs) != 5 and "5" in prec[item] and len(prec[item][tabs]) > 5 and prec[item][tabs][0] == "Election Day":
            EDrates.append(prec[item][tabs][5]-prec[item]["5"][5])
            if(prec[item]["5"][5] - prec[item][tabs][5] < 0.2 and prec[item]["5"][5] - prec[item][tabs][5] > -0.9):
                DistAPop += prec[item][tabs][1]+prec[item][tabs][2]+prec[item][tabs][3]
            if(prec[item]["5"][5] - prec[item][tabs][5] < -0.9):
                DistBPop += prec[item][tabs][2]+prec[item][tabs][2]+prec[item][tabs][3]
            if(prec[item]["5"][5] - prec[item][tabs][5] > 0.2):
                DistCPop += prec[item][tabs][2]+prec[item][tabs][2]+prec[item][tabs][3]
        if int(tabs) != 5 and "5" in prec[item] and len(prec[item][tabs]) > 5 and prec[item][tabs][0] == "Early Voting":
            EVrates.append(prec[item][tabs][5]-prec[item]["5"][5])
            if(prec[item]["5"][5] - prec[item][tabs][5] < 0.2 and prec[item]["5"][5] - prec[item][tabs][5] > -0.9):
                DistAPop += prec[item][tabs][1]+prec[item][tabs][2]+prec[item][tabs][3]
            if(prec[item]["5"][5] - prec[item][tabs][5] < -0.9):
                DistBPop += prec[item][tabs][2]+prec[item][tabs][2]+prec[item][tabs][3]
            if(prec[item]["5"][5] - prec[item][tabs][5] > 0.2):
                DistCPop += prec[item][tabs][2]+prec[item][tabs][2]+prec[item][tabs][3]
        if int(tabs) != 5 and "5" in prec[item] and len(prec[item][tabs]) > 5 and prec[item][tabs][0] == "Mail":
            Mrates.append(prec[item][tabs][5]-prec[item]["5"][5])

plt.figure(figsize=(8, 6), dpi=160)
plt.hist(np.array(EDrates),bins=100,range=(-2,2),alpha=0.5,label='Election Day',density=True)
plt.hist(np.array(EVrates),bins=100,range=(-2,2),alpha=0.5,label='Early Voting',density=True)
plt.hist(np.array(Mrates),bins=100,range=(-2,2),alpha=0.5,label='Mail',density=True)
plt.legend()
plt.title("Margin of Votes REP%-DEM% with Constant Precinct, Varying Tabulator")
plt.xlabel("Margin of Votes, REP%-DEM%")
plt.ylabel("Normalized Bin Counts for 100 bins of 0.04% Width")
plt.savefig("VoteMarginTabulatorHist.pdf")
plt.savefig("VoteMarginTabulatorHist.jpg")


print("Population of Distribution A (center peak): %i"%DistAPop)
print("Population of Distribution B (left peak): %i"%DistBPop)
print("Population of Distribution C (right peak): %i"%DistCPop)
print("Estimate of manipulated votes : %i"%int((DistCPop-DistBPop)/2))