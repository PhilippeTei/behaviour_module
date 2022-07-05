import numpy as np
import sciris as sc
from behaviour import RegionalBehaviourModel

"""
The code fails here, but that's because my previous "pop_truth" was buggy; it essentially simulated all work and family contacts being in city 1.
"""

params_ca = dict(name = 'toronto', n=20000, com_contacts=20, rand_seed=1) # large city
params_cb = dict(name = 'miss', n=10000, com_contacts=10, rand_seed=1) # medium city
params_cc = dict(name = 'milton', n=5000,  com_contacts=10, rand_seed=1) # small city
pop_mod = RegionalBehaviourModel(None, None, *(params_ca, params_cb, params_cc))

# Check *all* connections are the same between the popdicts. 
pop_truth = sc.loadobj('/home/andrew/dev/wble_proj/behaviour_module/tests/mr_pop_no_bl_shift.pop')

# Surprisingly fast 
pop_truth = pop_truth.total_popdict
pop_mod = pop_mod.total_popdict

assert len(pop_truth) == len(pop_mod)

for uid in range(len(pop_truth)):
    for layer in ['H','S','W']:
        assert np.array_equal(pop_mod[uid]['contacts'][layer], pop_truth[uid]['contacts'][layer])

## What are the implications for Covasim?