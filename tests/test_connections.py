import numpy as np
import behaviour as bh
import sciris as sc

# Set defaults
pop_size = 10000
pop_mod = bh.Pop(n=pop_size, rand_seed=1)  # Other Pop parameters can be adjusted 

pop_truth = sc.loadobj('/home/andrew/dev/wble_proj/behaviour_module/tests/population_truth.pop')

# Surprisingly fast 
pop_truth = pop_truth.popdict
pop_mod = pop_mod.popdict

assert len(pop_truth) == len(pop_mod)

for uid in range(len(pop_truth)):
    for layer in ['H','S','W','C']:
        assert np.array_equal(pop_mod[uid]['contacts'][layer], pop_truth[uid]['contacts'][layer])