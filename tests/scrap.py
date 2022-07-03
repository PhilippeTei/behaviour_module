import numpy as np
import behaviour as bh
# import synthpops as sp

import covasim as cv
import matplotlib.pyplot as plt

pars = dict(n=20000, rand_seed=1)
pars_ss = dict(n=20000, rand_seed=1, com_dispersion=0.2)

pop = bh.BehaviourModel(pars)
# pop_ss = bh.BehaviourModel(pars_ss)
