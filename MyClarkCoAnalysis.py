#Written by anonymous so that all can replicate and be anonymous and knowledgable!
#################################################################
################## EXPLANATION , METHODOLOGY ####################
#################################################################
#
#We are given the Clark Co. Nevada ballot data
#We want to check if the data has been manipulated
#How do we do this?
#
#Hypothesis -- we expect rates to follow a Poisson-like distribution
#I usually recommend (https://en.wikipedia.org/wiki/Poisson_distribution)
#Its wiki but its OK reading material
#
#The gist is that, be it fundamental particle decays or rates of counting things, 
#rates tend to look like the Poisson distribution in our universe.
#This is to say, it has one mode (one peak) with a short tail on the left side and a long tail on the right.
#
#We will compute rates of votes by the frequency of DEM / REP and REP / DEM for each tabulator.
#In this way we are sensitive to specific tabulation machines or tabulators.
#We do both of these rates so that we can be sensitive to the different tails of the distribution.
#
#We do this because if the underlying data is described by one distribution of rates
#which, we expect to be like a Poisson, then there should be one mode (one peak)
#because the Poisson distribution (and those like it) is unimodal (one mode or one peak.) 
#If we measure that there is not one mode (one peak) and instead multiple modes (or peaks)
#then we know that the data is not consistent with one source for the rates.
#
#This is because to get a rate distribution with two modes you would have to add 
#(technically convolve, which is like adding for distributions)
#two individual rate distributions together.
#
#Example: If you conducted an experiment of the rate of rolling a '2' on random selection of 1000 d6 die 
#         and 1000 d12 die, you would expect to see a peak at a rate of 1/6 , from the d6s, 
#         and at 1/12 , from the d12s. Thus, it would not be unimodal.
#
#Instead, multiple modes means multiple sources of rates.
#But! What if the data has one source? We did one experiment! (or election)
#Then multiple modes means either some of the data has been changed or some data was taken in different methods.
#
#Since there are three methods of data taking that were done in Clark Co. , we will separate the rates
#according to each type of tabulation: Mail , Early Voting , Election Day
#By doing this our analysis cannot be contaminated by the separate hypothesis that multiple modes comes
#from multiple methods.
#
#We will measure modality using Hartigan's diptest (DOI: 10.1214/aos/1176346577)
#This is a widely used statistical measure to test if a distribution is unimodal or not.
#By using a statistical measure like this, which is narrow in scope and utility, the result should be accurate.
#
#By doing things this way we don't need to care about the exact distribution or fitting it.
#We also can keep ourself blind to what these numbers are and the results of the test by 
#using the TamperCheck function below.
#
#This is to say, this analysis was done in a way to keep the results unbiased.
#Thank you.
#
#################################################################
################ EXPLANATION , METHODOLOGY END ##################
#################################################################

import numpy as np #pip install numpy
import diptest as dt #pip install diptest
import csv

def TamperCheck(label,pvalRD,pvalDR):
    #this function takes two p-values , from two rates (REP / DEM and DEM / REP)
    #and sees if they pass the two population test or not
    #
    #if the p-value is < 0.05 (2 sigma significance) then the data IS NOT from one origin
    #and instead it is two or more origins, i.e. a MANIPULATED dataset and a CLEAN dataset
    print("\n##########Tamper check for %s ##########"%label)
    if(pvalRD < 0.05 or pvalDR < 0.05):
        print("At least one of the rates distribution of %s are two populations. It has been manipulated."%label)
    else:
        print("Both rates of %s are one population. It is clean and not manipulated."%label)

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

#count of the number of lines processed
linecnt = 0
#use this to omit problematic lines

#this is the tabulator number
#we have to do some parsing to get it
tnum = '="5"'.split("\"")[1] #this is an example!
#print(tnum) #this should say 5

#we use this to keep track of the number of '*' votes
#as I don't know what those mean!
starvotes = 0

#We will keep a dictionary for the rates
tabrates = {}
#in tabrates we will compute the following rates in a list object:
#0 = "MAIL" or "EARLY VOTING" or "ELECTION DAY" , the tabulator type
#1 = rate of DEM votes per REP votes
#2 = rate of REP votes per DEM votes (yes, they are inverse but we want both)

