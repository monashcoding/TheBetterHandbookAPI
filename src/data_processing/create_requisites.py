from re import findall

enrolment_rule = dict[str, str]
enrolment_rules = list[enrolment_rule]


def create_requisites(requsite_results: dict[str, enrolment_rules]) -> dict[str]:
    """
    Determines requisite rules given a set of requisites in english.

    @param requisite_results: A scrape from the MonPlan API, contains list of requisites for a unit.
    """
    unit_pattern = r'[A-Z]{3}[0-9]{4}'
    num_pattern = r'[0-9]{1,3}'

    def get_number_from_msg(msg: str) -> int:
        """ Retrieves a 1-3 digit number in a message."""
        return int(findall(num_pattern, msg)[0])

    def get_named_units(msg: str) -> list[str]:
        """ Returns a list of units meeting the requirement above. """
        return findall(
            unit_pattern, msg)

    parsed_requisites: dict[str] = {unit: {"permission": False, "prohibitions": [], "corequisites": [], "prerequisites": [], "cp_required": 0}
                                    for unit in requsite_results}

    for unit, unit_rules in requsite_results.items():

        for unit_rule in unit_rules:  # Go over each rule
            match unit_rule['title']:
                case "Prohibited unit":
                    parsed_requisites[unit]["prohibitions"] = get_named_units(
                        unit_rule["description"])
                # There are only three units in the latter case
                case "Have not enrolled in a unit" | "Have not completed enough units":
                    parsed_requisites[unit]["prerequisites"].append(
                        {"NumReq": 1, "units": get_named_units(unit_rule["description"])})

                case "Have not passed enough units":
                    number_required_msg, units_msg = unit_rule['description'].split(
                        ":")

                    # TODO: REGEX pattern cannot pick up BMS3052 prereqs as they are BIO\u2026
                    parsed_requisites[unit]["prerequisites"].append({
                        "NumReq": get_number_from_msg(number_required_msg),
                        "units": units_msg.strip().replace(" or", ",").split(", ")
                    })

                case "Not enough passed credit points" | "Not enough enrolled credit points":
                    parsed_requisites[unit]["cp_required"] = get_number_from_msg(
                        unit_rule["description"])

                case "Missing corequisites":
                    parsed_requisites[unit]["corequisites"] = get_named_units(
                        unit_rule["description"])

                case "Permission is required for this unit":
                    parsed_requisites[unit]["permission"] = True

    return parsed_requisites


if __name__ == "__main__":
    from json import load
    with open("unit_reqs_clean.json", "r") as file:
        unit_reqs = load(file)

    create_requisites(unit_reqs)
