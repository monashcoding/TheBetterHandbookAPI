import queue
import time
from requests import post
from threading import Thread
import json


def perform_web_requests(unit_chunks: list[list[str]], no_workers: int):
    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue
            self.results = []

        def run(self):
            """

            Retrieves and adds rules continuously.

            """
            while True:
                content = self.queue.get()
                if content == "":
                    break

                response = post("https://mscv.apps.monash.edu",
                                json=self._build_post_content(content))
                try:
                    response = response.json()
                except json.JSONDecodeError as e:
                    print(f'{content} failed, retrying...')
                    self.queue.put(content)
                    break
                try:
                    self.results.append(response['courseErrors'])
                except KeyError as e:
                    print(f'Failed to retrieve rules for {content}, {e}')
                self.queue.task_done()

        def _build_post_content(self, units: list[str]) -> dict:

            return {
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

    # Create queue and add addresses
    q = queue.Queue()
    for chunk in unit_chunks:
        q.put(chunk)

    # Workers keep working till they receive an empty string
    for _ in range(no_workers):
        q.put("")

    # Create workers and add to  the queue
    workers = []
    for _ in range(no_workers):
        worker = Worker(q)
        worker.start()
        workers.append(worker)

    # Join workers to wait till they finished
    for worker in workers:
        worker.join()

    # Combine results from all workers
    r = []
    for worker in workers:
        r.extend(worker.results)
    return r


def load_units_csv(file_name: str = "all_units.csv"):
    with open(file_name, 'r') as f:
        text = f.read().split("\n")
        return list(set(map(lambda x: x.split(",")[1].strip(), text)))[1:]


def process_requisites(unit_reqs) -> dict:
    """
    TODO: Completely process the requisites.

    """

    unit_req_dict = {}

    for unit_req in unit_reqs:
        if (unit_code := unit_req['references'][0]['unitCode']) not in unit_req_dict:
            unit_req_dict[unit_code] = []

        unit_req_dict[unit_code].append(
            {'title': unit_req['title'], 'description': unit_req['description']})

    return unit_req_dict


def retrieve_requisites(unit_list: list[str]) -> dict:
    """
    Pulls raw requisite data from the MonPlan verification server in chunks of 125. Works in parallel.
    :param unit_list: List of unit codes to obtain requisite rules for.
    """

    unit_chunks = [unit_list[idx:min(idx+125, len(unit_list))]
                   for idx in range(0, len(unit_list), 125)]

    return retrieve_requisite_chunks(unit_chunks)


def retrieve_requisite_chunks(unit_chunks: list[list[str]]) -> dict:
    """
    Retrieves raw requisite data in chunks.
    """
    now = time.time()
    results = perform_web_requests(unit_chunks, 22)
    time_taken = time.time() - now

    print(time_taken)
    unit_reqs = [item for sublist in results for item in sublist]

    return process_requisites(unit_reqs)


if __name__ == "__main__":
    units = load_units_csv()

    with open("unit_reqs_clean.json", "w") as f:
        json.dump(retrieve_requisites(units), f)
