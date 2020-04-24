import json
import os

from AnalyseData.cagr_calculator import cagr

analysis_path = "/Users/akhilvarma/Documents/Development/Mutual Funds/Fund Data/2020-04-23/Analysis/"
data_path = "/Users/akhilvarma/Documents/Development/Mutual Funds/Fund Data/2020-04-23/"
file_name = "elssSchemesDirectGrowth.json"

cagr_for_schemes = {}

with open(os.path.join(analysis_path, file_name)) as elss_schemes_file:
    elss_schemes_data = json.load(elss_schemes_file)
    for scheme in elss_schemes_data:
        with open(os.path.join(data_path, str(scheme['scheme_code']) + ".json")) as scheme_file:
            scheme_data = json.load(scheme_file)
            start = scheme_data['data'][500]
            end = scheme_data['data'][0]
            elss_cagr = cagr(start, end)

            cagr_for_schemes[scheme['scheme_name']] = elss_cagr

sorted_cagr = sorted(cagr_for_schemes.items(), key=lambda x: x[1], reverse=True)
for gr in sorted_cagr:
    print(gr)
