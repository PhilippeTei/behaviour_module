import numpy as np
import behaviour as bh
import sciris as sc
import pandas as pd
import json
import matplotlib.pyplot as plt

"""
RESULTS: Distributions are good but normalizer is a bit off. Probably a parameter that we'll have to tune.
"""

# Set defaults
pars = dict(n = 50000, rand_seed=1, country_location="canada",dist_sw_probabilstically=True)
pop_mod = bh.BehaviourModel(pars)  # Other Pop parameters can be adjusted
pop_mod.save('/home/andrew/dev/wble_proj/behaviour_module/tests/pop_sw.pop')
# pop_mod = sc.load('/home/andrew/dev/wble_proj/behaviour_module/tests/pop_sw.pop')

# Load the theoretical pars. 
p_w_i = pop_mod.pars.sw_params.p_w_given_i
p_w_a = pop_mod.pars.sw_params.p_w_given_a

full_incomes = pop_mod.pars.sw_params.income_bracs
full_ages = pop_mod.pars.sw_params.age_bracs

# Calculate the empirical pars. See if P(W|A) and P(W|I) and P(W) are all replicated. 
I_counter = {i:0 for i in full_incomes}
A_counter = {i:0 for i in full_ages}
I_W_counter = {i:0 for i in full_incomes}
A_W_counter = {i:0 for i in full_ages}
num_watches = 0
pop = 0

for uid in pop_mod.structs.smartwatch_ownership_by_uid:
    pop += 1
    age = pop_mod.structs.age_by_uid[uid]
    income = pop_mod.structs.fam_income_by_uid[uid]
    I_counter[income] += 1 # Counts the totals per bracket. 
    A_counter[age] += 1
    if pop_mod.structs.smartwatch_ownership_by_uid[uid] == 1:
        I_W_counter[income] += 1
        A_W_counter[age] += 1
        num_watches += 1

#Get normalized array for I and A. 
I_counter_array = np.array(list(I_counter.values()))
p_w_given_income_emp = np.array(list(I_W_counter.values()))/I_counter_array

A_counter_array = np.array(list(A_counter.values()))
p_w_given_age_emp = np.array(list(A_W_counter.values()))/A_counter_array

# Rolling window filter the arrays. 
p_w_given_income_emp = np.convolve(p_w_given_income_emp, np.ones(5)/5, mode='same')
p_w_given_age_emp = np.convolve(p_w_given_age_emp, np.ones(5)/5, mode='same')


# On two subplots, plot empirical P(W|A) and P(W|I) against the theoretical ones.
fig, axs = plt.subplots(1, 2)
axs[0].plot(full_ages, p_w_given_age_emp, 'r', label='Empirical')
axs[0].plot(full_ages, p_w_a, 'g', label='Given')
axs[0].set_xlabel('Age')
axs[0].set_ylabel('P(W|A)')
axs[0].set_title('Probability of watch ownership vs age')
axs[0].legend()
axs[1].plot(full_incomes, p_w_given_income_emp, 'r', label='Empirical')
axs[1].plot(full_incomes, p_w_i, 'g', label='Given')
axs[1].set_xlabel('Income')
axs[1].set_ylabel('P(W|I)')
axs[1].set_title('Probability of watch ownership vs income')
axs[1].legend()
plt.show()

print("Ratio of People With Watches: ", num_watches/pop)
