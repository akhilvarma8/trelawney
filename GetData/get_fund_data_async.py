from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import parameters
import json
import os.path
from datetime import datetime

parameters.update_latest_data_folder(str(datetime.today().strftime('%Y-%m-%d')) + '/')
schemes_file_path = parameters.ABSOLUTE_PATH + parameters.LATEST_DATA_FOLDER
if not os.path.exists(parameters.SCHEME_DATA_PATH):
    os.makedirs(parameters.SCHEME_DATA_PATH)
schemes = []


def response_handler(request_response):
    data = request_response.json()
    if request_response.status_code == 200 and len(data["data"]) != 0:
        meta = data["meta"]
        schemes.append(meta)
        with open(os.path.join(parameters.SCHEME_DATA_PATH, str(meta["scheme_code"]) + ".json"), 'w') as fund_data:
            json.dump(data, fund_data)
        fund_data.close()


def get_fund_data():
    with FuturesSession(max_workers=10) as session:
        scheme = 100000
        futures = []
        while scheme <= 150000:
            futures.append(session.get(parameters.API_URL + str(scheme)))
            scheme += 1

        for future in as_completed(futures):
            response = future.result()
            response_handler(response)

    print("Total Schemes", len(schemes))
    with open(os.path.join(schemes_file_path, "schemes.json"), 'w') as json_file:
        json.dump(schemes, json_file)
    json_file.close()
