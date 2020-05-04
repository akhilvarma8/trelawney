import json
import os
import csv
from statistics import mean
from Divination.DataOperations.AnalysisHelpers.cagr_calculator import cagr
from Divination.DataOperations.AnalysisHelpers.helper_functions import fund_type_to_key_words
from Divination.DataOperations.Parse.filter_schemes import FilterSchemes
from Divination import parameters

ANALYSIS_DATE = '21-04-2020'
ANALYSIS_DAYS = 100


class CAGRHistory:

    def __init__(self, fund_type: str):
        if not os.path.exists(parameters.ANALYSIS_PATH):
            os.makedirs(parameters.ANALYSIS_PATH)
        self.cagr_for_schemes = {}
        self.cagrs = []
        self.analysis_file_name = ANALYSIS_DATE + ":" + str(ANALYSIS_DAYS) + "Days" + ".csv"
        self.fund_type = fund_type

    def cagr_for_funds_of_type(self):
        self.analysis_file_name = self.fund_type + ":" + self.analysis_file_name
        key_words = fund_type_to_key_words(self.fund_type)
        filtered_schemes = FilterSchemes().filter_schemes_for_keywords(key_words, ANALYSIS_DATE, ANALYSIS_DAYS)
        for scheme in filtered_schemes:
            with open(os.path.join(parameters.RAW_DATA_PATH, str(scheme['scheme_code']) + ".json")) as raw_data_file:
                scheme_data = json.load(raw_data_file)
                start = scheme_data['data'][scheme['startIndex']]
                end = scheme_data['data'][scheme['endIndex']]
                growth_rate = cagr(start, end)

                self.cagr_for_schemes[scheme['scheme_name']] = growth_rate
                self.cagrs.append(growth_rate)
            raw_data_file.close()

        self.write_funds_history_to_file()

    def write_funds_history_to_file(self):
        sorted_funds = sorted(self.cagr_for_schemes.items(), key=lambda x: x[1], reverse=True)
        print(len(sorted_funds))
        funds_mean = mean(self.cagrs)

        with open(os.path.join(parameters.ANALYSIS_PATH, self.analysis_file_name), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Fund Name", "CAGR", "Performance above Average"])
            for fund in sorted_funds:
                fund = fund + tuple([round(fund[1] - funds_mean, 2)])
                writer.writerow(fund)


def main():
    CAGRHistory("ELSS").cagr_for_funds_of_type()


if __name__ == '__main__':
    main()
