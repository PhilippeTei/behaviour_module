Changes from Synthpops Notes:

#### Large Changes ####

- No LTCF. 

#### Coding Approach ####

- Copy-paste parameterization and data-loading code, deleting parts that we don't use. Do light refactorization.
    - LTCF stuff
    - Some redundant lines. 

- To be safe, write a test. 
    - Fix a seed
    - Do a reductive rather than additive approach. 
        - Make a copy of the entire Synthpops repo
        - Make one change at a time
        - After each change, run the test.
