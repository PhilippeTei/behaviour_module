# Covasim Integration Test.
import numpy as np
from behaviour import RegionalBehaviourModel
import covasim as cv

fname = '/home/andrew/dev/wble_proj/behaviour_module/tests/mr_pop.pop'

# Generate population
# params_ca = dict(name = 'toronto', n=20000, com_contacts=20) # large city
# params_cb = dict(name = 'miss', n=10000, com_contacts=10) # medium city
# params_cc = dict(name = 'milton', n=5000,  com_contacts=10) # small city
# pop_mod = RegionalBehaviourModel(None, *(params_ca, params_cb, params_cc))
# pop_mod.save(fname)

pop_mod = RegionalBehaviourModel.load(fname)
# Set defaults
pop_size = 35000
pop_type = 'behaviour_module'
n_days = 200

# Create parameter dictionary 

it0_advanced_params = dict(
    uid_list = None,
    regs_to_infect = {'toronto':0, 'miss': 0, 'milton':20} # default is 20 in covasim.
)
pars = dict(
    pop_size = pop_size,
    pop_type = pop_type, 
    n_days = n_days,
    rand_seed = 1)

sim = cv.Sim(pars=pars, people=pop_mod.total_popdict,it0_advanced_params=it0_advanced_params,
             multireg_pars = pop_mod.reg_pars)

sim.run(verbose=False)
sim.plot()