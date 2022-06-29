import numpy as np
import sciris as sc
from . import data_distributions as spdata


class BehaviourModelParams():
    def __init__(self) -> None:
        self.h = True
        self.w = True
        self.c = True
        self.s = True
        self.o = False # Other

        # Work Options
        self.work_contacts = 20 # average # contacts at work
        
        # Other misc
        self.rand_seed = None

class BehaviourModel():
    def __init__(self,
        n, 
        params = BehaviourModelParams()
        ):
        """
        Generate structures according to contact matrices. 
        """
        self.n = int(n)
        self.structures = None
        self.load_data()

        return

    def load_data(self):
        
        # General parameters
        datadir                         = self.datadir
        location                        = self.location
        state_location                  = self.state_location
        country_location                = self.country_location
        n                               = self.n
        sheet_name                      = self.sheet_name
        max_contacts                    = self.max_contacts
        use_default                     = self.use_default
        loc_pars                        = self.loc_pars

        # Age distribution parameters
        smooth_ages                     = self.smooth_ages
        window_length                   = self.window_length

        # Household parameters
        household_method                = self.household_method

        # LTCF parameters
        use_two_group_reduction         = self.ltcf_pars.use_two_group_reduction
        average_LTCF_degree             = self.ltcf_pars.average_LTCF_degree
        with_facilities                 = self.ltcf_pars.with_facilities
        ltcf_staff_age_min              = self.ltcf_pars.ltcf_staff_age_min
        ltcf_staff_age_max              = self.ltcf_pars.ltcf_staff_age_max

        # School parameters
        with_school_types               = self.school_pars.with_school_types
        school_mixing_type              = self.school_pars.school_mixing_type
        average_class_size              = self.school_pars.average_class_size
        inter_grade_mixing              = self.school_pars.inter_grade_mixing
        average_student_teacher_ratio   = self.school_pars.average_student_teacher_ratio
        average_teacher_teacher_degree  = self.school_pars.average_teacher_teacher_degree
        teacher_age_min                 = self.school_pars.teacher_age_min
        teacher_age_max                 = self.school_pars.teacher_age_max
        with_non_teaching_staff         = self.school_pars.with_non_teaching_staff
        average_student_all_staff_ratio = self.school_pars.average_student_all_staff_ratio
        average_additional_staff_degree = self.school_pars.average_additional_staff_degree
        staff_age_min                   = self.school_pars.staff_age_min
        staff_age_max                   = self.school_pars.staff_age_max

        # Load and store the expected age distribution of the population
        age_bracket_dist = spdata.read_age_bracket_distr(**loc_pars)  # age distribution defined by bins or age brackets
        expected_age_dist = spdata.get_smoothed_single_year_age_distr(**loc_pars, window_length=self.window_length)
        self.expected_age_dist = expected_age_dist
        expected_age_dist_values = [expected_age_dist[a] for a in expected_age_dist]
        self.expected_age_dist_values = expected_age_dist_values

        # Load and store the age brackets
        age_brackets = spdata.get_census_age_brackets(**loc_pars)
        self.age_brackets = age_brackets
        # mapping
        age_by_brackets = spb.get_age_by_brackets(age_brackets)
        self.age_by_brackets = age_by_brackets

        # Load the contact matrix
        contact_matrices = spdata.get_contact_matrices(datadir, sheet_name=sheet_name)
        # Store expected contact matrices
        self.contact_matrices = contact_matrices

        # Load age brackets, and mapping dictionary that matches contact matrices
        contact_matrix_shape = contact_matrices[list(contact_matrices.keys())[0]].shape
        contact_matrix_row = contact_matrix_shape[0]

        cm_age_brackets = spdata.get_census_age_brackets(**loc_pars, nbrackets=contact_matrix_row)
        self.cm_age_brackets = cm_age_brackets
        cm_age_by_brackets = spb.get_age_by_brackets(cm_age_brackets)
        self.cm_age_by_brackets = cm_age_by_brackets
        

    def initialize(self):
        # Initialize people and structures. Place people into structures. 
        self.expected_age_dist = spdata.get_smoothed_single_year_age_distr(**loc_pars, window_length=self.window_length)

    