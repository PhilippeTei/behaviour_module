import numpy as np
import behaviour as bh
import sciris as sc

# Set defaults
pars = dict(n = 10000, rand_seed=1)
pop_mod = bh.BehaviourModel(pars)  # Other Pop parameters can be adjusted 

pop_truth = sc.loadobj('/home/andrew/dev/wble_proj/behaviour_module/tests/population_truth.pop')

# Schools.
# Check if number of schools is equal.
assert len(pop_truth.schools) == len(pop_mod.schools)

# Check if students, teachers, other staff are all equal. 
for i_school in range(len(pop_truth.schools)):
    t_school = pop_truth.schools[i_school] # t for truth
    m_school = pop_mod.schools[i_school] # m for modified
    assert np.array_equal(t_school['student_uids'], m_school['student_uids'])
    assert np.array_equal(t_school['teacher_uids'], m_school['teacher_uids'])
    assert np.array_equal(t_school['non_teaching_staff_uids'], m_school['non_teaching_staff_uids'])
    
# Workplaces
assert len(pop_truth.workplaces) == len(pop_mod.workplaces)

for i_wp in range(len(pop_truth.workplaces)):
    t_wp = pop_truth.workplaces[i_wp]
    m_wp = pop_mod.workplaces[i_wp]
    assert np.array_equal(t_wp['member_uids'], m_wp['member_uids'])

# Homes
t_into_arr = np.array(pop_truth.homes_by_uids, dtype='object')
m_into_arr = np.array(pop_mod.homes_by_uids, dtype='object')

assert np.array_equal(t_into_arr, m_into_arr)


# # Set defaults
# pop_size = 10000
# pop_mod = bh.Pop(n=pop_size, rand_seed=1)  # Other Pop parameters can be adjusted 

# pop_truth = sc.loadobj('/home/andrew/dev/wble_proj/behaviour_module/tests/population_truth.pop')

# Surprisingly fast 
d_pop_truth = pop_truth.popdict
d_pop_mod = pop_mod.popdict

assert len(d_pop_truth) == len(d_pop_mod)

for uid in range(len(d_pop_truth)): # Don't probe in the community layer b/c normal SP doesn't have it. 
    for layer in ['H','S','W']:
        assert np.array_equal(d_pop_mod[uid]['contacts'][layer], d_pop_truth[uid]['contacts'][layer])