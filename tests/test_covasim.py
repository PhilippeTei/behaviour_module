import numpy as np
import behaviour as sp
# import synthpops as sp
import covasim as cv

# Set defaults
pop_size = 10000
pop_type = 'behaviour_module'
n_days = 200

# Create parameter dictionary 
pars = dict(
    pop_size = pop_size,
    pop_type = pop_type, 
    n_days = n_days,
    rand_seed = 1)

# # Generate a new synthetic population 
pop = sp.BehaviourModel(pop_size, rand_seed=1)  # Other Pop parameters can be adjusted 
popdict = pop.popdict

sim = cv.Sim(pars=pars, people=popdict)
sim.run(verbose=False)
sim.plot()