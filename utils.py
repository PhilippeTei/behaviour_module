"""
Some miscellaneous tools. 
"""
import numpy as np
import numba as nb
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

 
def n_poisson(rate, n):
    '''
    An array of Poisson trials.

    Args:
        rate (float): the rate of the Poisson process (mean)
        n (int): number of trials

    **Example**::

        outcomes = cv.n_poisson(100, 20) # 20 Poisson trials with mean 100
    '''
    return np.random.poisson(rate, n)


def n_neg_binomial(rate, dispersion, n, step=1): # Numba not used due to incompatible implementation
    '''
    An array of negative binomial trials. See cv.sample() for more explanation.

    Args:
        rate (float): the rate of the process (mean, same as Poisson)
        dispersion (float):  dispersion parameter; lower is more dispersion, i.e. 0 = infinite, ∞ = Poisson
        n (int): number of trials
        step (float): the step size to use if non-integer outputs are desired

    **Example**::

        outcomes = cv.n_neg_binomial(100, 1, 50) # 50 negative binomial trials with mean 100 and dispersion roughly equal to mean (large-mean limit)
        outcomes = cv.n_neg_binomial(1, 100, 20) # 20 negative binomial trials with mean 1 and dispersion still roughly equal to mean (approximately Poisson)
    '''
    nbn_n = dispersion
    nbn_p = dispersion/(rate/step + dispersion)
    samples = np.random.negative_binomial(n=nbn_n, p=nbn_p, size=n)*step
    return samples




 
def choose(max_n, n):
    '''
    Choose a subset of items (e.g., people) without replacement.

    Args:
        max_n (int): the total number of items
        n (int): the number of items to choose

    **Example**::

        choices = cv.choose(5, 2) # choose 2 out of 5 people with equal probability (without repeats)
    '''
    return np.random.choice(max_n, n, replace=False)

 
def choose_r(max_n, n):
    '''
    Choose a subset of items (e.g., people), with replacement.

    Args:
        max_n (int): the total number of items
        n (int): the number of items to choose

    **Example**::

        choices = cv.choose_r(5, 10) # choose 10 out of 5 people with equal probability (with repeats)
    '''
    return np.random.choice(max_n, n, replace=True)

