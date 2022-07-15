
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
import scipy.optimize as opt

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

def simulate_watch_dist(n, w_0, w_1, w_2):
    # Sample from the joint distribution. We want tuples of (i_age, i_income). i_age is limited to the range (0, 129).
    # i_income is limited to the range (0, 300000).
    # Work with indicies, not values.
    age_mesh, income_mesh = np.meshgrid(np.arange(len(targ_ages)), np.arange(len(targ_incs)))
    # Convert to a list of tuples. 
    age_income_tuples = list(zip(age_mesh.flatten(), income_mesh.flatten()))
    # Flatten the joint distribution such that it's compatible with the mesh. 
    A_I_joint_flat = A_I_joint.flatten(order='F')

    # Draw 1000 samples from A_I_joint_flat. (Note we're drawing indicies, non-inclusive of the last value. )
    i_samples = np.random.choice(len(age_income_tuples), size=n, p=A_I_joint_flat)
    
    total_by_i_age = np.zeros(len(targ_ages))
    total_by_i_income = np.zeros(len(targ_incs))
    watch_users_by_i_age = np.zeros(len(targ_ages))
    watch_users_by_i_income = np.zeros(len(targ_incs))
    num_watches = 0

    for uid in i_samples:
        i_income = int(age_income_tuples[uid][1])
        i_age = int(age_income_tuples[uid][0])
        total_by_i_age[i_age] += 1
        total_by_i_income[i_income] += 1

        f = w_2*(w_0*p_w_given_a_interp[i_age] + w_1*p_w_given_i_interp[i_income])
    
        # Decide whether to give a watch. 
        if np.random.random() < f:
            watch_users_by_i_age[i_age] += 1
            watch_users_by_i_income[i_income] += 1
            num_watches += 1

    p_w_given_age_emp = watch_users_by_i_age/total_by_i_age
    p_w_given_income_emp = watch_users_by_i_income/total_by_i_income

    return p_w_given_age_emp, p_w_given_income_emp, num_watches/n

def loss(params):
    w_0 = params[0]
    w_1 = params[1]
    w_2 = params[2] # normalizer

    # Run simulation, which is a func of the data and the parameters. 
    # Returns watch_users_by_age, watch_users_by_income, num_users. 
    p_w_given_age_emp, p_w_given_income_emp, p_w_emp = simulate_watch_dist(100000,w_0, w_1, w_2)
    
    # Calculate the actual losses. 
    loss_age = np.sum(np.square(p_w_given_age_emp - p_w_given_a_interp))
    loss_income = np.sum(np.square(p_w_given_income_emp - p_w_given_i_interp))
    loss_p_w = np.sum(np.square(p_w_emp - p_w))

    return loss_age + 100*loss_income + loss_p_w

theta_0 = [0.74851301, 0.45408946, 0.95152681]
theta_0 = np.array(theta_0)

# Minimize the parameters. Verbose. 

res = opt.minimize(loss, theta_0, method='Nelder-Mead', options={'maxiter': 1000, 'disp': True})
print(res)
# Run the simulation with the optimal parameters.
p_w_given_age_emp, p_w_given_income_emp, p_w_emp = simulate_watch_dist(100000,res.x[0], res.x[1], res.x[2])

# Compare empirical vs given conditional probs on two subplots for age and income. 
fig, axs = plt.subplots(1, 2)
axs[0].plot(targ_ages, p_w_given_age_emp, label='Empirical Method 1')
axs[0].plot(targ_ages, p_w_given_a_interp, label='Given')
axs[0].set_xlabel('Age')
axs[0].set_ylabel('P(W|A)')
axs[0].legend()
axs[1].plot(targ_incs, p_w_given_income_emp, label='Empirical Method 2')
axs[1].plot(targ_incs, p_w_given_i_interp, label='Given')
axs[1].set_xlabel('Income')
axs[1].set_ylabel('P(W|I)')
axs[1].legend()

plt.show()

print("Empirical P(W) = ", p_w_emp)