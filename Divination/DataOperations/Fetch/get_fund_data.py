import requests
from Divination import parameters
import json
import os.path
from datetime import datetime

from Divination.DataOperations.helper_functions import add_non_working_day_nav


class GetFundData:

    def __init__(self):
        parameters.update_latest_data_folder(str(datetime.today().strftime('%Y-%m-%d')) + '/')
        self.schemes_file_path = parameters.ABSOLUTE_PATH + parameters.LATEST_DATA_FOLDER
        if not os.path.exists(parameters.RAW_DATA_PATH):
            os.makedirs(parameters.RAW_DATA_PATH)
        self.schemes = []

    def get_fund_data(self):
        scheme = 100000
        while scheme <= 200000:
            name_of_file = str(scheme)
            url = parameters.API_URL + name_of_file

            response = requests.get(url=url)
            data = response.json()
            if response.status_code == 200 and len(data["data"]) != 0:
                data = add_non_working_day_nav(data)
                schemes.append({scheme: data["meta"]})
                with open(os.path.join(parameters.RAW_DATA_PATH, name_of_file + ".json"), 'w') as fund_data:
                    json.dump(data, fund_data)
                fund_data.close()

            scheme += 1

        print("Total Schemes", len(self.schemes))
        with open(os.path.join(self.schemes_file_path, "schemes.json"), 'w') as json_file:
            json.dump(self.schemes, json_file)
        json_file.close()


if __name__ == '__main__':
    fetch_data = GetFundData()
    fetch_data.get_fund_data()
