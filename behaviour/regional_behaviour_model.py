from behaviour import BehaviourModel
import numpy as np
import sciris as sc

def load_default_mixing_pars(num_cities):
    come_from_cur = 0.8
    come_from_others = 0.2
    
    ret = (come_from_others/(num_cities-1))* \
    np.ones((num_cities, num_cities))

    for i in range(ret.shape[0]):
        ret[i][i] = come_from_cur

    return ret # Just a matrix with the diagonal set to come_from_cur.

class RegionalBehaviourModel():
    def __init__(self, mixing_pars = None, *args):
        if mixing_pars == None:
            mixing_pars = load_default_mixing_pars(len(args))
        
        # Init cities
        self.regs = sc.objdict() # reg stands for region.
        for reg_params in args: # args is a list.
            cur_reg = reg_params.pop('name')
            reg_params["as_region"] = True
            self.regs[cur_reg] = BehaviourModel(reg_params) # inits. 

        # Allocate people to their structures. TODO: coupled initialization for workplaces.
        for _, rsim in self.regs.items():
            rsim.make_structures()
        
        # Make connections. 
        for _, rsim in self.regs.items():
            rsim.init_contact_structure() # TODO: implement these wrappers
            rsim.make_home_contacts()
            rsim.make_school_contacts()
            rsim.make_work_contacts()
        
        self.make_mixed_community_contacts()

        self.aggregate_regions() # make a popdict usable by covasim.

    def make_mixed_community_contacts():
        return

    def aggregate_regions():
        # TODO: just append the popdicts.
        return

if __name__ == "__main__":
    params_ca = dict(name = 'toronto', n=20000, com_contacts=20) # large city
    params_cb = dict(name = 'miss', n=10000, com_contacts=10) # medium city
    params_cc = dict(name = 'milton', n=5000,  com_contacts=10) # small city
    pop_mod = RegionalBehaviourModel(None, *(params_ca, params_cb, params_cc))
