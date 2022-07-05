import numpy as np
from behaviour import RegionalBehaviourModel

params_ca = dict(name = 'toronto', n=20000, com_contacts=20) # large city
params_cb = dict(name = 'miss', n=10000, com_contacts=10) # medium city
params_cc = dict(name = 'milton', n=5000,  com_contacts=10) # small city

dests_a = {'miss':0.6, 'milton':0.4}
dests_b = {'toronto':0.9, 'milton':0.1}
dests_c = {'toronto':0.9, 'miss': 0.1}

params_work_mixing = dict(toronto = {"leaving":0.05, "dests":dests_a},
                          miss =    {"leaving":0.4, "dests":dests_b},
                          milton =  {"leaving":0.3, "dests":dests_c})

pop_mod = RegionalBehaviourModel(None, params_work_mixing, *(params_ca, params_cb, params_cc))
