
from src.api.handbook_api import UnitAPI
from src.data_processing.retrieve_requisites import retrieve_requisites, retrieve_requisite_chunks
from src.data_processing.create_requisites import create_requisites
from src.data_processing.pull_handbook_requisites import pull_handbook_requisites
from src.data_processing.utils import get_named_units, SetEncoder

from functools import reduce
from json import dump


"""
Script to retrieve, process and collate Monash Handbook data.
"""



if __name__ == "__main__":

    handbook_api = UnitAPI()

    monash_handbook_data = handbook_api.retrieve_search(0, 6000, 2022)
    monash_handbook_dict = {item["unit_code"].strip()
        : item for item in monash_handbook_data}

    raw_requisites = retrieve_requisites(
        list(monash_handbook_dict.keys()))
    refined_requisites = create_requisites(
        raw_requisites)

    prohibition_candidates = {unit: pull_handbook_requisites(handbook)
                              for unit, handbook in monash_handbook_dict.items() if pull_handbook_requisites(handbook)}

    new_prohibitions_raw = retrieve_requisite_chunks(
        [[unit]+list(items) for unit, items in prohibition_candidates.items()])

    new_corequisites = retrieve_requisite_chunks(
        [[unit] for unit in monash_handbook_dict])

    unfiltered_corequisites = {unit:
                               [rule for rule in coreq_rules if rule['title']
                                == 'Missing corequisites']
                               for unit, coreq_rules in new_corequisites.items()}

    filtered_corequisites = {unit: rule for unit,
                             rule in unfiltered_corequisites.items() if rule}

    all_corequisites = create_requisites(filtered_corequisites)
    new_prohibitions = {
        unit: reduce(lambda x, y: x | y,
                     list(map(
                         lambda x: set(get_named_units(
                             x['description'])) if x['title'] == 'Prohibited unit' else set(),
                         prohib)))
        for unit, prohib in new_prohibitions_raw.items()
    }

    # Now, merge corequisites and prohibitions

    for unit, corequisite_rule in all_corequisites.items():
        if unit in refined_requisites:
            refined_requisites[unit]['corequisites'] = corequisite_rule['corequisites']
        else:
            refined_requisites[unit] = corequisite_rule

    for unit, prohibition_rule in new_prohibitions.items():
        if unit not in refined_requisites:
            refined_requisites[unit] = {"permission": False, "prohibitions": prohibition_rule, "corequisites": [], "prerequisites": [], "cp_required": 0}
        refined_requisites[unit]['prohibitions'] |= prohibition_rule

    # TODO: Patch data
            
    # Finally collate and slim with handbook data

    complete_handbook_data = {
        unit:{
            'unit_name': h_dict['unit_name'],
            'unit_code': h_dict['unit_code'].strip(),
            'credit_points': h_dict['credit_points'],
            'school': h_dict['school'],
            'requisites': refined_requisites[unit] if unit in refined_requisites else {"permission": False, "prohibitions": prohibition_rule, "corequisites": [], "prerequisites": [], "cp_required": 0},
            'offerings': h_dict['offerings']
        }
        for unit, h_dict in monash_handbook_dict.items()
    }

    """
    complete_handbook_data = monash_handbook_dict
    for unit in complete_handbook_data:
        complete_handbook_data[unit]['requisites'] = refined_requisites[unit]
    """


    with open("handbook_data_complete.json","w") as file:
        dump(complete_handbook_data, file,cls=SetEncoder)
