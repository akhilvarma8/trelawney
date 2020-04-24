from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import json
import os.path
from datetime import datetime

print(datetime.now())
defaultURL = 'https://api.mfapi.in/mf/'
path = "/Users/akhilvarma/Documents/Development/Mutual Funds/Fund Data/" + str(datetime.today().strftime('%Y-%m-%d'))
if not os.path.exists(path):
    os.makedirs(path)
schemes = []


def response_handler(request_response):
    data = request_response.json()
    if request_response.status_code == 200 and len(data["data"]) != 0:
        meta = data["meta"]
        schemes.append(meta)
        with open(os.path.join(path, str(meta["scheme_code"]) + ".json"), 'w') as fund_data:
            json.dump(data, fund_data)
        fund_data.close()
        if len(schemes) % 1000 == 0:
            print("scheme", data["meta"]["scheme_code"], "Total Schemes", len(schemes))


with FuturesSession(max_workers=10) as session:
    scheme = 100000
    futures = []
    while scheme <= 150000:
        futures.append(session.get(defaultURL + str(scheme)))
        scheme += 1

    for future in as_completed(futures):
        response = future.result()
        response_handler(response)

print("Total Schemes", len(schemes))
with open(os.path.join(path, "schemes.json"), 'w') as json_file:
    json.dump(schemes, json_file)
json_file.close()
print(datetime.now())
