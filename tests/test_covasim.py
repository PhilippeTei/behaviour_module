import numpy as np
import behaviour as bh
import covasim as cv

# Set defaults
pop_size = 10000
pop_type = 'synthpops'
n_days = 200
pop_mod = bh.BehaviourModel(n=pop_size, rand_seed=1)  # Other Pop parameters can be adjusted 

# Create parameter dictionary 
pars = dict(
    pop_size = pop_size,
    pop_type = pop_type, 
    n_days = n_days)

# # Generate a new synthetic population 
pop = bh.BehaviourModel(pop_size)  # Other Pop parameters can be adjusted 
popdict = pop.popdict

sim = cv.Sim(pars=pars, people=popdict)
sim.run(verbose=False)
sim.plot()