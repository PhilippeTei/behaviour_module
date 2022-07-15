"""
Method 1: P(W|A,I) = normalizer_1 * P(W|A) * P(W|I)
Method 2: P(W|A,() = normalizer_2 * (1-P(W=0|I)*P(W=0|A))
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

# Calculate P(W|A, I). Note that A and I are of a much finer grain than the brackets we have SW data for. 
# So we need to interpolate. 
p_w_given_i_interp = stuff_brackets_1d(inc_bracs, p_w_given_i, targ_incs)
p_w_given_a_interp = stuff_brackets_1d(age_bracs, p_w_given_a, targ_ages)

# Calculate the normalizer. First calculate its denominator. 
denom = 0
for i in range(len(targ_ages)):
    for j in range(len(targ_incs)):
        denom += p_w_given_i_interp[j] * p_w_given_a_interp[i] * A_I_joint[i,j]

normalizer_1 = p_w/denom

# Calculate the normlizer for method 2. 
denom = 0
for i in range(len(targ_ages)):
    for j in range(len(targ_incs)):
        P_wnot_g_I = 1 - p_w_given_i_interp[j] # p(w=0|i)
        P_wnot_g_A = 1 - p_w_given_a_interp[i]
        alpha = 1 - P_wnot_g_I * P_wnot_g_A
        denom += alpha * A_I_joint[i,j]

normalizer_2 = p_w/denom # Normalizer is much lower than normalizer_1, indicating that the method 2 is more accurate.

print("The normalizer for method 1 is: ", normalizer_1)
print("The normalizer for method 2 is: ", normalizer_2)

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
i_samples = np.random.choice(len(age_income_tuples), size=1000000, p=A_I_joint_flat)

# Give watches to people using P(W|A,I); calculated via both methods. 
watches = 0
watches_via_meth_2 = 0
for uid in i_samples:
    i_income = int(age_income_tuples[uid][1])
    i_age = int(age_income_tuples[uid][0])
    if np.random.random() < p_w_given_i_interp[i_income] * p_w_given_a_interp[i_age] * normalizer_1:
        watches += 1
    # Calculate for method 2. 
    P_wnot_g_I = 1 - p_w_given_i_interp[i_income] # p(w=0|i)
    P_wnot_g_A = 1 - p_w_given_a_interp[i_age] # p(w=0|a)
    alpha = 1 - P_wnot_g_I * P_wnot_g_A
    if np.random.random() < alpha * normalizer_2:
        watches_via_meth_2 += 1

p_w_emp = watches/len(i_samples)
p_w_emp_meth_2 = watches_via_meth_2/len(i_samples)

print("Ratio of People With Watches: ", p_w_emp) # We get 0.293. Pass. 
print("Ratio of People With Watches (Method 2): ", p_w_emp_meth_2)

# See if P(W|A) is replicated. 
watch_users_by_i_age = np.zeros(len(targ_ages))
total_by_i_age = np.zeros(len(targ_ages))
watch_users_by_i_income = np.zeros(len(targ_incs))
total_by_i_income = np.zeros(len(targ_incs))

watch_users_by_i_age_meth_2 = np.zeros(len(targ_ages))
watch_users_by_i_income_meth_2 = np.zeros(len(targ_incs))

for uid in i_samples:
    i_income = int(age_income_tuples[uid][1])
    i_age = int(age_income_tuples[uid][0])
    total_by_i_age[i_age] += 1
    total_by_i_income[i_income] += 1
    
    # Decide whether to give a watch. 
    if np.random.random() < p_w_given_i_interp[i_income] * p_w_given_a_interp[i_age] * normalizer_1:
        watch_users_by_i_age[i_age] += 1
        watch_users_by_i_income[i_income] += 1
    
    # Repeat for method 2. 
    P_wnot_g_I = 1 - p_w_given_i_interp[i_income] # p(w=0|i)
    P_wnot_g_A = 1 - p_w_given_a_interp[i_age] # p(w=0|a)
    alpha = 1 - P_wnot_g_I * P_wnot_g_A
    if np.random.random() < alpha * normalizer_2:
        watch_users_by_i_age_meth_2[i_age] += 1
        watch_users_by_i_income_meth_2[i_income] += 1

# Calculate the probabilities. 
p_w_given_age_emp = watch_users_by_i_age/total_by_i_age
p_w_given_income_emp = watch_users_by_i_income/total_by_i_income
p_w_given_age_emp_meth_2 = watch_users_by_i_age_meth_2/total_by_i_age
p_w_given_income_emp_meth_2 = watch_users_by_i_income_meth_2/total_by_i_income

# Compare empirical vs given conditional probs on two subplots for age and income. 
fig, axs = plt.subplots(1, 2)
axs[0].plot(targ_ages, p_w_given_age_emp, label='Empirical Method 1')
axs[0].plot(targ_ages, p_w_given_age_emp_meth_2, label='Empirical Method 2')
axs[0].plot(targ_ages, p_w_given_a_interp, label='Given')
axs[0].set_xlabel('Age')
axs[0].set_ylabel('P(W|A)')
axs[0].legend()
axs[1].plot(targ_incs, p_w_given_income_emp, label='Empirical Method 2')
axs[1].plot(targ_incs, p_w_given_income_emp_meth_2, label='Empirical Method 2')
axs[1].plot(targ_incs, p_w_given_i_interp, label='Given')
axs[1].set_xlabel('Income')
axs[1].set_ylabel('P(W|I)')
axs[1].legend()
plt.show()
