import numpy as np
import sciris as sc

pop = sc.load("/home/andrew/dev/wble_proj/behaviour_module/tests/mobility_workers_debug.pop")

# potential_worker_uids

"""
Goal: Sample the following data structure: 
dests_a = {'miss':0.6, 'milton':0.4}
dests_b = {'toronto':0.9, 'milton':0.1}
dests_c = {'toronto':0.9, 'miss': 0.1}

params_work_mixing = dict(toronto = {"leaving":0.05, "dests":dests_a},
                          miss =    {"leaving":0.4, "dests":dests_b},
                          milton =  {"leaving":0.3, "dests":dests_c})

To do this, I need to: 
- Find how many people from each city are in other cities.
- how many torontonians are are mississauga, in milton.

"""
src_dest = {}
reg_list = list(pop.regs.keys())
ranges = {"toronto":[0,20000], "miss": [20000,30000], "milton":[30000,35000]}

for src in pop.regs:
    oregs = list(reg_list)
    oregs.remove(src)

    dest_counts = {oregs[0]:0, oregs[1]:0} # always only 2 other regs.
    for dest in oregs:
        worker_list = pop.regs[dest].work_structs.potential_worker_uids
        # Count number of people from src city working in this other region. 
        for uid in worker_list:
            if uid >= ranges[src][0] and uid < ranges[src][1]:
                dest_counts[dest] += 1
    src_dest[src] = dest_counts

# Normalize and calc ratio of ppl that left. 
n_left = {}
import sciris as sc

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
    
    n_left[src] = total_left/pop.total_valid_workers[src]
    
print(src_dest_normalized)
print(n_left)