import json
import os

from Divination import parameters
from Divination.DataOperations.AnalysisHelpers.cagr_calculator import cagrs_for_schemes
from Divination.DataOperations.AnalysisHelpers.helper_functions import fund_type_to_key_words, redeemed_amount_for
from Divination.DataOperations.Parse.filter_schemes import FilterSchemes


class InvestmentPerformance:
    ANALYSIS_DATE = '21-04-2020'
    ANALYSIS_DAYS = 84
    MINIMUM_HISTORICAL_DAYS = 1500
    FUNDS_DIVERSIFICATION = 3  # Top 'N' number of funds will be invested.
    INVESTMENT_AMOUNT = 100000.00

    def __init__(self, fund_type: str):
        self.fund_type = fund_type
        key_words = fund_type_to_key_words(self.fund_type)
        self.filtered_schemes = FilterSchemes().filter_schemes_for_keywords(key_words,
                                                                            self.ANALYSIS_DATE,
                                                                            self.MINIMUM_HISTORICAL_DAYS)
        print(len(self.filtered_schemes))

    def return_on_investment(self):
        start_index = self.filtered_schemes[0]['startIndex']
        end_index = self.filtered_schemes[0]['endIndex']

        print(start_index, end_index)

        index = start_index - self.ANALYSIS_DAYS
        while index - self.ANALYSIS_DAYS > end_index:
            cagrs = cagrs_for_schemes(index + self.ANALYSIS_DAYS, index, self.filtered_schemes)
            sorted_funds = sorted(cagrs.items(), key=lambda x: x[1], reverse=True)
            self.calculate_redeemed_amount(index, index - self.ANALYSIS_DAYS, sorted_funds)
            index -= self.ANALYSIS_DAYS

        cagrs = cagrs_for_schemes(index + self.ANALYSIS_DAYS, index, self.filtered_schemes)
        sorted_funds = sorted(cagrs.items(), key=lambda x: x[1], reverse=True)
        self.calculate_redeemed_amount(index, end_index, sorted_funds)
        index = end_index
        print(index, round(self.INVESTMENT_AMOUNT))

    def calculate_redeemed_amount(self, start_index: int, end_index: int, sorted_funds: []):
        redeemed_amount = 0
        for fund in sorted_funds[0: self.FUNDS_DIVERSIFICATION]:
            with open(os.path.join(parameters.RAW_DATA_PATH, fund[0] + ".json")) as raw_data_file:
                scheme_data = json.load(raw_data_file)
                data = scheme_data['data']
                redeemed_amount += redeemed_amount_for(self.INVESTMENT_AMOUNT / self.FUNDS_DIVERSIFICATION,
                                                       data[start_index], data[end_index])

        self.INVESTMENT_AMOUNT = redeemed_amount

    def average_return_on_investment(self):
        investment_amount = 100000
        redeemed_amount = 0
        for scheme in self.filtered_schemes:
            with open(os.path.join(parameters.RAW_DATA_PATH, str(scheme['scheme_code']) + ".json")) as raw_data_file:
                scheme_data = json.load(raw_data_file)
                start = scheme_data['data'][scheme['startIndex'] - self.ANALYSIS_DAYS]
                end = scheme_data['data'][scheme['endIndex']]
                redeemed_amount += redeemed_amount_for(investment_amount / len(self.filtered_schemes),
                                                       start, end)

        print('Average Performance =', redeemed_amount)


def main():
    performance = InvestmentPerformance('ELSS')
    performance.return_on_investment()
    print(performance.INVESTMENT_AMOUNT)
    performance.average_return_on_investment()


if __name__ == '__main__':
    main()
