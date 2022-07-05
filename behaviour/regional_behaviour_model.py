from . import behaviour_model as bm
import numpy as np
import sciris as sc
import covasim.utils as cvu

class RegionalBehaviourModel(bm.BehaviourModel):
    def __init__(self, params_com_mixing = None, params_work_mixing = None, *args):

        self.completed_layers = []
        self.reg_pars = sc.dcp(args) # copy these args since we'll modify later
        self.augment_pars()
        args = sc.dcp(self.reg_pars) # reflect these augmentations on args. 
        
        self.params_work_mixing = params_work_mixing
        self.params_com_mixing = params_com_mixing
        self.process_mixing_params()

        self.init_total_popdict_skele()

        # Init cities
        self.regs = sc.objdict() # reg stands for region.
        for reg_params in args: # args is a list.
            cur_reg = reg_params.pop('name')
            reg_params["as_region"] = True
            self.regs[cur_reg] = bm.BehaviourModel(reg_params) # inits. 

        # Allocate people to their structures. TODO: coupled initialization for workplaces.
        for _, rsim in self.regs.items():
            rsim.load_pars_and_data()
            rsim.make_structures()
        
        # Make connections. 
        for _, rsim in self.regs.items():
            rsim.init_contact_structure()
            rsim.make_home_contacts()
            rsim.make_school_contacts()
            rsim.make_work_contacts()
        
        self.make_mixed_community_contacts()

        self.aggregate_regions() # make a popdict usable by covasim.

    def process_mixing_params(self):
        # first, community mixing. We assume there's always inter-community movement. 

        if self.params_com_mixing == None:
            print("Community mixing parameters not given; initializing defaults...")
            self.load_default_mixing_pars(len(self.reg_pars))
        
        if self.params_work_mixing != None:
            # then, workplace mixing. Check all keys are normalized.
            for _, reg in self.params_work_mixing.items():
                if reg["leaving"] > 1:
                    raise ValueError("Must Normalize!")
                
                dests = reg["dests"]
                for _, dest in dests.items():
                    if dest > 1:
                        raise ValueError("Must Normalize!")

    def augment_pars(self):
        # first, number the cities, Then, assign them base-UID's, for later aggregation.
        i = 0
        cur_offset = 0
        for city_par_set in self.reg_pars:
            city_par_set['city_id'] = i
            city_par_set['base_uid'] = cur_offset
            i += 1
            cur_offset += city_par_set['n']

    def load_default_mixing_pars(self, num_cities):
        """
        Populate workplace and community mixing matricies. (mm)
        """

        self.params_com_mixing = {}
        come_from_cur = 0.8
        come_from_others = 0.2
        
        ret = (come_from_others/(num_cities-1))* \
        np.ones((num_cities, num_cities))

        for i in range(ret.shape[0]):
            ret[i][i] = come_from_cur

        mixing_layers = ["C", "W"]

        for k in mixing_layers:
            self.params_com_mixing[k] = ret

    def init_total_popdict_skele(self):
        # calculate total pop size.
        total_n = 0
        use_ltcf = False # Will need rewriting later when we roll this in. Principle: don't develop what you won't test. 

        for city_params in self.reg_pars:
            total_n += city_params['n']
        
        if use_ltcf:
            layer_keys = ['H', 'S', 'W', 'C', 'LTCF']
        else:
            layer_keys = ['H', 'S', 'W', 'C']

        self.total_popdict = {}

        for uid in range(total_n):
            self.total_popdict[uid] = {}
            self.total_popdict[uid]['age'] = None
            self.total_popdict[uid]['sex'] = None
            self.total_popdict[uid]['loc'] = None
            self.total_popdict[uid]['contacts'] = {}
            if use_ltcf:
                self.total_popdict[uid]['ltcf_res'] = None
                self.total_popdict[uid]['ltcf_staff'] = None
            self.total_popdict[uid]['hhid'] = None
            self.total_popdict[uid]['hhincome'] = None
            self.total_popdict[uid]['scid'] = None
            self.total_popdict[uid]['sc_student'] = None
            self.total_popdict[uid]['sc_teacher'] = None
            self.total_popdict[uid]['sc_staff'] = None
            self.total_popdict[uid]['sc_type'] = None
            self.total_popdict[uid]['sc_mixing_type'] = None
            self.total_popdict[uid]['wpid'] = None
            self.total_popdict[uid]['wpindcode'] = None
            if use_ltcf:
                self.total_popdict[uid]['ltcfid'] = None
            for k in layer_keys:
                self.total_popdict[uid]['contacts'][k] = set()

    def make_mixed_community_contacts(self):
        """
        Make random community contacts, with mixing specified by the mixing matrix
        Result: self.total_popdict[*]['contacts']['C'] is populated, where * is all UIDs accross all regions.
        Refactoring TODO: discard self.reg_pars and store that information in the actual region objects. 
        """
        n_regs = len(self.reg_pars)
        i_cur_reg = 0
        # For each region
        for k_reg in self.regs:
            reg = self.regs[k_reg]
            base = self.reg_pars[i_cur_reg]['base_uid']
            dispersion = reg.input_pars['com_dispersion']

            n = reg.input_pars['n']
            contacts = reg.input_pars['com_contacts']
            total_contacts = n*1.1*contacts # adjust for overshoot

            contacts_list = []

            for i_reg in range(n_regs):
                # The proportion of community contacts in cur_reg coming from i_reg.
                prop = self.params_com_mixing['C'][i_cur_reg][i_reg]
                
                # Draw people, add cur base.
                cur_base = self.reg_pars[i_reg]['base_uid']
                cur_n = self.reg_pars[i_reg]['n']
                people_from_city_i = cvu.choose_r(max_n = cur_n, n=total_contacts*prop)
                people_from_city_i += cur_base

                contacts_list = [*contacts_list, *list(people_from_city_i)]
            contacts_list = np.array(contacts_list)
            np.random.shuffle(contacts_list)
            i_cur_reg += 1
        
            # Distribute this list of contacts to the people.
            if dispersion is None:
                contacts_per_person = cvu.n_poisson(contacts, n)
            else:
                contacts_per_person = cvu.n_neg_binomial(rate=contacts, dispersion=dispersion, n=n)
            
            cumu = 0

            for uid in range(n):
                self.total_popdict[base+uid]['contacts']['C'] = contacts_list[cumu:cumu + contacts_per_person[uid]]
                cumu += contacts_per_person[uid]

        self.completed_layers.append('C')
        # TODO: Tests: 
        # Should be able to recreate the mixing matrix.
        # Numbe of contacts per city should be pop_size*20.

    def aggregate_regions_old(self):
        # Transition popdicts from the independently initialized parts into total_popdict. 
        # Different regions aren't yet assumed to have shifted UIDs. 
        """
        i_cur_reg = 0
        for reg in self.regs:
            base = self.reg_params[i_cur_reg]['base_uid']
            i_cur_reg += 1
        """
        # Can't blindly merge all dicts because some fields are already populated. (by self.mixing_* funcs)
        i_cur_reg = 0
        for k_reg in self.regs: # loop through all regions. ....
            reg = self.regs[k_reg]
            base = self.reg_pars[i_cur_reg]['base_uid']
            n = self.reg_pars[i_cur_reg]['n']
            for uid in range(n): # loop through all user id's ...
                adjusted_uid = uid + base

                for key, val in reg.popdict[uid].items(): # loop through all attributes of the person ...
                    if key == 'contacts': # don't over-write contacts that were intialized in this class. 
                        for layer in val:
                            if layer not in self.completed_layers:
                                self.total_popdict[adjusted_uid][key][layer] = val[layer]

                    else:
                        self.total_popdict[adjusted_uid][key] = val
            i_cur_reg += 1

        self.completed_layers = list(self.total_popdict[0]['contacts'].keys()) # Done all layers.

        return
    
    def aggregate_regions(self):
        # The different regions already have shifted UIDs.
        # Transition popdicts from the independently initialized parts into total_popdict. 

        for k_reg in self.regs:
            reg = self.regs[k_reg]
            for uid, person in reg.popdict.items():
                for key, val in person.items():
                    if key == 'contacts':
                        for layer in val:
                            if layer not in self.completed_layers:
                                self.total_popdict[uid][key][layer] = val[layer]
                    else:
                        self.total_popdict[uid][key] = val
        self.completed_layers = list(self.total_popdict[0]['contacts'].keys()) # Done all layers.
        return

if __name__ == "__main__":
    params_ca = dict(name = 'toronto', n=20000, com_contacts=20) # large city
    params_cb = dict(name = 'miss', n=10000, com_contacts=10) # medium city
    params_cc = dict(name = 'milton', n=5000,  com_contacts=10) # small city
    pop_mod = RegionalBehaviourModel(None, *(params_ca, params_cb, params_cc))
