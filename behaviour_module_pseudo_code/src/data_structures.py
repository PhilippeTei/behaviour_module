from re import L
import numpy as np

class People():
    '''
    The class storing all of the agents. Stores traits of all agents in tabular format. 
    '''
    def __init__(self, n):
        # Set their traits. 
        self.ages = None
        self.incomes = None

class Layer():
    ''' 
    Stores the contacts for the layer but not the structure.

    Args:
        p1, p2: Take your entire list of contacts. p1 and p2 are the two individuals involved in each one. 
            Important: The pairs must be sorted by p1. 
        n: The number of agents.
    '''
    def __init__(self, p1, p2, index):
        self.p1 = p1
        self.p2 = p2
        # Keep original versions to recover changes. 
        self.p1_base = p1
        self.p2_base = p2

        self.contact_index = index
        self.contact_index_base = self.contact_index

    # def index_contacts():
    #     # Count contacts through p1. 
    #     # Set self.num_contacts. 
    #     return 

    def assert_ordered_pairs():
        return

class Structures():
    '''
    Stores structural information. Who's in what city? etc. 

    Usage: 
    
    '''

    def __init__(self, params):
        self.schools = {} # TODO: sciris ordered list
        # TODO: parse params. 
    def initialize():
        """
        if homes in structures_to_init:
            init_homes()
        if schools...
        """
