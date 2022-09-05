
import string

# Type aliases for readability
PrereqOption = dict[str]
UnitCode = str


class Unit:
    """
    Stores unit information.
    Unit requisites information will be stored using Requisite subclass in self.requisites.
    """
    def __init__(self, unit_code : str, name : str, credits : int = 6):
        """
        Construct an unit instance.


        @param unit_code: String for UNIT CODE (i.e FIT1045). This acts as unique identifier key for accessing the Unit from the database.
        @param name: String for UNIT NAME (i.e Introduction to C++)
        @param credits: Integer value for credit points (defaults to 6 as most Monash units worth 6 points)
        """
        self.unit_code : str = unit_code
        self.name : str = name
        self.credits : int = credits

        self.description : str = ""
        self.requisites = self.Requisites(self)

        self.offerings = self.Offerings(self)

    def set_unit_code(self, unit_code):
        """Set new string for unit code."""
        self.unit_code : str = unit_code

    def set_name(self, name : str):
        """Set new string for unit name."""
        self.name : str = name

    def set_credits(self, credits : int):
        """Set new integer for unit credit points award."""
        self.credits : int = credits  

    def set_description(self, description : str):
        """Set new string for unit description."""
        self.description : str = description

    def get_unit_code(self) -> str:
        """Return unit code string."""
        return self.unit_code
    
    def get_name(self) -> str:
        """Return unit name string."""
        return self.name
    
    def get_credits(self) -> int:
        """Return unit credits award integer."""
        return self.credits
    
    def get_description(self) -> str:
        """Return unit description string."""
        return self.description

    def get_offerings(self) -> list[dict[str]]:
        return self.offerings

    def __repr__(self) -> str:
        """
        Printable representation of the unit.
        `FIT1045 Introduction to algorithms and Python`
        """
        return f'{self.unit_code} {self.name}'

    def __str__(self) -> str:
        """
        String representation of the unit.
        `FIT1045 Introduction to algorithms and Python`
        """
        return f'{self.unit_code} {self.name}'

    def __eq__(self, other) -> bool:
        """
        2 Unit objects are equal if they share the same unit code, name and credits award.
        """
        return self.unit_code == other.unit_code and self.name == other.name and self.credits == other.credits

    class Offering:
        """;
        Unit offering:
        # Campus: CLAYTON, CAULFIELD, MALAYSIA, etc
        # Period: S1, S2, etc
        # Mode: ONLINE, ON-CAMPUS, etc
        """

        def __init__(self, period : str, campus : str, mode : str):
            self.campus: str = campus
            self.period : str = period
            self.mode : str = mode

        def __repr__(self) -> str:
            return f'{self.period}-{self.campus}-{self.mode}'

        def __str__(self) -> str:
            return f'{self.period}-{self.campus}-{self.mode}'

    class Offerings:
        def __init__(self, parent_unit):
            self.parent_unit = parent_unit
            self.all_offerings = []

        def get_all_offerings(self):
            return self.all_offerings

        def add_offering(self, offering):
            offering.campus : str = offering.campus.upper()
            offering.mode : str = offering.mode.upper()
            offering.period : str = offering.period.upper()
            self.all_offerings.append(offering)

        def add_offerings(self, offerings : list):
            for offering in offerings:
                self.add_offering(offering)

        def get_offerings_by_campus(self, campus : str) -> list:
            campus_offerings = []
            for offering in self.all_offerings:
                if offering.campus == campus.upper():
                    campus_offerings.append(offering)
            return campus_offerings

        def get_offerings_by_mode(self, mode : str) -> list:
            mode_offerings = []
            for offering in self.all_offerings:
                if offering.mode == mode.upper():
                    mode_offerings.append(offering)
            return mode_offerings

        def get_offerings_by_period(self, period : str) -> list:
            period_offerings = []
            for offering in self.all_offerings:
                if offering.period == period.upper():
                    period_offerings.append(offering)
            return period_offerings

    class Requisites:
        """
        Stores requisite information for a parent Unit.
        Provides methods to print information in readable format.
        """
        def __init__(self, parent_unit):
            """
            Construct the Requisite subclass object.
            Sets the parent unit for access to upper level information (parent unit code).
            """
            self.parent_unit = parent_unit
            self.prerequisites: list[PrereqOption] = [] # [{'NumReq':int, units:list[str]}, ...]
            self.permission_required: bool = False
            self.prohibitions: list[UnitCode] = [] # [MTH1020, PHS1030...]
            self.corequisites: list[UnitCode] = [] # Same as above

        def set_prerequisites(self, prereqs : list[PrereqOption]):
            """Set list of dictionaries of prerequisite routes/options."""
            self.prerequisites = prereqs

        def set_permission_required(self, permission_required : bool):
            """Set boolean of additional permission requirement to enrol in unit."""
            self.permission_required = permission_required

        def set_prohibitions(self, prohibitions : list[UnitCode]):
            """Set list of string for names of prohibited units."""
            self.prohibitions = prohibitions

        def set_corequisites(self, coreqs : list[UnitCode]):
            """Set list of string for names of corequisite units."""
            self.corequisites = coreqs

        def get_prerequisites(self) -> list[PrereqOption]:
            """Get list of dictionaries of prerequisite routes/options."""
            return self.prerequisites
        
        def get_permission_required(self) -> bool:
            """Get boolean of additional permission requirement to enrol in unit."""
            return self.permission_required
        
        def get_prohibitions(self) -> list[UnitCode]:
            """Get list of string for names of prohibited units."""
            return self.prohibitions

        def get_corequisites(self) -> list[UnitCode]:
            """Get list of string for names of corequisite units."""
            return self.corequisites

        def remove_prerequisites(self):
            """Remove all prerequisites by emptying the list."""
            self.prerequisites = []
        
        def remove_prohibitions(self):
            """Remove all prohibitions by emptying the list."""
            self.prohibitions = []

        def remove_corequisites(self):
            """Remove all corequisites by emptying the list."""
            self.corequisites = []

        def print_prerequisites(self):
            """Print all prereqs in readable format."""
            if len(self.prerequisites) == 0:
                print(f'{self.parent_unit.unit_code} has no prerequisites.')
            else:
                print(f'{self.parent_unit.unit_code} has {len(self.prerequisites)} prerequisite options:')
                
                i = 1
                for option in self.prerequisites:
                    option_str = f'\t{i}. Complete {option["NumReq"]} units: {", ".join(option["units"])}.'
                    print(option_str)
                    i += 1

        def print_permission_requirement(self):
            """Print all permission requirement in readable format."""
            print(f'{(f"{self.parent_unit.unit_code} requires further permission to enrol.") if self.permission_required else f"No permissions required for {self.parent_unit.unit_code}."}')

        def print_corequisites(self):
            """Print all coreqs in readable format."""
            if len(self.corequisites) == 0:
                print(f'{self.parent_unit.unit_code} has no corequisites.')
            else:
                print(f'{self.parent_unit.unit_code} has {len(self.corequisites)} corequisites: {", ".join(self.corequisites)}.')

        def print_prohibitions(self):
            """Print all prohibitions in readable format."""
            if len(self.prohibitions) == 0:
                print(f'{self.parent_unit.unit_code} has no prohibitions.')
            else:
                print(f'{self.parent_unit.unit_code} has {len(self.prohibitions)} prohibitions: {", ".join(self.prohibitions)}.')

        # Methods aliases for usability
        requires_permission = get_permission_required 
        set_prereqs = set_prerequisites
        get_prereqs = get_prerequisites
        remove_prereqs = remove_prerequisites
        print_prerequs = print_prerequisites

        set_coreqs = set_corequisites
        get_coreqs = get_corequisites
        remove_coreqs = remove_corequisites
        print_coreqs = print_corequisites

        set_prohibs = set_prohibitions
        get_prohibs = get_prohibitions
        remove_prohibs = remove_prohibitions
        print_prohibs = print_prohibitions


