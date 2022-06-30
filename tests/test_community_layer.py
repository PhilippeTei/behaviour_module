# import numpy as np
# import behaviour as bh
# import matplotlib.pyplot as plt
# import covasim as cv

##### Test 1: Count the total number of community contacts #####
# pop_size = 10000
# pop_mod = bh.BehaviourModel(n=pop_size, rand_seed=1)  # Other Pop parameters can be adjusted 

# # Verify that the total number of contacts is around the expected value.
# total_contacts = 0
# for uid, person in pop_mod.popdict.items():
#     total_contacts += len(person['contacts']['C'])

# print("The total number of community contacts is: {}".format(total_contacts))


##### Test 2: See if translation of popdict into covasim works #####
# pop_size = 10000
# pop_mod = bh.BehaviourModel(n=pop_size, rand_seed=1)  # Other Pop parameters can be adjusted 

# n_contacts_list = []

# for uid, person in pop_mod.popdict.items():
#     n_contacts_list.append(len(person['contacts']['S']))

# # Now reverse-engineer Covasim's strangeness. 
# pars = dict(
#     pop_size = pop_size,
#     pop_type = 'behaviour_module', 
#     n_days = 200,
#     rand_seed = 1)

# sim = cv.Sim(pars=pars, people=pop_mod.popdict)
# sim.run(verbose=False)

# p1 = sim.people.contacts['s']['p1']

# n_contacts_list_cv = []
# for i in range(pop_size):
#     n_contacts_list_cv.append(np.count_nonzero(p1==i))

# uids = np.arange(0, pop_size, 1)

# plt.plot(uids, n_contacts_list)
# plt.plot(uids, n_contacts_list_cv)
# plt.show()

##### Test 3: See if Synthpops + normal covasim has the same decaying contacts implementation #####

import numpy as np
import synthpops as sp
import matplotlib.pyplot as plt
import covasim as cv

pop_size = 10000
pop_mod = sp.Pop(n=pop_size, rand_seed=1)  # Other Pop parameters can be adjusted 

n_contacts_list = []

for uid, person in pop_mod.popdict.items():
    n_contacts_list.append(len(person['contacts']['S']))

# Now reverse-engineer Covasim's strangeness. 
pars = dict(
    pop_size = pop_size,
    pop_type = 'synthpops', 
    n_days = 200,
    rand_seed = 1)

sim = cv.Sim(pars=pars, people=pop_mod.popdict)
sim.run(verbose=False)

p1 = sim.people.contacts['s']['p1']

n_contacts_list_cv = []
for i in range(pop_size):
    n_contacts_list_cv.append(np.count_nonzero(p1==i))

uids = np.arange(0, pop_size, 1)

plt.plot(uids, n_contacts_list)
plt.plot(uids, n_contacts_list_cv)
plt.show()
