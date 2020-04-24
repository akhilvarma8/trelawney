import json
import os

TEST_DATES = ["21-04-2020", "22-04-2020", "20-04-2020"]
LONG_HISTORY_DAYS = 500

path = "/Users/akhilvarma/Documents/Development/Mutual Funds/Fund Data/2020-04-23/"
analysis_path = os.path.join(path, "Analysis")
if not os.path.exists(analysis_path):
    os.makedirs(analysis_path)
active_schemes = []
long_history_schemes = []

with open(os.path.join(path, "schemes.json")) as schemes_file:
    schemes_data = json.load(schemes_file)
    for scheme in schemes_data:
        with open(os.path.join(path, str(scheme['scheme_code'])+'.json')) as scheme_file:
            scheme_data = json.load(scheme_file)
            active = False
            for daily_nav in scheme_data['data']:
                if daily_nav['date'] in TEST_DATES:
                    active = True
                    break

            if active:
                active_schemes.append(scheme)
                if len(scheme_data['data']) > LONG_HISTORY_DAYS:
                    long_history_schemes.append(scheme)

        scheme_file.close()
schemes_file.close()

with open(os.path.join(analysis_path, "activeSchemes.json"), 'w') as json_file:
    json.dump(active_schemes, json_file)
json_file.close()

with open(os.path.join(analysis_path, "longHistorySchemes.json"), 'w') as json_file:
    json.dump(long_history_schemes, json_file)
json_file.close()

print("Total Long History Schemes", len(long_history_schemes))
print("Total Active Schemes", len(active_schemes))





