from re import findall
from json import JSONEncoder

enrolment_rule = dict[str, str]
enrolment_rules = list[enrolment_rule]

unit_pattern = r'[A-Z]{3}[0-9]{4}'
num_pattern = r'[0-9]{1,3}'


def get_number_from_msg(msg: str) -> int:
    """ Retrieves a 1-3 digit number in a message."""
    return int(findall(num_pattern, msg)[0])


def get_named_units(msg: str) -> list[str]:
    """ Returns a list of units meeting the requirement above. """
    return findall(
        unit_pattern, msg)

class SetEncoder(JSONEncoder):
    def default(self, obj):
       if isinstance(obj, set):
          return list(obj)
       return JSONEncoder.default(self, obj)