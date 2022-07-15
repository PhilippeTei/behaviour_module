import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

def rescale_2d_pmf(row_bracs, col_bracs, pmf, targ_row_bracs, targ_col_bracs):
    """
    Requires that the input PMF is coarser than the target PMF. 
    """
    # Make sure that targ_ages, targ_incs, are numpy arrays. 
    targ_row_bracs = np.array(targ_row_bracs)
    targ_col_bracs = np.array(targ_col_bracs)

    # Make sure that all original bracket values are contained in the new axes. 
    # ensure all values of census_income_bracs are in targ_col_bracs. 
    for i in row_bracs:
        if i not in targ_row_bracs:
            raise ValueError("Value {} not in targ_row_bracs".format(i))
    for i in col_bracs:
        if i not in targ_col_bracs:
            raise ValueError("Value {} not in targ_col_bracs".format(i))

    # Create a new array called A_I_joint_scaled of the target axes. 
    A_I_joint_scaled = np.zeros((len(targ_row_bracs), len(targ_col_bracs)))

    for i_age in range(pmf.shape[0]):
        for i_inc in range(pmf.shape[1]):
            # Get the current value. 
            cur_val = pmf[i_age, i_inc]
            # Get the previous income value. Set to 0 if first.
            prev_inc = 0 if i_inc == 0 else col_bracs[i_inc-1]
            prev_age = 0 if i_age == 0 else row_bracs[i_age-1]
            # Get the corresponding block of points in the new array.
            n_arr_age_start = np.argmax(targ_row_bracs >= prev_age) # new array age start
            n_arr_age_end = np.argmax(targ_row_bracs >= row_bracs[i_age])
            n_arr_inc_start = np.argmax(targ_col_bracs >= prev_inc)
            n_arr_inc_end = np.argmax(targ_col_bracs >= col_bracs[i_inc])
            # Get the area of this block
            area = (n_arr_age_end - n_arr_age_start) * (n_arr_inc_end - n_arr_inc_start)
            # Scale the value by the area.
            A_I_joint_scaled[n_arr_age_start:n_arr_age_end, n_arr_inc_start:n_arr_inc_end] = cur_val / area
    return A_I_joint_scaled/np.sum(A_I_joint_scaled, axis=(0,1))

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

# Calculate the conditional probabilities for a few given ages. 
ages = [24, 34, 44, 54, 64]
all_cond_probs = []
# ages = [44]
for age in ages:
    cur_joint = A_I_joint[age,:]
    cur_p_age = p_age[age]
    p_I_given_A = cur_joint/cur_p_age
    all_cond_probs.append(p_I_given_A)
    plt.plot(p_I_given_A)
    print("Verify conditional: {}".format(np.sum(p_I_given_A)))

plt.legend(ages)
plt.show()

# Test the sampling. 
# Fix age bracket, sample 1000 times, and see if we replicate the distribution. 
cur_age_bracket = 2
cur_cond = all_cond_probs[cur_age_bracket]
cur_incomes = []
for i in range(10000):
    cur_income = np.random.choice(targ_incs, p=cur_cond)
    cur_incomes.append(cur_income)

# Get the frequencies of the incomes. Count occurances using a dictionary. 
inc_counts = {}

# Init all counts to 0. 
for i in targ_incs:
    inc_counts[i] = 0

for inc in cur_incomes:
    inc_counts[inc] += 1

# Get values from the dict in array form. 
inc_counts_array = np.array([inc_counts[i] for i in inc_counts])
inc_counts_array = inc_counts_array/np.sum(inc_counts_array)

plt.figure()
plt.plot(targ_incs, inc_counts_array)
plt.plot(targ_incs, cur_cond)
plt.legend(["Sampled", "Conditional"])
plt.show() # Results: It's good.

#### OLD CODE ####
# # Test: If you sum up over the new array, the sum should be the same as the original array.
# test_arr = np.zeros(canada_data.shape)
# for i_age in range(canada_data.shape[0]):
#     for i_inc in range(canada_data_array.shape[1]):
#         # Get the previous income value. Set to 0 if first.
#         prev_inc = 0 if i_inc == 0 else census_income_bracs[i_inc-1]
#         prev_age = 0 if i_age == 0 else census_age_bracs[i_age-1]
#         # Get the corresponding block of points in the new array.
#         n_arr_age_start = np.argmax(targ_ages >= prev_age)
#         n_arr_age_end = np.argmax(targ_ages >= census_age_bracs[i_age])
#         n_arr_inc_start = np.argmax(targ_incs >= prev_inc)
#         n_arr_inc_end = np.argmax(targ_incs >= census_income_bracs[i_inc])
#         # Sum up over this block. 
#         sum = np.sum(A_I_joint_scaled[n_arr_age_start:n_arr_age_end, n_arr_inc_start:n_arr_inc_end])
#         # Add to the test array.
#         test_arr[i_age, i_inc] = sum

