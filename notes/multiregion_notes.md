mixing_pars = {
    {community_matrix: file_c.csv}
    {work_matrix: file_w.csv}
}

params_ca = {'name' = 'toronto', 'n'=20000, 'com_contacts'=20} # large city
params_cb = {'name' = 'miss',    'n'=10000, 'com_contacts'=10} # medium city
params_cc = {'name' = 'milton',  'n'=5000,  'com_contacts'=10} # small city

d = RegionalBehaviourModel(params_ca, params_cb ,params_cc ,mixing_pars=None)

How will this be used?
- covasim: translate popdict into people.
    - contacts: per layer contacts. Schools, etc.
        - p1 ordered
    - traits.

What structure needs to remain in the cities? (Within the regions object)
- Their parameters.
- Their generating structures.

What structure is visible from outside the reigions object?

structure: a) stored in the sub regions. 
    - have a foreigner option. 
        - take the foreigners, put them in the array, sample.
or:
           b) stored in total region.
    - communities, schools, etc. 
    - NONTRIVIAL. FIGURE OUT LATER. 

contacts: stored in the total region.


class RegionalBehaviourModel(BehaviourModel)
    def __init__(self, mixing_pars, **kwargs,){

        #### ADDITIONAL PARAMS ####
        self.contacts['community']['p1'] = []
        self.contacts[] ...
        (do for each layer. Directly populated by a make_mixed_... contact. 
        For individually inited, we have aggregate_regions())

        #### ####
        if mixing_pars == None: 
            self.load_default_mixing_pars()
        # Init cities
        for city_params in **kwargs: 
            cities[city_params['name']] = BehaviourModel(city_params, as_multi_region = True)
        # Alloc people to their structures.
        for city in cities:
            city.assign_homes()
            city.assign_schools()
        self.assign_workplaces(mixing_pars)

        # Make connections
        for city in cities: 
            make_h_connections()
            make_s_connections()
        self.assign_community_connections(cities, mixing_pars)
        self.assign_workplace_connections(cities, mixing_pars)

        # Last, make an interface that's compatible with covasim.
        pop_dict = self.make_pop_dict(cities)
    }

    # By default, have 80% contacts be in city, 20% outside.
    def load_default_mixing_pars(num_cities):
        come_from_cur = 0.8
        come_from_others = 0.2
        
        ret = (come_from_others/(n-1))*np.ones(num_cities, num_cities) + come_from_cur-come_from_others*np.identity(num_cities)
        
#### Changes to BehaviourModel ####
- a) Change BehaviourModel __init__ to not init the structures.
    - Or, add param "as_multi_region" = True. 

___
if as_multi_region == False:
    generate()
___

#### Calculating Statistics ####

def update_statistics():
    reg_sizes = [20k, 10k, 5k, 35k]
    reg_starts = [0, 20k, 5k, 0]
    reg_names = ["Toronto", "Mississauga", "Milton", ""] // cumulative called nothing so cur plotting works.

    #people.count -> param: start, end indexes. If none, do normal. O.W., return count_nonzero in the range. 