#we also keep these lists of rates for the diptest
MailDR = []
MailRD = []
EarlyDR = []
EarlyRD = []
DayDR = []
DayRD = []
TestDR = []
TestRD = []

ntest = 0

with open(FILENAME,'r') as file: #opens the file
    csv_r = csv.reader(file) #opens a csv reader object , so we can read
    for row in csv_r: #gets a single csv row in the csv
        linecnt += 1
        if(linecnt > 4): #the first vote is on the 5th line
            tnum = row[1].split("\"")[1]
            if(row[16] == '*' or row[19] == '*' or row[17] == '*' or row[18] == '*' or row[20] == '*'): #omit the outlier * marked votes
                starvotes += 1
            else:
                if(tnum not in tabulators):
                    tabulators[tnum] = [row[5],int(row[19]),int(row[16]),int(row[17])+int(row[18])+int(row[20])]
                else:
                    tabulators[tnum] = [row[5],tabulators[tnum][1]+int(row[19]),
                                        tabulators[tnum][2]+int(row[16]),
                                        tabulators[tnum][3]+int(row[17])+int(row[18])+int(row[20])]
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
    #compute the tabrates values and add them to tabrates
    if(tabulators[item][1] != 0 and tabulators[item][2] != 0):
        tabrates[item] = [tabulators[item][0],tabulators[item][1]/tabulators[item][2],tabulators[item][2]/tabulators[item][1]]
        #add to the lists , to be used by diptest
        if(tabulators[item][0] == "Mail"):
            MailRD.append(tabrates[item][1])
            MailDR.append(tabrates[item][2])
            if(ntest < 3): #manipulate the first three in the testing example
                TestRD.append(round(tabulators[item][1]*1.1)/round(tabulators[item][2]*0.9))
                TestDR.append(round(tabulators[item][2]*0.9)/round(tabulators[item][1]*1.1))
                ntest += 1
            else:
                TestRD.append(tabrates[item][1])
                TestDR.append(tabrates[item][2])
        if(tabulators[item][0] == "Early Voting"):
            EarlyRD.append(tabrates[item][1])
            EarlyDR.append(tabrates[item][2])
        if(tabulators[item][0] == "Election Day"):
            DayRD.append(tabrates[item][1])
            DayDR.append(tabrates[item][2])
    print("%i , %s\t\t: REP = %i , DEM = %i , THIRD = %i"%(int(item),tabulators[item][0],tabulators[item][1],tabulators[item][2],tabulators[item][3]))

#The dip statistic and p-value for the dip test
dipRD, pvalRD = dt.diptest(np.array(MailRD))
dipDR, pvalDR = dt.diptest(np.array(MailDR))
label = "Mail"

#we pass it to the TamperCheck function for printing the result!
TamperCheck(label,pvalRD,pvalDR)

#now we repeat for the other tabulator types
#The dip statistic and p-value for the dip test
dipRD, pvalRD = dt.diptest(np.array(EarlyRD))
dipDR, pvalDR = dt.diptest(np.array(EarlyDR))
label = "Early Voting"

#we pass it to the TamperCheck function for printing the result!
TamperCheck(label,pvalRD,pvalDR)

#now we repeat for the other tabulator types
#The dip statistic and p-value for the dip test
dipRD, pvalRD = dt.diptest(np.array(DayRD))
dipDR, pvalDR = dt.diptest(np.array(DayDR))
label = "Election Day"

#we pass it to the TamperCheck function for printing the result!
TamperCheck(label,pvalRD,pvalDR)

#As a final example, and sanity check, let us demonstrate that the diptest can identify manipulation! 
#We will take the mail in vote population and flip 10% of DEM votes to REP , but for only half of the tabulation runs
#(this was done above)
#and then compute the DR and RD rate p-values

#now we repeat for the other tabulator types
#The dip statistic and p-value for the dip test
dipRD, pvalRD = dt.diptest(np.array(TestRD))
dipDR, pvalDR = dt.diptest(np.array(TestDR))
label = "Example of Manipulation"

#we pass it to the TamperCheck function for printing the result!
TamperCheck(label,pvalRD,pvalDR)