def test():

    fit = Unit('fit1045', 'python')

    pr = [
            {'NumReq' : 2,
            'units' : ['MAT1830','MAT1841']},

            {'NumReq' : 1,
            'units' : ['MTH1030']}
        ] 

    fit.requisites.set_prereqs(pr)
    fit.requisites.set_coreqs(['FIT1047','FIT1008'])
    fit.requisites.set_prohibs(['FIT1055'])
    fit.requisites.set_permission_required(True)
    fit.requisites.print_prerequisites()
    fit.requisites.print_permission_requirement()
    fit.requisites.print_corequisites()
    fit.requisites.print_prohibs()
    fit.offerings.add_offerings(
        [Unit.Offering('S1','CLAYTON','ONLINE'), 
        Unit.Offering('S1','CLAYTON','ON-CAMPUS'),
        Unit.Offering('S2','CLAYTON','ONLINE'),
        Unit.Offering('S2','CLAYTON','ON-CAMPUS'),
        Unit.Offering('S1','CAULFIED','ONLINE'), 
        Unit.Offering('S1','CAULFIED','ON-CAMPUS'),
        Unit.Offering('S2','CAULFIED','ONLINE'),
        Unit.Offering('S2','CAULFIED','ON-CAMPUS')])
    print(fit.offerings.get_all_offerings())
    print(fit.offerings.get_offerings_by_campus('clayton'))
    print(fit.offerings.get_offerings_by_period('s1'))
    print(fit.offerings.get_offerings_by_mode('online'))


#test()