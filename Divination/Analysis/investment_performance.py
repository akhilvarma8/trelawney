import json
import os

from Divination import parameters
from Divination.DataOperations.AnalysisHelpers.helper_functions import fund_type_to_key_words
from Divination.DataOperations.Parse.filter_schemes import FilterSchemes

ANALYSIS_DATE = '21-04-2020'
ANALYSIS_DAYS = 200
MINIMUM_HISTORICAL_DAYS = 1500


class InvestmentPerformance:
    def __init__(self, fund_type: str):
        self.fund_type = fund_type
        key_words = fund_type_to_key_words(self.fund_type)
        self.filtered_schemes = FilterSchemes().filter_schemes_for_keywords(key_words,
                                                                            ANALYSIS_DATE,
                                                                            MINIMUM_HISTORICAL_DAYS)
        print(len(self.filtered_schemes))

    def return_on_investment(self, investment_amount: int):
        for scheme in self.filtered_schemes:
            with open(os.path.join(parameters.RAW_DATA_PATH, str(scheme['scheme_code']) + ".json")) as raw_data_file:
                scheme_data = json.load(raw_data_file)
