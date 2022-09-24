from re import findall, IGNORECASE, search
from src.data_processing.utils import unit_pattern



def pull_handbook_requisites(handbook_dict: dict[str]) -> set:
    """
    Attempts to retrieve listed prohibitions in the Monash handbook.
    :param handbook_dict: Handbook information for a unit in dictionary form.
    """
    prohibitions = set()

    # BREAKS FOR MTE3201, need to split manually
    if (_manual_rules := handbook_dict["enrolment_rules_group"]):
        manual_rules: list[dict] = _manual_rules[0]['rules']
        for rule_dict in manual_rules:
            description = rule_dict["description"]
            if search("PROHIBITION", description, IGNORECASE):
                prohibitions |= set(findall(unit_pattern, description))


    if (boxed_rules := handbook_dict["requisites"]):
        for rule_box in boxed_rules:
            match rule_box['requisite_type']['value']:
                case 'prohibitions':
                    for unit_spec in rule_box['container'][0]['relationships']:
                        prohibitions.add(
                            unit_spec['academic_item']['value'].split(" ")[1])

    return prohibitions


