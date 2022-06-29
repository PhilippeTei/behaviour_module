class people
class school
class home
class workplace
class city

class locations{
    self.schools = {0: school_0, 1: school_1, ...}
    self.homes = ...
}

class ContactScript # ordered dictionary with keys being dates, values being arrays of contacts. 
class AllContacts
class Interventions

# Core functions?

# Init Contacts
all_contacts = AllContacts(params_AC)
locs = locations(params_LS)
all_contacts.init_home_contacts(locs)
all_contacts.init_school_contacts(locs)
all_contacts.init_workplace_contacts(locs)
all_contacts.init_community_contacts(locs)

class AllContacts{
    def __init__()
        self.home_contacts = ContactScript()
        self....

    # Provide Contacts
    def get_contacts(day)
        return np.cat(self.home_contacts, ...)
    def get_contacts_list()
}

class Interventions(friend class AllContacts){
    def __init__()
        self.all_contacts = pointer_to_AllContacts
    # Modify the contacts
    def quarantine(){
        # Reduce all community contacts. 
        self.all_contacts.community_contacts[day_start:day_end] = np.empty(day_end-day_start, 1)
    }
}