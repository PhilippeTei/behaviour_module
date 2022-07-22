import numpy as np
import sciris as sc

def group_uids_by_income_age_brackets(age_bracs, inc_bracs, age_by_uid, fam_income_by_uid):
    # Group UIDs by income and age brackets. 
    ppl_income_age = {}
    for i in range(len(inc_bracs)):
        ppl_income_age[i] = {i:[] for i in range(len(age_bracs))} # Each cell contains a list of people we'll append to. 

    for uid in age_by_uid:
        person = uid

        # Get brackets. 
        income = fam_income_by_uid[uid]
        age = age_by_uid[uid]

        # See which bracket the income calls into. 
        b_i = None
        for i, b_inc in enumerate(inc_bracs):
            if income < b_inc:
                b_i = i
                break
        # If still not assigned, assign to last bracket. 
        if b_i is None:
            b_i = len(inc_bracs) - 1
        
        # same for age.
        b_a = None
        for i, b_age in enumerate(age_bracs):
            if age < b_age:
                b_a = i
                break
        if b_a is None:
            b_a = len(age_bracs) - 1

        ppl_income_age[b_i][b_a].append(person)
    
    return ppl_income_age


def allocate_smartwatches(pars, age_by_uid, fam_income_by_uid):
    use_prob = pars.sw_params.dist_sw_probabilstically

    # Initialize to false, for all UID's. UID's are the keys of age_by_uid. 
    ret = {uid:False for uid in age_by_uid}

    if use_prob:
        # Allocate smartwatches for each person according to P(W|A,I). 
        # We approximate this using P(W|A)*P(W|I)*normalizer, where the normalizer assumes we match the overall P(W). 
        A_I_joint = pars.age_income_dist
        p_w_given_i = pars.sw_params.p_w_given_i
        p_w_given_a = pars.sw_params.p_w_given_a
        p_w = pars.sw_params.p_w
        ages = pars.sw_params.age_bracs
        incomes = pars.sw_params.income_bracs

        # Calculate the normalizer. First, the denominator. 
        denom = 0
        for i in range(len(ages)):
            for j in range(len(incomes)):
                denom += p_w_given_i[j] * p_w_given_a[i] * A_I_joint[i,j]

        normalizer = p_w/denom

        # Make dictionaries relating age to p_w_given_a and income to p_w_given_i.
        p_w_given_a_by_age = dict()
        p_w_given_i_by_income = dict()
        for i in range(len(ages)):
            p_w_given_a_by_age[ages[i]] = p_w_given_a[i]
        for j in range(len(incomes)):
            p_w_given_i_by_income[incomes[j]] = p_w_given_i[j]
        
        # Now give the smartwatches!
        for uid in age_by_uid:
            age = age_by_uid[uid]
            income = fam_income_by_uid[uid]
            p_w_given_a_i = p_w_given_a_by_age[age] * p_w_given_i_by_income[income] * normalizer
            if np.random.random() < p_w_given_a_i:
                ret[uid] = True
        return ret

    else:
        p_w_given_i = pars.sw_params.p_w_given_i
        p_w_given_a = pars.sw_params.p_w_given_a
        age_bracs = pars.sw_params.age_bracs
        inc_bracs = pars.sw_params.income_bracs

        # First, put all the UID's into the 2d datastructure. 
        ppl_income_age = group_uids_by_income_age_brackets(age_bracs, inc_bracs, age_by_uid, fam_income_by_uid)

        # Get the totals for each axis. 
        totals_income = {i:0 for i in range(len(inc_bracs))}
        totals_age = {i:0 for i in range(len(age_bracs))}
        # For each income bracket, get the total number of people in that bracket.
        for i in range(len(inc_bracs)):
            for j in range(len(age_bracs)):
                totals_income[i] += len(ppl_income_age[i][j])

        for i in range(len(age_bracs)):
            for j in range(len(inc_bracs)):
                totals_age[i] += len(ppl_income_age[j][i])

        # Calculate the number of watches to distribute for each age group. 
        to_distribute_by_age = {i: int(totals_age[i]*p_w_given_a[i]) for i in range(len(age_bracs))}
        to_distribute_by_inc = {i: int(totals_income[i]*p_w_given_i[i]) for i in range(len(inc_bracs))}

        # Now, allocate the watches.
        for i_brac in to_distribute_by_inc:
            i_count = to_distribute_by_inc[i_brac]

            for i in range(i_count):
                alloc = False
                while not alloc:
                    # Draw an age based on to_distribute_by_age. 
                    # If there's no uid in that age group, draw again.
                    if sum(to_distribute_by_age.values()) <= 0:
                        a_brac = np.random.choice(len(age_bracs)) # If to_dist_by_age is 0, uniformly distribute to any age group.
                    else:
                        counts_dist = np.array(list(to_distribute_by_age.values()))
                        p = counts_dist/np.sum(counts_dist)
                        a_brac = np.random.choice(np.arange(len(age_bracs)), p=p)

                    if len(ppl_income_age[i_brac][a_brac]) > 0:
                        uid = ppl_income_age[i_brac][a_brac].pop() # Remove last element. (Doesn't matter)
                        alloc = True
                        # Subtract 1 or clip at 0. 
                        to_distribute_by_age[a_brac] = max(0, to_distribute_by_age[a_brac]-1)
                        to_distribute_by_inc[i_brac] = max(0, to_distribute_by_inc[i_brac]-1)
                        ret[uid] = True
        
        return ret

def allocate_household_incomes(pars, age_by_uid, homes_by_uids, homes):
    ret = dict()
    A_I_joint = pars.age_income_dist
    p_age = np.sum(A_I_joint, axis=1)
    all_incs = pars.ai_inc_bracs    

    for i, home_ages in enumerate(homes): # TODO: I think homes contains the age of each person per home.
        # TODO: I think that home is the key. 

        # Assume the age of the reference individual is simply the highest age in the household.
        hh_holder_age = max(home_ages)

        # Calculate P(I|A); a vector of probabilities of each income, given the age.
        cur_joint = A_I_joint[hh_holder_age,:]
        p_inc_given_age = cur_joint / p_age[hh_holder_age]

        # Sample an income from this distribution.
        hh_income = np.random.choice(all_incs, p=p_inc_given_age)

        for uid in homes_by_uids[i]:
            ret[uid] = hh_income
    
    return ret 

def update_pars(default_pars, pars):
    for key, item in pars.items():
        default_pars[key] = item
    return default_pars

def make_pars():
    # Make default pars for the behaviour model. 
    ret = sc.objdict(
            n=None,
            max_contacts=None,
            ltcf_pars=None,
            school_pars=None,
            with_industry_code=False,
            with_facilities=False,
            use_default=False,
            use_two_group_reduction=True,
            average_LTCF_degree=20,
            ltcf_staff_age_min=20,
            ltcf_staff_age_max=60,
            with_school_types=False,
            school_mixing_type='random',
            average_class_size=20,
            inter_grade_mixing=0.1,
            average_student_teacher_ratio=20,
            average_teacher_teacher_degree=3,
            teacher_age_min=25,
            teacher_age_max=75,
            with_non_teaching_staff=False,
            average_student_all_staff_ratio=15,
            average_additional_staff_degree=20,
            staff_age_min=20,
            staff_age_max=75,
            com_contacts=20,
            com_dispersion=None,
            rand_seed=None,
            country_location=None,
            state_location=None,
            location=None,
            sheet_name=None,
            household_method='infer_ages',
            smooth_ages=False,
            window_length=7,
            do_make=True,
            as_region = False,
            base_uid=0,
            init_incomes_and_watches=True,
            dist_sw_probabilstically=False)
    return ret