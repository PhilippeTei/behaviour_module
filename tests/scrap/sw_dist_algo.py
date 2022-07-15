"""
Algorithmic distribution of smartwatches.
In this simulation, we use P(A,I) where A and I are for the entire household. 
Thus we're simulating smartwatch ownership on an entire household granularity. 
"""
p_w = 0.3

p_w_given_i = [
0.1469311841,
0.1498439126,
0.2951441578,
0.2712238148,
0.4112715417,
]

# Less than. 
inc_bracs = [
20,
35,
50,
75,
300
]


p_w_given_a = [
0, # Set a zero probability for children, since we have no data. 
0.3808812547,
0.3516981132,
0.257718557,
0.1910219675,
0.1459854015
]

# Less than. 
age_bracs = [
18,
34,
49,
64,
74,
129
]

inc_bracs = [i*1000 for i in inc_bracs]

##### Get P(A,I) joint distribution. #####

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from behaviour.utils import rescale_2d_pmf
from behaviour.utils import stuff_brackets_1d

# Load the tabular data
fpath = "/home/andrew/dev/wble_proj/behaviour_module/new_data/Canada"
fname = "/canada_hhinc_by_age.csv"
canada_data = pd.read_csv(fpath+fname)
# Drop the first column (age) and add it to a list. 
canada_data.drop(canada_data.columns[0], axis=1, inplace=True)
# Get a 2d array of the values
canada_data_array = canada_data.values

# Use bracket maximums
census_income_bracs = [10,15,20,25,30,35,40,45,50,60,70,75,80,90,100,150,200,250,300]
census_income_bracs = [i*1000 for i in census_income_bracs]
census_age_bracs = [24, 34, 44, 54, 64, 129] # TODO: See whether this is fine to do. (Treating probability from 64 to 130 all the same)

targ_inc_range = (0, 300000)
target_age_range = (0, 129)
targ_incs = np.linspace(targ_inc_range[0], targ_inc_range[1], num=301) # Results in 2k increments. 
targ_ages = np.linspace(target_age_range[0], target_age_range[1], num=130)


A_I_joint = rescale_2d_pmf(census_age_bracs, census_income_bracs, canada_data_array, targ_ages, targ_incs)
p_age = np.sum(A_I_joint, axis=1) # Might be a bug? P(A) is veeeery small for 0-24 range. This is because only looking at couples. 
p_inc = np.sum(A_I_joint, axis=0)


# Test that this works. First look at replicating p_w. 

# Sample from the joint distribution. We want tuples of (i_age, i_income). i_age is limited to the range (0, 129).
# i_income is limited to the range (0, 300000).
# Work with indicies, not values.
age_mesh, income_mesh = np.meshgrid(np.arange(len(targ_ages)), np.arange(len(targ_incs)))
# Convert to a list of tuples. 
age_income_tuples = list(zip(age_mesh.flatten(), income_mesh.flatten()))
# Flatten the joint distribution such that it's compatible with the mesh. 
A_I_joint_flat = A_I_joint.flatten(order='F')

# Draw 1000 samples from A_I_joint_flat. (Note we're drawing indicies, non-inclusive of the last value. )
i_samples = np.random.choice(len(age_income_tuples), size=100000, p=A_I_joint_flat)


ppl_income_age = {}
for i in range(len(inc_bracs)):
    ppl_income_age[i] = {i:[] for i in range(len(age_bracs))} # Each cell contains a list of people we'll append to. 

for uid in i_samples:
    i_income = int(age_income_tuples[uid][1])
    i_age = int(age_income_tuples[uid][0])
    person = age_income_tuples[uid]

    # Get brackets. 
    income = targ_incs[i_income]
    age = targ_ages[i_age]

    # See which bracket the income calls into. 
    b_i = None
    for i, b_inc in enumerate(inc_bracs):
        if income < b_inc:
            b_i = i
            break
    # If still not assigned, assign to last bracket. 
    if b_i is None:
        b_i = len(inc_bracs) - 1
    
    # same for age.
    b_a = None
    for i, b_age in enumerate(age_bracs):
        if age < b_age:
            b_a = i
            break
    if b_a is None:
        b_a = len(age_bracs) - 1

    ppl_income_age[b_i][b_a].append(person)



print(total_by_income)
print(total_by_age) # TODO: this bracket has too many people.

# Calculate the number of watches to distribute for each age group. 
to_distribute_by_age = {total_by_age[i]*p_w_given_a[i] for i in range(len(age_bracs))}
to_distribute_by_inc = {total_by_income[i]*p_w_given_i[i] for i in range(len(inc_bracs))}

# Print these. 
print(to_distribute_by_age)
print(to_distribute_by_inc)

# 