"""
Some miscellaneous tools. 
"""
import numpy as np

def stuff_brackets_1d(bracs, vals, targ_bracs):
    """
    bracs: coarse brackets. 
    targ_bracs: finer ones. This must be in-line with bracs. 
    returns: corresponding vals for targ_bracs. 
    """
    # ensure all values of bracs are in targ_bracs. 
    assert all([i in targ_bracs for i in bracs])
    ret = np.zeros(len(targ_bracs))
    for i in range(len(bracs)):
        # get previous bracket value. Set to 0 if first. 
        prev_brac = 0 if i == 0 else bracs[i-1]

        # Get corresponding block of points in the new array. 
        n_arr_start = np.argmax(targ_bracs >= prev_brac)
        n_arr_end = np.argmax(targ_bracs >= bracs[i])

        # Set corresponding vals in ret. 
        ret[n_arr_start:n_arr_end] = vals[i]
    # deal with the last value. 
    ret[-1] = vals[-1]

    return ret

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
            # If you're on the last row, set the end to the end of the array.
            n_arr_age_end = len(targ_row_bracs) if i_age == pmf.shape[0]-1 else np.argmax(targ_row_bracs >= row_bracs[i_age])
            
            n_arr_inc_start = np.argmax(targ_col_bracs >= prev_inc)
            # If you're on the last column, just include the rest of the incomes. 
            n_arr_inc_end = len(targ_col_bracs) if i_inc == pmf.shape[1]-1 else np.argmax(targ_col_bracs >= col_bracs[i_inc])
            # Get the area of this block
            area = (n_arr_age_end - n_arr_age_start) * (n_arr_inc_end - n_arr_inc_start)
            # Scale the value by the area.
            A_I_joint_scaled[n_arr_age_start:n_arr_age_end, n_arr_inc_start:n_arr_inc_end] = cur_val / area
    return A_I_joint_scaled/np.sum(A_I_joint_scaled, axis=(0,1))
