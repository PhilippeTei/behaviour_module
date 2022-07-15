## Tests ##
- Recreate the age by income pdf and test average error vs the input pdf. 
- Test that P(I|A) sums to 1 and has dimensions # brackets.
- See if there's a fast way to calculate P(I|A). 

## Data Structures ##
*Actual available data*
Ages: under 25, 25-44, 45-64, over 64. (For Canada)
Income: 5k increments from <10k to >200k. 
class age_income_joint(){
    age_to_bracket = {
        0:0,
        ...
        24:0,
        25:1,
        ...
        44:1,
        45:2,
        ...
    }
    bracket_to_income = {
        0:5000,
        1:1000,
        etc
    }
    joint_dist = [b_age][b_income]. // [[0,0,1],[0,1,0], etc.] 
        - By default load income = 70k w.p. 1.
}

# Income Distribution #
*Revised implementation*
- For each bracket, assign the top income for the bracket.
    - For the highest bracket, simply assign that income + 100k.

*Usage*
for f in households:
    get the abv i
    for person in households:
        assign_income() 

# Matching distributions across different discretizations #
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

# Distribute watches #
*Implementation*
// Get age brackets A, I. 
// Get P(A,I), an axb matrix.
    // for A_bracket, I_bracket:
        // Interpolate census P(A,I) to 1000 elements
        // Sum up all elements in the square covered by the brackets A, I. 

// Calculate P(W|A, I). The inputs are A and I; two scalars. 

// P(W|A, I) = normalizer*P(W|A)P(W|I). These two values are scalars, loaded from a table.
    Where:
    // normalizer = p_w/denom
        denom = 0
        for A' in age_brackets:
            for I' in incomes:
                denom += P(W|A')P(W|I')P(A,I) // TODO: get P(A,I). 
        *Parameters*

// Test that this works.

// Sample a bunch of people according to P(A,I). What's P(W) in total? (Expect 0.3)
    // Get 1000x2 tuples by sampling the distribution 1000 times. UID's will correspond to the indicies. 
    // Populate has_watch (1000x1) using prev. tuples. 
    // Find ratio of has_watch == 1. 

// Calculate P(W|A). For each bracket, compare to input P(W|A). 
    Plot and visually inspect histograms. 
// Same for P(W|I).

*Usage*
for u in uids:
    assign_smartwatch(u.income, u.age)



## Scrap ##
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
