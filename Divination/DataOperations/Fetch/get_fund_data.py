import requests
from Divination import parameters
import json
import os.path
from datetime import datetime

parameters.update_latest_data_folder(str(datetime.today().strftime('%Y-%m-%d')) + '/')
schemes_file_path = parameters.ABSOLUTE_PATH + parameters.LATEST_DATA_FOLDER
if not os.path.exists(parameters.RAW_DATA_PATH):
    os.makedirs(parameters.RAW_DATA_PATH)
schemes = []


def get_fund_data():
    scheme = 100000
    while scheme <= 200000:
        name_of_file = str(scheme)
        url = parameters.API_URL + name_of_file

        response = requests.get(url=url)
        data = response.json()
        if response.status_code == 200 and len(data["data"]) != 0:
            schemes.append({scheme: data["meta"]})
            with open(os.path.join(parameters.RAW_DATA_PATH, name_of_file + ".json"), 'w') as fund_data:
                json.dump(data, fund_data)
            fund_data.close()

        scheme += 1

    print("Total Schemes", len(schemes))
    with open(os.path.join(schemes_file_path, "schemes.json"), 'w') as json_file:
        json.dump(schemes, json_file)
    json_file.close()
