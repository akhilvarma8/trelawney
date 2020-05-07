from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from Divination import parameters
import json
import os.path
from datetime import datetime

from Divination.DataOperations.helper_functions import add_non_working_day_nav


class GetFundDataAsync:

    def __init__(self):
        parameters.update_latest_data_folder(str(datetime.today().strftime('%Y-%m-%d')) + '/')
        self.schemes_file_path = parameters.ABSOLUTE_PATH + parameters.LATEST_DATA_FOLDER
        if not os.path.exists(parameters.RAW_DATA_PATH):
            os.makedirs(parameters.RAW_DATA_PATH)
        self.schemes = []

    def response_handler(self, request_response):
        data = request_response.json()
        if request_response.status_code == 200 and len(data["data"]) != 0:
            meta = data["meta"]
            self.schemes.append(meta)
            data = add_non_working_day_nav(data)
            with open(os.path.join(parameters.RAW_DATA_PATH, str(meta["scheme_code"]) + ".json"), 'w') as fund_data:
                json.dump(data, fund_data)
            fund_data.close()

    def get_fund_data(self):
        with FuturesSession(max_workers=10) as session:
            scheme = 100000
            futures = []
            while scheme <= 150000:
                futures.append(session.get(parameters.API_URL + str(scheme)))
                scheme += 1

            for future in as_completed(futures):
                response = future.result()
                self.response_handler(response)

        print("Total Schemes", len(self.schemes))
        with open(os.path.join(self.schemes_file_path, "schemes.json"), 'w') as json_file:
            json.dump(self.schemes, json_file)
        json_file.close()


if __name__ == '__main__':
    fetch_data = GetFundDataAsync()
    fetch_data.get_fund_data()
