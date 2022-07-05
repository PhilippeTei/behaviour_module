import numpy as np
import sciris as sc

def allocate_household_incomes(pars, age_by_uid, homes_by_uids, homes):
    ret = dict()
    for uid in age_by_uid:
        ret[uid] = 70000
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
            base_uid=0)
    return ret