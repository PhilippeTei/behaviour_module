#### Data Structure ####

{"Toronto": {"p_leaving": 0.05, "dest": 
    {"miss": 0.5, "milt": 0.5}}
}
or: 

columns and rows: A,B,C. 


#### What kind of data is available? ####

uk, california, new york
- uk: Inflow and outflow information between all local authorities (around city-size) (tells the # people). https://www.nomisweb.co.uk/census/2011/WU03EW/chart/1132462136 
    - https://www.nomisweb.co.uk/census/2011/data_finder is great source
    - visualizer works but the csv download is broken in abv link
    - csv download works in this link: https://www.nomisweb.co.uk/census/2011/wp7103ew (but only seems to have "people working outside the county")

- california/usa: exact numbers of people going from one county to another, for every combination of counties. 
    - This is also mathematically solvable.
https://www.census.gov/data/tables/2015/demo/metro-micro/commuting-flows-2015.html

- mississauga: https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/page.cfm?Lang=E&Geo1=CSD&Code1=3521005&Geo2=CD&Code2=3521&SearchText=Mississauga&SearchType=Begins&SearchPR=01&B1=Journey%20to%20work&TABID=1&type=0

(tells us how many residents of Mississauga go elsewhere)

#### What kind of features will we need? ####

TODO: % and # people both fine. 

Bottom line:

    A | B | C
A | - | 4 | 2
B | 1 | - | 3
C | 4 | 1 | -

How many people go to each city?

Sample parameters: 
- In percentages, if the ABM has smaller populations. 
    - Can input above in percents or numbers.
    - Would then require # of region population leaving.

Input: either normalized or raw numbers. 
Processing: 
1. Normalize the numbers
2. Rescale to the ABM population 
3. Distribute workers. 


#### Dev ####
1. Create test.py & specify interface.
2. Implement. 
2.1. Add structural stuff. (parameter passing, if multi_region in get_valid_workers, etc)
2.2. Implement algorithm. (Simply put workers into the age brackets and shuffle)
2.3. Test it. 
    <!-- a) Disable inter-region community and workplace & init all infections in 1 place. See no spread. Now enable workplace. See spread. -->
    b) Like for community contact matrix: generate one for work and an expected and calculate the percentages. 


#### 2.1. structures for multi-region ####
1. init homes, ltcfs, schools. But no workers yet. 
2. get workers. alloc to schools, ltcfs, work.
3. build package for connection-building. 

for each region: 
    # pass all the objects around by reference and directly modify them
    work_structures[region] = valid_workers = get_valid_workers()

    # choose to donate some workers. 
    nw2d = get_nw2d(params_work_mixing[region]) # number of workers to donate. 
    # get list of uids to donate. Get a pool of outgoing mobility workers per city.
    mobility_workers[region] = sample_mobility_workers(work_structures, nw2d)
    
# Now for each region, allocate the folks. Using the script. 
for each region:
    script = make_script(mixing_params[region]) # looks like 000111020121010101001
The script idea is ru b/c it requires modifying each distribution function separately. Let's modify the data structures.

// Looking at assign_rest_of_workers:
- keep total counter or pop from the script. 
- reference individuals must be native. 
- for each input variable, set them by reference to work_structures[region].*

## Tests. ##
- Structures: Plot workplace ID vs # mobility workers in the company. 
    - Implement global workplace ID; do this for all regions.
- Structures: Re-create the matrix.
- Contacts: Disable inter-community. Check no spread. Enable employment. Ensure spread.

#### DATA STRUCTURES: ####

n_leaving = {
    "miss": 4000,
    "toronto": 500,
    "milton": 1020
}

uids_leaving = {
    "miss": [1,5,7]
    "toronto: [11,24,16,15],
    ...
}

going_to_coming_from = {
    "miss": 
    {
        "toronto": [11,15,16],
        "milton": [30,31,33],
        ...},
     "toronto":
     {
        "miss": [...],
        "milton":[...],
        ...
     },
     ...
}

potential_worker_uids_by_age = {
    0: [...],
    1: [...],
    ...
}

dests_a = {'miss':0.6, 'milton':0.4}
dests_b = {'toronto':0.9, 'milton':0.1}
dests_c = {'toronto':0.9, 'miss': 0.1}

params_work_mixing = dict(toronto = {"leaving":0.05, "dests":dests_a},
                          miss =    {"leaving":0.4, "dests":dests_b},
                          milton =  {"leaving":0.3, "dests":dests_c})

__ work_structs variables to update __
workers_by_age_to_assign_count: has all ages. o.w. same as below. 
potential_workers_ages_left_count: only contains ages 15 to 100, inclusive. 
-[C] potential_worker_uids: dict of uid:age. 
-[C] potential_worker_uids_by_age: {age:[uids]}

employment_rates: Don't need to update.
Ages 16 to 100, inclusive. This loaded from census data.
- only effects assign_teachers_to_schools()
    - where it's not actually used. 

## Questions to resolve ##
- How to count the number of people for the script?
    - count number of people left at this stage?
- Is it an ok assumption to only have as migrant workers those not at schools/ltcf's? 

## Making Contact Code ##
contacts: the issue is we do popdict["foreign_uid"].workplace_contacts = [], but "foreign_uid" doesn't exist yet. 
    - can simply make separate "popdict_foreign_uid" that gets aggregated later. Trivial? (Lots of code locations if affecting LTCF's, schools and other)

rsim.make_mixed_work_contacts()

self.popdict, self.fpopdict = spcnx.make_mixed_work_contacts(...)

make_mixed_work_contacts:
    - if uid > pop.n:
        cur_popdict = fpopdict # Points to same object.

## Shifting the BehaviourModule uids ##
- Should be possible because there's no examples of using array indicies as UID's. 
- To test: 
    - Compare with a total_popdict with community mixing, from before the update. 

Approach 1: 
- Create a function: behaviour_model.shift_uids(), which is called before finding the valid workers. 

** Approach 2: **
- Add a field base_id that gets factored into every UID consideration. Probably only need to do to the first few.  
    - households: assign_uids_by_homes

Either way:
- Community mixing: 
    - Remove base shifting.
    - Nevermind - keep the base shifting because we're not using the already-initted populations for this. 

- init_popdict_skele: 
    - make sexes into a dictionary.

 - make fam_income_by_uid a dictionary.

- Popdict aggregation: 
    - Remove base and contact shifting.


TODO: 
- Update hhid, scid, wpid's to global ones. 