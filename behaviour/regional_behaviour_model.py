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

class RegionalBehaviourModel(BehaviourModel):
    def __init__(self, mixing_pars = None, *args):
        if mixing_pars == None:
            mixing_pars = load_default_mixing_pars(len(args))
        
        # Init cities
        self.cities = sc.objdict()
        for city_params in args: # args is a list.
            cur_city = city_params.pop('name')
            city_params["as_region"] = True
            self.cities[cur_city] = BehaviourModel(city_params)

if __name__ == "__main__":
    params_ca = dict(name = 'toronto', n=20000, com_contacts=20) # large city
    params_cb = dict(name = 'miss', n=10000, com_contacts=10) # medium city
    params_cc = dict(name = 'milton', n=5000,  com_contacts=10) # small city
    pop_mod = RegionalBehaviourModel(None, *(params_ca, params_cb, params_cc))
