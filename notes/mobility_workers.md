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


structures: simply modify workers_by_age_to_assign_count. 
    - Requires global uid's.

valid_workers = get_valid_workers()

per_city:
    to_donate_uid_lists[city] = pop_donated_workers(workplace_mixing_pars) # Also removes them.

incoming_uid_lists = generate_incoming_uid_lists(to_donate_uid_lists)

per_city:
    valid_workers = update_valid_workers(incoming_uid_lists[city])

DATA STRUCTURES:
Say miss has uids btwn 1000 and 2000. Maybe it's time to transition UID's to global sooner.
incoming_uid_lists = {
    "miss": [0] // People coming into mississauga for work.
    "milton": ...
}

to_donate = {
    "miss": [110, 3521, 5102, 4, 391]
    "milton": [38, 125, 452, 6844]
}

## Questions to resolve ##
- How to also pass ages? Is there any worker info other than ages to pass?

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