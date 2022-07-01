mixing_pars = {
    {community_matrix: file_c.csv}
    {work_matrix: file_w.csv}
}

params_ca = {'name' = 'toronto', 'n'=20000, 'com_contacts'=20} # large city
params_cb = {'name' = 'miss',    'n'=10000, 'com_contacts'=10} # medium city
params_cc = {'name' = 'milton',  'n'=5000,  'com_contacts'=10} # small city

d = RegionalBehaviourModel(params_ca, params_cb ,params_cc ,mixing_pars=None)

class RegionalBehaviourModel(BehaviourModel)
    def __init__(self, mixing_pars, **kwargs,){
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