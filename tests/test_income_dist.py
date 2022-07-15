import numpy as np
import behaviour as bh
import sciris as sc
import pandas as pd
import json
from behaviour.utils import rescale_2d_pmf
import matplotlib.pyplot as plt

# Set defaults
# pars = dict(n = 100000, rand_seed=1, country_location="canada")
# pop_mod = bh.BehaviourModel(pars)  # Other Pop parameters can be adjusted 

pop_mod = sc.load('/home/andrew/dev/wble_proj/behaviour_module/tests/pop_inc.pop')

# Calculate the theoretical conditional income distribution.
fpath = "/home/andrew/dev/wble_proj/behaviour_module/behaviour/data/income_age_dists/canada.csv"
raw_joint = pd.read_csv(fpath).values

fpath = "/home/andrew/dev/wble_proj/behaviour_module/behaviour/data/canada.json"
# load the json
with open(fpath) as f:
    pars = sc.objdict(**json.load(f))

# Get age and income brackets. 
age_bracs = pars.census_age_bracs
income_bracs = pars.census_income_bracs

# Make 1k-incrementing income bracket. 
full_incomes = np.arange(0, income_bracs[-1]+1000, 1000)
full_ages = np.arange(0, age_bracs[-1]+1, 1)
A_I_joint = rescale_2d_pmf(age_bracs, income_bracs, raw_joint, full_ages, full_incomes)

# Get marginal 
A_marg = np.sum(A_I_joint, axis=1)

# Visually inspect for 3 different ages. Plot the theoretical ones all green, empirical all red.
ages = [18, 34, 49]

# Make dictionary of zeros where keys are full_incomes
I_counter = {i:0 for i in full_incomes}
A_counter = {i:0 for i in full_ages}
# For each age, count the number of households making that income. Normalize. Plot in red. 
# Make three subplots. 
fig, axs = plt.subplots(1, 4, figsize=(12,4))

for k, age in enumerate(ages):
    
    # Get empirical P(I|A)
    for i, home_ages in enumerate(pop_mod.structs.homes_by_ages):
        if len(home_ages) > 1:
            holder_age = np.max(home_ages)
            A_counter[holder_age] += 1
            if holder_age == age:
                # Get income of household by getting UID of anyone in the household. 
                uid = pop_mod.structs.homes_by_uids[i][0]
                income = pop_mod.structs.fam_income_by_uid[uid]
                I_counter[income] += 1

    # Convert to an array and Normalize.
    I_counter_array = np.array(list(I_counter.values()))
    I_counter_array = I_counter_array/np.sum(I_counter_array)

    # Low pass filter this array using numpy. 
    I_counter_array = np.convolve(I_counter_array, np.ones(5)/5, mode='same')

    # Plot the empirical in red. 
    axs[k].plot(full_incomes, I_counter_array, 'r', label='Empirical')

A_counter_array = np.array(list(A_counter.values()))
A_counter_array = A_counter_array/np.sum(A_counter_array)

# Below is a pain because it's in brackets; not ages. 
# Calculate the theoretical P(A), which comes from the parameters in Synthpops. 
# household_head_age_distribution_by_family_size = [
#     [1, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
#     [2, 163.0, 999.0, 2316.0, 2230.0, 1880.0, 1856.0, 2390.0, 3118.0, 9528.0, 9345.0, 5584.0],
#     [3, 115.0, 757.0, 1545.0, 1907.0, 2066.0, 1811.0, 2028.0, 2175.0, 3311.0, 1587.0, 588.0],
#     [4, 135.0, 442.0, 1029.0, 1951.0, 2670.0, 2547.0, 2368.0, 1695.0, 1763.0, 520.0, 221.0],
#     [5, 61.0, 172.0, 394.0, 905.0, 1429.0, 1232.0, 969.0, 683.0, 623.0, 235.0, 94.0],
#     [6, 25.0, 81.0, 153.0, 352.0, 511.0, 459.0, 372.0, 280.0, 280.0, 113.0, 49.0],
#     [7, 24.0, 33.0, 63.0, 144.0, 279.0, 242.0, 219.0, 115.0, 157.0, 80.0, 16.0],
#     [8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
#   ]

# # First, sum over the rows. 
# a_counts = np.array(household_head_age_distribution_by_family_size)
# a_counts = np.sum(household_head_age_distribution_by_family_size[1:][:], axis=1)[1:]
# p_a_cv = a_counts/np.sum(a_counts)

# Plot the theoreticals. 
for k, age in enumerate(ages):
    # Calculate the theoretical P(I|A) for this income and age pair. 
    cur_joint = A_I_joint[age,:]
    cur_cond = cur_joint/A_counter_array[age]

    # Plot the theoretical in green.
    axs[k].plot(full_incomes, cur_cond, 'g', label='Theoretical')
    axs[k].set_xlabel('Income')
    axs[k].set_ylabel('P(I|A)')
    axs[k].set_title('Age: '+str(age))
    axs[k].legend()

# Not plot empirical vs theoretical p(a). 
axs[3].plot(full_ages, A_counter_array, 'r', label='Empirical')
axs[3].plot(full_ages, A_marg, 'g', label='Theoretical')
axs[3].set_xlabel('Age')
axs[3].set_ylabel('P(A)')
axs[3].set_title('Age Distribution')
axs[3].legend()

plt.show()
