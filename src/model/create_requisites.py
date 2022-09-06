from re import findall

enrolment_rule = dict[str, str]
enrolment_rules = list[enrolment_rule]


def create_requisites(requsite_results: dict[str, enrolment_rules]) -> dict[str]:
    """
    Determines requisite rules given a set of requisites in english.

    @param requisite_results: A scrape from the MonPlan API, contains list of requisites for a unit.
    """

    parsed_requisites: dict[str] = {unit: {"permission": False, "prohibitions": [], "corequisites": [], "prerequisites": [], "cp_required": 0}
                                    for unit in requsite_results}

    for unit, unit_rules in requsite_results.items():

        for unit_rule in unit_rules:  # Go over each rule
            match unit_rule['title']:
                case "Prohibited unit":
                    pass
                case "Have not enrolled in a unit":
                    pass
                case "Have not completed enough units":
                    pass
                case "Have not passed enough units":  # only implement this for now
                    _, units = unit_rule['description'].split(":")
                    parsed_requisites[unit].extend(
                        units.strip().replace(" or", ",").split(", "))
                case "Not enough passed credit points":
                    pass
                case "Not enough enrolled credit points":
                    pass
                case "Missing corequisites":
                    parsed_requisites["corequisites"] = findall(
                        r'[A-Z]{3}[0-9]{4}', unit_rule["description"])
                case "Permission is required for this unit":
                    parsed_requisites[unit] = True

    return parsed_requisites
