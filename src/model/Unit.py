
class Unit:
    """
    Stores unit information.
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

    def set_unit_code(self, unit_code):
        self.unit_code : str = unit_code

    def set_name(self, name : str):
        self.name : str = name

    def set_credits(self, credits : int):
        self.credits : int = credits  

    def set_description(self, description : str):
        self.description : str = description

    def get_unit_code(self) -> str:
        return self.unit_code
    
    def get_name(self) -> str:
        return self.name
    
    def get_credits(self) -> int:
        return self.credits
    
    def get_description(self) -> str:
        return self.description

    def __repr__(self):
        return f'{self.unit_code} {self.name}'

    def __str__(self):
        return f'{self.unit_code} {self.name}'

    def __eq__(self, other):
        return self.unit_code == other.unit_code and self.name == other.name and self.credits == other.credits


    class Requisites:
        def __init__(self, parent_unit):
            self.parent_unit = parent_unit
            self.prerequisites: list[dict[str]] = [] # [{'NumReq':int, units:list[str]}, ...]
            self.permission_required: bool = False
            self.prohibitions: list[str] = [] # [MTH1020, PHS1030...]
            self.corequisites: list[str] = [] # Same as above

        def set_prerequisites(self, prereqs : list[dict[str]]):
            self.prerequisites = prereqs

        def set_permission_required(self, permission_required : bool):
            self.permission_required = permission_required

        def set_prohibitions(self, prohibitions : list[str]):
            self.prohibitions = prohibitions

        def set_corequisites(self, coreqs : list[str]):
            self.corequisites = coreqs

        def get_prerequisites(self) -> list[dict[str]]:
            return self.prerequisites
        
        def get_permission_required(self) -> bool:
            return self.permission_required
        
        def get_prohibitions(self) -> list[str]:
            return self.prohibitions

        def get_corequisites(self) -> list[str]:
            return self.corequisites

        def remove_prerequisites(self):
            self.prerequisites = []
        
        def remove_prohibitions(self):
            self.prohibitions = []

        def remove_corequisites(self):
            self.corequisites = []

        def print_prerequisites(self):
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
            print(f'{(f"{self.parent_unit.unit_code} requires further permission to enrol.") if self.permission_required else f"No permissions required for {self.parent_unit.unit_code}."}')

        def print_corequisites(self):
            if len(self.corequisites) == 0:
                print(f'{self.parent_unit.unit_code} has no corequisites.')
            else:
                print(f'{self.parent_unit.unit_code} has {len(self.corequisites)} corequisites: {", ".join(self.corequisites)}.')

        def print_prohibitions(self):
            if len(self.prohibitions) == 0:
                print(f'{self.parent_unit.unit_code} has no prohibitions.')
            else:
                print(f'{self.parent_unit.unit_code} has {len(self.prohibitions)} prohibitions: {", ".join(self.prohibitions)}.')

        # Alias for usability
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