#### Summary ####
pars = dict(n = 10000, rand_seed=1, country_location = 'canada', state_location = 'Ontario', location = 'toronto', sheet_name = 'United States of America')

or 

pars = dict(n = 10000, rand_seed=1, country_location = 'canada')

In the second option, defaults for state_location, etc are filled out in defaults.py..

sheet_name refers to the country name-indexed sheet for each of the MUestimates_home.obj, etc. 

country-specific inputs are located in behaviour/data/country.json. 
    - You can have children locations, and use them using the state_location and/or location parameters. 

You can access the json file contents using load_location(). 

#### New Parameters ####
- Age-income distribution
- SW-Age distribution
- SW-income distribution

#### Parameter Loading Architecture ####
- Load and do preliminary processing on the parameters, with the contact matricies. Store them also like the CM's.  
    - Load 2D structures from files
    - Load 1D directly from the json. 
        - Brackets, etc.
- Perform all the computation (calculating normalizer, etc) when it's required. 


#### On a few data structures ####
age_by_brackets: list. Index is age, value is which bracket it's in. 

expected_age_dist = smoothed distribution of probability vs age, for ages 0 to 100 inclusive. 

age_brackets: dict {0:[0,1,2,3,4], ... } if you have 5-year brackets.
- Last bracket (index 15) has ages 75 to 100 inclusive. 
