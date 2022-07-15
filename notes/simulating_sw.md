#### Parameters ####
Sensitivity: 

SE TP / (TP + FN)
- Denominator is all instances where you actually have covid.
Ex 1: People get infected. From that point until symptoms, accumulate positive and negative alarms. The daily sensitivity is positives / (positives + negatives). 
Ex 2: The total sensitivity is whether people get at least 1 alarm within time between infection and symptoms.

Specificity:

SP = TN / (TN + FP)
- Denominator is all instances when there's no covid. 
True negatives: assume the alarm makes a decision daily. Then TN would be when it says you don't have covid and you don't.


#### Behviour Implementation ####

* Phenomena *
- Which of your contacts do you reach out to? 
    - All of your family, 20% of your other contacts. 

* Implementation Questions *
- How to implement the decision tree such that you can skip the test phase? (either isolate or not w.p. p) (Don't model people seeking tests)
- Evaluate the decision tree all at once or in real time?
- 


#### Decisions ####
- Should we include post-symptomatic detection? Answer: No. 
    - After getting symptoms, people either get or don't get a test. We're looking at those who don't get a test. 
    - For these people, how much will the smartwatch increase their adherance? This behavioural characteristic is hard to characterise. 

- Should we implement sensitivity/specificity on a daily or total level? Answer: Total. 
    - By def, specificity has to be on a total level. 
    - Sensitivity's daily vs total implementation are equivalent; but the total one is cleaner, so we should stick with that.

- How should we treat asymptomatic cases? (since we have no data)
    - For now, ignore them. 

#### Required Features ####
- Simulating quarantine efficiently on an individual level. 
- Finding contacts. (Covasim has a function)

#### Cross-Disciplinary ####
- Covasim:
    - Viral load translates to transmissability?
    - Viral load vs symptom onset time?
