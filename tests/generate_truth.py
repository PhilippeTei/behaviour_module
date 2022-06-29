import synthpops as sp
import numpy as np

pop_size = 10000
pop = sp.Pop(n=pop_size, rand_seed=1)
pop.save('/home/andrew/dev/wble_proj/behaviour_module/tests/population_truth.pop')