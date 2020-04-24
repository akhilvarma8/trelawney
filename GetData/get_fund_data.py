import requests
import json
import os.path
from datetime import datetime

defaultURL = 'https://api.mfapi.in/mf/'
path = "/Users/akhilvarma/Documents/Development/Mutual Funds/Fund Data/" + str(datetime.today().strftime('%Y-%m-%d'))
if not os.path.exists(path):
    os.makedirs(path)
schemes = []

scheme = 100000
while scheme <= 200000:
    nameOfFile = str(scheme)
    url = defaultURL+nameOfFile

    response = requests.get(url=url)
    data = response.json()
    if response.status_code == 200 and len(data["data"]) != 0:
        schemes.append({scheme: data["meta"]})
        with open(os.path.join(path, nameOfFile + ".json"), 'w') as fund_data:
            json.dump(data, fund_data)
        fund_data.close()

    scheme += 1

print(len(schemes))
with open(os.path.join(path, "schemes.json"), 'w') as json_file:
    json.dump(schemes, json_file)
json_file.close()






