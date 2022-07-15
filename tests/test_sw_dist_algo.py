import numpy as np
import behaviour as bh
import sciris as sc
import pandas as pd
import json
import matplotlib.pyplot as plt


# Set defaults
pars = dict(n = 10000, rand_seed=1, country_location="canada")
pop_mod = bh.BehaviourModel(pars)  # Other Pop parameters can be adjusted

# TODO: This currently breaks the save function.
pop_mod.save('/home/andrew/dev/wble_proj/behaviour_module/tests/pop_sw.pop')
# pop_mod = sc.load('/home/andrew/dev/wble_proj/behaviour_module/tests/pop_sw.pop')

# Load the theoretical pars. 
p_w_i = pop_mod.pars.sw_params.p_w_given_i
p_w_a = pop_mod.pars.sw_params.p_w_given_a

inc_bracs = pop_mod.pars.sw_params.income_bracs
age_bracs = pop_mod.pars.sw_params.age_bracs

# Calculate the empirical pars. See if P(W|A) and P(W|I) and P(W) are all replicated. 
I_counter = {i:0 for i in range(len(inc_bracs))}
A_counter = {i:0 for i in range(len(age_bracs))}
I_W_counter = {i:0 for i in range(len(inc_bracs))}
A_W_counter = {i:0 for i in range(len(age_bracs))}
num_watches = 0
pop = 0

for uid in pop_mod.structs.smartwatch_ownership_by_uid:
    pop += 1
    age = pop_mod.structs.age_by_uid[uid]
    income = pop_mod.structs.fam_income_by_uid[uid]

    # Need to find the bracket inc_bracs that income falls into. 
    b_i = None
    for i, b_inc in enumerate(inc_bracs):
        if income < b_inc:
            b_i = i
            break
    # If still not assigned, assign to last bracket.
    if b_i is None:
        b_i = len(inc_bracs) - 1
    
    # Same for age.
    b_a = None
    for i, b_age in enumerate(age_bracs):
        if age < b_age:
            b_a = i
            break
    if b_a is None:
        b_a = len(age_bracs) - 1

    I_counter[b_i] += 1 # Counts the totals per bracket. 
    A_counter[b_a] += 1
    if pop_mod.structs.smartwatch_ownership_by_uid[uid] == 1:
        I_W_counter[b_i] += 1
        A_W_counter[b_a] += 1
        num_watches += 1

#Get normalized array for I and A. 
I_counter_array = np.array(list(I_counter.values()))
p_w_given_income_emp = np.array(list(I_W_counter.values()))/I_counter_array

A_counter_array = np.array(list(A_counter.values()))
p_w_given_age_emp = np.array(list(A_W_counter.values()))/A_counter_array

# # Rolling window filter the arrays. 
# p_w_given_income_emp = np.convolve(p_w_given_income_emp, np.ones(5)/5, mode='same')
# p_w_given_age_emp = np.convolve(p_w_given_age_emp, np.ones(5)/5, mode='same')


# On two subplots, plot empirical P(W|A) and P(W|I) against the theoretical ones.
fig, axs = plt.subplots(1, 2)
axs[0].plot(age_bracs, p_w_given_age_emp, 'r', label='Empirical')
axs[0].plot(age_bracs, p_w_a, 'g', label='Given')
axs[0].set_xlabel('Age')
axs[0].set_ylabel('P(W|A)')
axs[0].set_title('Probability of watch ownership vs age')
axs[0].legend()
axs[1].plot(inc_bracs, p_w_given_income_emp, 'r', label='Empirical')
axs[1].plot(inc_bracs, p_w_i, 'g', label='Given')
axs[1].set_xlabel('Income')
axs[1].set_ylabel('P(W|I)')
axs[1].set_title('Probability of watch ownership vs income')
axs[1].legend()
plt.show()

print("Ratio of People With Watches: ", num_watches/pop)
