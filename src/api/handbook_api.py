import json
from requests import post

"""

This class is synchronous and only naively retrieves all implementation years for a unit. As a result, this should 
only be used to get an idea for what the response looks like.

"""


class UnitAPI:

    BASE_URL = "https://handbook.monash.edu/api/es/search"

    def __init__(self) -> None:
        pass

    def _post(self, json_content: dict) -> dict:

        request = post(self.BASE_URL, json=json_content)

        if request.status_code != 200:
            raise ValueError(f'Error code: {request.status_code}')

        return request.json()

    def _build_pagination_query(self, start: int = 0, size: int = 50, year: int = 2022):
        """

        TODO: Test the limit for retrieving units in one go

        """

        return {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"live": True}},
                        [
                            {
                                "bool": {
                                    "minimum_should_match": "100%",
                                    "should": [
                                        {
                                            "query_string": {
                                                "fields": [
                                                    "monash2_psubject.implementationYear"
                                                ],
                                                "query": f"*{year}*",
                                            }
                                        }
                                    ],
                                }
                            }
                        ],
                    ],
                    "filter": [{"terms": {"contenttype": ["monash2_psubject"]}}],
                }
            },
            "sort": [{"monash2_psubject.code_dotraw": {"order": "asc"}}],
            "from": start,
            "size": size,
            "track_scores": True,
            "_source": {
                "includes": [
                    "*.code",
                    "*.name",
                    "*.award_titles",
                    "*.keywords",
                    "urlmap",
                    "contenttype",
                ],
                "excludes": ["", None],
            },
        }

    def retrieve_search(self, start: int = 0, size: int = 50, year: int = 2022):

        search_results = self._post(self._build_pagination_query(start, size, year))

        return [self._summarise_unit_info(json.loads(result['data']))
                for result in search_results['contentlets']]
        

    def _build_unit_query(self, content: str = 'MTH3170', options: dict = None) -> dict:
        """

        Builds the query.

        """
        return {
            "query": {
                "bool": {
                    "must": [
                        {"query_string": {"query": f"monash2_psubject.code: {content}"}},
                        {"term": {"live": True}},
                    ]
                }
            },
            "aggs": {
                "implementationYear": {
                    "terms": {
                        "field": "monash2_psubject.implementationYear_dotraw",
                        "size": 100
                    }
                },
                "availableInYears": {
                    "terms": {"field": "monash2_psubject.availableInYears_dotraw", "size": 100}
                },
            },
            "size": 100,
            "_source": {
                "includes": ["versionNumber", "availableInYears", "implementationYear"]
            },
        }

    def get_unit(self, unit: str) -> dict:
        """

        Retrieves all implementation years for a unit.

        """
        search_results = self._post(self._build_unit_query(unit))

        return [self._summarise_unit_info(json.loads(result['data']))
                for result in search_results['contentlets']]

    def _summarise_unit_info(self, unit_json: dict) -> dict:
        """

        Returns a filtered down version of unit information.

        """

        return {

            'unit_name': unit_json['title'],
            'unit_code': unit_json['unit_code'],
            'credit_points': unit_json['credit_points'],
            'school': unit_json['school']['value'],
            'workload': unit_json['workload_requirements'],
            'synopsis': unit_json['handbook_synopsis'],
            'learning_outcomes': sorted([(int(item['number']), item['description'])
                                         for item in unit_json["unit_learning_outcomes"]], key=lambda x: x[0]),
            'requisites': unit_json['requisites'],
            'enrolment_rules_group': unit_json['enrolment_rules_group'],
            'location': [location['location']['value'] for location in unit_json['unit_offering']],
            'teaching_periods': [teach['teaching_period']["value"] for teach in unit_json['unit_offering']],
            # add learning_activities_grouped
            # Add teaching_approaches
            'academic_contact_roles': [{
                'role': role['role'],
                'contacts': [
                    {'contact_name': contact['contact_name'],
                     'contact_role':contact['contact_role']['label'],
                     'display_details': contact['display_name']
                     } for contact in role['contacts']
                ]}
                for role in unit_json['academic_contact_roles']
            ]

        }
