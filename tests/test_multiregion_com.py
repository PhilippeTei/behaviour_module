import numpy as np
from behaviour import RegionalBehaviourModel

params_ca = dict(name = 'toronto', n=20000, com_contacts=20, rand_seed=1) # large city
params_cb = dict(name = 'miss', n=10000, com_contacts=10, rand_seed=1) # medium city
params_cc = dict(name = 'milton', n=5000,  com_contacts=10, rand_seed=1) # small city
pop_mod = RegionalBehaviourModel(None, None, *(params_ca, params_cb, params_cc))
fname = '/home/andrew/dev/wble_proj/behaviour_module/tests/mr_pop_no_bl_shift.pop'

pop_mod.save(fname)
# Test the inter-regional community mixing. 
# Test the total # contacts/city is correct. 

"""
def get_region(reg_starts, reg_lengths, uid):
    n_regs = len(reg_starts)
    for i in range(n_regs):
        if uid >= reg_starts[i] and uid < reg_starts[i]+reg_lengths[i]:
            return i

sources_arr = []
total_contacts = []
expected_contacts = []

for region in ['a', 'b', 'c']:
    # calculate community contacts from this part.
    %d reg_start_uids = [0, 20k, 40k]
    %d reg_sizes = [20k, 20k, 20k]
    for i in num_communities:
        start_uid = reg_start_uids[i]
        sources = [0,0,0]
        for uid in range(start_uid:start_uid+reg_sizes[i])
            for contact in self.total_popdicts[uid][contacts]['C']:
                sources[get_region(contact)] += 1

        # normalize
        sources = [i/sum(sources) for i in sources]
    sources_arr.append(sources)

print(sources_arr)

"""
def get_region(reg_starts, reg_lengths, uid):
    n_regs = len(reg_starts)
    for i in range(n_regs):
        if uid >= reg_starts[i] and uid < reg_starts[i]+reg_lengths[i]:
            return i

# TODO: Extend to n cities and actually read their parameters.
sources_arr = []
total_contacts_arr = []
expected_contacts_arr = []

reg_start_uids = [0, 20000, 30000]
reg_sizes = [20000, 10000, 5000]
n_contacts = [20, 10, 10] # todo: load from each region. 
n_regions = 3

for i_reg in range(n_regions):
    start_uid = reg_start_uids[i_reg]
    come_from_counter = [0,0,0]
    total_contacts = 0
    for uid in range(start_uid,start_uid+reg_sizes[i_reg]):
        for contact in pop_mod.total_popdict[uid]['contacts']['C']:
            come_from_counter[get_region(reg_start_uids, reg_sizes, contact)] += 1
        total_contacts += len(pop_mod.total_popdict[uid]['contacts']['C'])
    # normalize
    sources = [i/sum(come_from_counter) for i in come_from_counter]
    total_contacts_arr.append(total_contacts)
    expected_contacts_arr.append(n_contacts[i_reg]*reg_sizes[i_reg])
    
    sources_arr.append(sources)

ratio = list(np.array(total_contacts_arr)/np.array(expected_contacts_arr))

print("Contact Sources: {}".format(sources_arr))
print("Total/Expected Contacts: {}".format(ratio))
