import json
import os
import numpy
from Divination import parameters
from Divination.DataOperations.Parse.filter_schemes import FilterSchemes
from Divination.DataOperations.AnalysisHelpers.helper_functions import fund_type_to_key_words
from Divination.DataOperations.AnalysisHelpers.cagr_calculator import cagr

ANALYSIS_DATE = '21-04-2020'
MINIMUM_HISTORICAL_DAYS = 600
PROJECTION_DAYS = 100


class CAGRAVCorrelation:

    def __init__(self, fund_type: str):
        self.fund_type = fund_type
        key_words = fund_type_to_key_words(self.fund_type)
        self.filtered_schemes = FilterSchemes().filter_schemes_for_keywords(key_words,
                                                                            ANALYSIS_DATE,
                                                                            MINIMUM_HISTORICAL_DAYS)
        self.multiple_time_length_cagrs = self.multiple_time_length_cagr_for_schemes()
        self.multiple_time_length_cagravs = self.convert_multiple_time_length_cagrs_to_cagravs()
        self.calculate_correlation_between_projection_and_history()

    def multiple_time_length_cagr_for_schemes(self):
        cagrs_for_all_schemes = []
        for scheme in self.filtered_schemes:
            with open(os.path.join(parameters.RAW_DATA_PATH, str(scheme['scheme_code']) + ".json")) as raw_data_file:
                scheme_data = json.load(raw_data_file)
                data = scheme_data['data']
                cagrs = [cagr(data[PROJECTION_DAYS - 1], data[0])]
                for i in range(PROJECTION_DAYS, MINIMUM_HISTORICAL_DAYS):
                    cagrs.append(cagr(data[i], data[PROJECTION_DAYS - 1]))
                cagrs_for_all_schemes.append(cagrs)
        return numpy.array(cagrs_for_all_schemes)

    def convert_multiple_time_length_cagrs_to_cagravs(self):
        mean_array = numpy.around(numpy.mean(self.multiple_time_length_cagrs, axis=0), 2)
        return self.multiple_time_length_cagrs - mean_array

    def calculate_correlation_between_projection_and_history(self):
        projection = self.multiple_time_length_cagrs[:, 0]
        correlations = {}
        for i in range(1, MINIMUM_HISTORICAL_DAYS - PROJECTION_DAYS + 1):
            correlations[str(i)] = numpy.corrcoef(projection, self.multiple_time_length_cagravs[:, i])[0, 1]

        print(sorted(correlations.items(), key=lambda x: x[1], reverse=True))


def main():
    CAGRAVCorrelation('ELSS')


if __name__ == '__main__':
    main()
