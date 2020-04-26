import json
import os
import csv
from Divination.DataOperations.AnalysisHelpers.cagr_calculator import cagr
from Divination.DataOperations.Parse.filter_schemes import FilterSchemes
from Divination import parameters


class CAGRPerformance:

    def __init__(self, fund_type: str):
        if not os.path.exists(parameters.ANALYSIS_PATH):
            os.makedirs(parameters.ANALYSIS_PATH)
        self.cagr_for_schemes = {}
        self.analysis_file_name = parameters.ANALYSIS_DATE + ":" + str(parameters.ANALYSIS_DAYS) + "Days" + ".csv"
        self.fund_type = fund_type

    def cagr_for_funds_of_type(self):
        print(self.analysis_file_name)
        fund_type_lower = self.fund_type.lower()
        if fund_type_lower == 'equity':
            fund_key_words = parameters.EQUITY_KEY_WORDS
        elif fund_type_lower == 'elss':
            fund_key_words = parameters.ELSS_KEY_WORDS
        elif fund_type_lower == 'debt':
            fund_key_words = parameters.DEBT_KEY_WORDS
        elif fund_type_lower == 'hybrid':
            fund_key_words = parameters.HYBRID_KEY_WORDS
        else:
            print("Choose a valid fund type")
            return

        self.analysis_file_name = self.fund_type + ":" + self.analysis_file_name
        filtered_schemes = FilterSchemes(fund_key_words).filter_schemes_for_keywords()
        for scheme in filtered_schemes:
            with open(os.path.join(parameters.SCHEME_DATA_PATH, str(scheme['scheme_code']) + ".json")) as scheme_file:
                scheme_data = json.load(scheme_file)
                start = scheme_data['data'][scheme['startIndex']]
                end = scheme_data['data'][scheme['endIndex']]
                growth_rate = cagr(start, end)

                self.cagr_for_schemes[scheme['scheme_name']] = growth_rate
            scheme_file.close()

        self.write_funds_performance_to_file()

    def write_funds_performance_to_file(self):
        sorted_funds = sorted(self.cagr_for_schemes.items(), key=lambda x: x[1], reverse=True)
        print(len(sorted_funds))

        with open(os.path.join(parameters.ANALYSIS_PATH, self.analysis_file_name), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Fund Name", "CAGR"])
            writer.writerows(sorted_funds)


def main():
    CAGRPerformance("Hybrid").cagr_for_funds_of_type()
    CAGRPerformance("Equity").cagr_for_funds_of_type()
    CAGRPerformance("Debt").cagr_for_funds_of_type()
    CAGRPerformance("ELSS").cagr_for_funds_of_type()


if __name__ == '__main__':
    main()
