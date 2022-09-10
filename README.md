# TheBetterHandbookAPI

The definitive Monash handbook API.

## Using the handbook API

To request the Monash handbook from the URL `https://handbook.monash.edu/api/es/search` (POST) send the following JSON:

```py
{
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
```

Note that replacing `monash2` with `unsw` will let you request UNSW units. Additionally, content should be a unit code. This API for querying hasn't been documented properly, and there are likely many filters etc. There is also a request that can return all 5282 or so Monash units below:

```python
{
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
```

## Using the MonPlan API

MonPlan POSTs a request to `https://mscv.apps.monash.edu` with a course plan in JSON format. You can send up to 125 units in one request before it will fail:

```py
{
"startYear": 2022,
"advancedStanding": [

],
"internationalStudent": False,
"courseInfo": {

},
"teachingPeriods": [
    {
        "year": 2022,
        "code": "S1-01",
        "units": [
                {
                    "unitCode": unit_code,
                    "placeholder": False
                } for unit_code in units
        ],
        "intermission": False,
        "studyAbroad": False
    }
]
}
```

Here `units` is a list of unit codes.

## TODO

- Look at Handbook returns for prohibitions and corequisites, use Regex on both enrolment rules group and requisites.
- Do a secondary scrape of the MonPlan with prohibitions by putting them all together. There are likely no more than 100 prohibitions. (Is this required?)
- Collate data, in case of prohibitions, add them straight to the dataset
- For corequisites, add as well
- Remove units that are no longer offered
- Incorporate data patcher after collating (ADD,SET) operation, set for cp, add for rule that doesn't get added
- Implement serialisation class
- https://ipython-books.github.io/64-visualizing-a-networkx-graph-in-the-notebook-with-d3js/ 
- https://realpython.com/python-multiple-constructors/