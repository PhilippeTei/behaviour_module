import numpy as np
from behaviour import RegionalBehaviourModel

"""
Warning: hard-coded. Will break if you change the params. 
"""
params_ca = dict(name = 'toronto', n=20000, com_contacts=20, country_location='canada') # large city
params_cb = dict(name = 'miss', n=10000, com_contacts=10, country_location='canada') # medium city
params_cc = dict(name = 'milton', n=5000,  com_contacts=10, country_location='canada') # small city

dests_a = {'miss':0.6, 'milton':0.4}
dests_b = {'toronto':0.9, 'milton':0.1}
dests_c = {'toronto':0.9, 'miss': 0.1}

params_work_mixing = dict(toronto = {"leaving":0.05, "dests":dests_a},
                          miss =    {"leaving":0.4, "dests":dests_b},
                          milton =  {"leaving":0.3, "dests":dests_c})

pop_mod = RegionalBehaviourModel(None, params_work_mixing, *(params_ca, params_cb, params_cc))

"""
## Tests. ##
- 1. Structures: Plot workplace ID vs # mobility workers in the company. 
    - Could implement global workplace ID.. do this for all regions.
- 2. Structures: Re-create the matrix.
- 3. (TODO) Contacts: Disable inter-community. Check no spread. Enable employment. Ensure spread.

Test 2 Results: 
- Ratios are perfect. n_left has <20% error. Probably some details behind how they allocate workers.

Error is due to:
Beginning Workers: 16846
REMAINING WORKERS: 3644
Beginning Workers: 5620
REMAINING WORKERS: 1880
Beginning Workers: 3273
REMAINING WORKERS: 923
I.e. synthpops only allocates about 70% of the workers.
"""

## Test 1: Workforce breakdown ##
firms = pop_mod.regs['toronto'].structs.workplace_uid_lists
n_from_a = {}
n_from_b = {}
n_from_c = {}
for reg in pop_mod.regs:
    firms = pop_mod.regs[reg].structs.workplace_uid_lists
    n_from_a[reg] = []
    n_from_b[reg] = []
    n_from_c[reg] = []
    
    for firm in firms:
        n_from_a[reg].append(sum([i < 20000 for i in firm])) # identify origin of the agents based on their uid
        n_from_b[reg].append(sum([i >= 20000 and i < 30000 for i in firm]))
        n_from_c[reg].append(sum([i >= 30000 for i in firm]))

import matplotlib.pyplot as plt

# Create 3 subplots, for the 3 separate regions. 
fig, axs = plt.subplots(1,3,sharey=True)

regs = list(pop_mod.regs.keys())

for i_reg, reg in enumerate(pop_mod.regs):
    x_axis = np.arange(len(pop_mod.regs[reg].structs.workplace_uid_lists))
    axs[i_reg].plot(x_axis, n_from_a[reg])
    axs[i_reg].plot(x_axis, n_from_b[reg])
    axs[i_reg].plot(x_axis, n_from_c[reg])
    axs[i_reg].set_title(f"Workers of {reg}")
    axs[i_reg].set_xlabel("Company ID")
    axs[i_reg].set_ylabel("Number of workers")

plt.legend(regs)

plt.show()

#### Test 2: Recreate the Matrix ####
#### Recreate the Matrix ####
# pop_mod.total_valid_workers["toronto"]

src_dest = {}
reg_list = list(pop_mod.regs.keys())

ranges = {"toronto":[0,20000], "miss": [20000,30000], "milton":[30000,35000]}
    
for src in pop_mod.regs:
    oregs = list(reg_list)
    oregs.remove(src)
    
    dest_counts = {oregs[0]:0, oregs[1]:0} # always only 2 other regs.

    for dest in oregs:
        # Count number of people from src city working in this other region. 
        wkplces = pop_mod.regs[dest].structs.workplace_uid_lists
        for wkplce in wkplces:
            for uid in wkplce:
                if uid > ranges[src][0] and uid < ranges[src][1]:
                    dest_counts[dest] += 1
        # Repeat for other places people could be working. 
        schools = pop_mod.regs[dest].structs.teacher_uid_lists
        schools_nt = pop_mod.regs[dest].structs.non_teaching_staff_uid_lists

        for school in schools:
            for uid in school:
                if uid > ranges[src][0] and uid < ranges[src][1]:
                    dest_counts[dest] += 1
        for school in schools_nt:
            for uid in school:
                if uid > ranges[src][0] and uid < ranges[src][1]:
                    dest_counts[dest] += 1
        
        src_dest[src] = dest_counts

# Normalize and calc ratio of ppl that left. 
n_left = {}
import sciris as sc

# Extracted from prints. 
tor_dep = 16846 - 3644
miss_dep = 5620 - 1880
mil_dep = 3273 - 923

nums_dep = {"toronto":tor_dep, "miss":miss_dep, "milton":mil_dep} # dep for deployed. 

# tor_correction = tor_dep / 16846
# miss_correction = miss_dep / 5620
# mil_correction = mil_dep / 3273


src_dest_normalized = sc.dcp(src_dest)
for src in src_dest:
    oregs = list(reg_list)
    oregs.remove(src)
    
    total_left = 0
    for dest in oregs:
        total_left += src_dest[src][dest]
    
    # Update entries with normalized values. 
    for dest in oregs:
        src_dest_normalized[src][dest] = src_dest[src][dest]/total_left
    
    n_left[src] = total_left/nums_dep[src]
    n_left[src] = n_left[src]


print(src_dest_normalized)
print(n_left) # A bit of error; say we're talking about toronto here. We'd have to know the ratio of toronto people we deployed to mississsauga and the ratio we deployed to Milton that ended up getting employed. 