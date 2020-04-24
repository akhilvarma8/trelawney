import json
import os

EQUITY_KEY_WORDS = ["Equity", "Index"]
DEBT_KEY_WORDS = ["Debt"]
ELSS_KEY_WORDS = ["ELSS"]
HYBRID_KEY_WORDS = ["Hybrid"]

path = "/Users/akhilvarma/Documents/Development/Mutual Funds/Fund Data/2020-04-23/Analysis/"

equity_schemes = []
debt_schemes = []
elss_schemes = []
hybrid_schemes = []
equity_schemes_direct_growth = []
debt_schemes_direct_growth = []
elss_schemes_direct_growth = []
hybrid_schemes_direct_growth = []

scheme_categories = []

with open(os.path.join(path, "longHistorySchemes.json")) as schemes_file:
    schemes_data = json.load(schemes_file)
    for scheme in schemes_data:
        scheme_categories.append(scheme['scheme_category'])
        for key_word in EQUITY_KEY_WORDS:
            if "ELSS" in scheme["scheme_category"]:
                continue
            if key_word in scheme['scheme_category']:
                equity_schemes.append(scheme)
                if "Direct" in scheme["scheme_name"] and "Growth" in scheme["scheme_name"]:
                    equity_schemes_direct_growth.append(scheme)

        for key_word in DEBT_KEY_WORDS:
            if key_word in scheme['scheme_category']:
                debt_schemes.append(scheme)
                if "Direct" in scheme["scheme_name"] and "Growth" in scheme["scheme_name"]:
                    debt_schemes_direct_growth.append(scheme)

        for key_word in ELSS_KEY_WORDS:
            if key_word in scheme['scheme_category']:
                elss_schemes.append(scheme)
                if "Direct" in scheme["scheme_name"] and "Growth" in scheme["scheme_name"]:
                    elss_schemes_direct_growth.append(scheme)

        for key_word in HYBRID_KEY_WORDS:
            if key_word in scheme['scheme_category']:
                hybrid_schemes.append(scheme)
                if "Direct" in scheme["scheme_name"] and "Growth" in scheme["scheme_name"]:
                    hybrid_schemes_direct_growth.append(scheme)

with open(os.path.join(path, "equitySchemes.json"), 'w') as json_file:
    json.dump(equity_schemes, json_file)
json_file.close()

with open(os.path.join(path, "equitySchemesDirectGrowth.json"), 'w') as json_file:
    json.dump(equity_schemes_direct_growth, json_file)
json_file.close()

with open(os.path.join(path, "debtSchemes.json"), 'w') as json_file:
    json.dump(debt_schemes, json_file)
json_file.close()

with open(os.path.join(path, "debtSchemesDirectGrowth.json"), 'w') as json_file:
    json.dump(debt_schemes_direct_growth, json_file)
json_file.close()

with open(os.path.join(path, "elssSchemes.json"), 'w') as json_file:
    json.dump(elss_schemes, json_file)
json_file.close()

with open(os.path.join(path, "elssSchemesDirectGrowth.json"), 'w') as json_file:
    json.dump(elss_schemes_direct_growth, json_file)
json_file.close()

with open(os.path.join(path, "hybridSchemes.json"), 'w') as json_file:
    json.dump(hybrid_schemes, json_file)
json_file.close()

with open(os.path.join(path, "hybridSchemesDirectGrowth.json"), 'w') as json_file:
    json.dump(hybrid_schemes_direct_growth, json_file)
json_file.close()


print(len(equity_schemes))
print(len(equity_schemes_direct_growth))
print(len(debt_schemes))
print(len(debt_schemes_direct_growth))
print(len(elss_schemes))
print(len(elss_schemes_direct_growth))
print(len(hybrid_schemes))
print(len(hybrid_schemes_direct_growth))
print(set(scheme_categories))