# Get the RMSE error between test_arr and the canada_data_array. 
# rmse = np.sqrt(np.mean((test_arr - canada_data_array)**2))
# print(rmse)

# Make a 3d plot of A_I_joint_scaled
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# X, Y = np.meshgrid(targ_ages, targ_incs)
# ax.plot_surface(X, Y, np.transpose(A_I_joint_scaled))
# ax.set_xlabel('Age')
# ax.set_ylabel('Income')
# ax.set_zlabel('Probability')
# plt.show()


# Convert this to a PDF bt interpolating on both axes. 


###############################################################################
"""
This requires interpolation of input data sources to a predefined parameter value set. 
Incomes = 150 linearly spaced values between 5 and 300k. 
Ages = 130 linearly spaced values between 0 and 129. 

Iterpolate all input distributions to these resolutions. 

Notes: 
- This allows you to directly plug the agent's age when indexing P(W|A), etc.
- We both generate incomes and use them as an input. So if we stick to these 150 values, the PMF's will be compatible. 

TODO: 
- Implement rediscretize_pmf(), which returns the normalized pmf. 
    - Over-lay original and discretized. 
- Redo income distribution (in editor) with this loading in mind
- Implement smartwatch distribution. 
"""
###############################################################################

# def interpolate_pmf(x_axis, y_axis, vals_to_interp_to):
#     # if number of dimensions is 1
#     if len(x_axis.shape) == 1:
#         xaxis_new = np.linspace(min(x_axis), max(x_axis), vals_to_interp_to)
#         pmf_counts_interp = np.interp(xaxis_new, x_axis, y_axis)
#         return xaxis_new, pmf_counts_interp/np.sum(pmf_counts_interp)
#     else:
#         raise ValueError("x_axis must be a 1D array")

# def interpolate_2d_pmf(x_axis, y_axis, z_axis, xaxis_new, yaxis_new):
#     """
#     Interpolate a 2D pmf.
#     Args:
#         x_axis: 1D array of x values.
#         y_axis: 1D array of y values.
#         z_axis: 2D array of z values.
#         vals_to_interp_to: Number of values to interpolate to.
#         xaix_new: 1D array of new x values.
#         yaxis_new: 1D array of new y values.
#     Returns:
#         z_interp: 2D array of interpolated z values.
#     """
#     # if number of dimensions is 2
#     # Convert x axis and y axis to np arrays. 
#     x_axis = np.array(x_axis) # Safely idempotent. 
#     y_axis = np.array(y_axis)
#     if len(z_axis.shape) == 2:
#         """
#         This function indexes the column coordinates with the first input and the row coords with the second. 
#         """
#         f = interpolate.interp2d(y_axis, x_axis, z_axis, kind='linear')
#         z_axis_new = f(yaxis_new, xaxis_new)
#         return z_axis_new/np.sum(z_axis_new,axis=(0,1))

# # Interpolate a 2d pmf to the given x and y axes. 
# def interpolate_2d_pmf_grid(x_axis, y_axis, z_axis, x_targs, y_targs):
#     # if number of dimensions is 2
#     if len(z_axis.shape) == 2:
#         # Make a mesh out of the x_axis and y_axis
#         x_mesh, y_mesh = np.meshgrid(x_axis, y_axis)
#         # Convert the mesh into a list of tuples. (Coordinates)
#         xy_tuples = list(zip(x_mesh.flatten(), y_mesh.flatten()))
#         # Flatten the z axis. 
#         z_axis_flattened = z_axis.flatten(order='F') # go through all ages for a given income, etc. Just for compatibility with above. 
#         # Make a mesh out of the target axes
#         x_targ_mesh, y_targ_mesh = np.meshgrid(x_targs, y_targs)

#         # This applies the interpolation function
#         z_axis_interp = interpolate.griddata(xy_tuples, z_axis_flattened, 
#             (x_targ_mesh, y_targ_mesh), method='nearest') # other methods fill with "nan" by default. 

#         return z_axis_interp/np.sum(z_axis_interp, axis=(0,1))
#     else:
#         raise ValueError("z_axis must be a 2D array")
