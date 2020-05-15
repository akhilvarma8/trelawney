import json
import os
import numpy
from datetime import datetime
from Divination import parameters
from Divination.DataOperations.Parse.filter_schemes import FilterSchemes
from Divination.DataOperations.helper_functions import fund_type_to_key_words
from Divination.DataOperations.AnalysisHelpers.cagr_calculator import cagr

ANALYSIS_DATE = '30-12-2019'
ANALYSIS_DAYS = 1000
MINIMUM_HISTORICAL_DAYS = 2000
PROJECTION_DAYS = 365


class CAGRAVCorrelation:

    def __init__(self, fund_type: str):
        self.fund_type = fund_type
        key_words = fund_type_to_key_words(self.fund_type)
        self.filtered_schemes = FilterSchemes().filter_schemes_for_keywords(key_words,
                                                                            ANALYSIS_DATE,
                                                                            MINIMUM_HISTORICAL_DAYS)
        print(len(self.filtered_schemes))

    def multiple_time_length_cagrav_for_schemes(self, projection_day: int):
        print(projection_day, datetime.now())
        cagrs_for_all_schemes = []
        for scheme in self.filtered_schemes:
            with open(os.path.join(parameters.RAW_DATA_PATH, str(scheme['scheme_code']) + ".json")) as raw_data_file:
                scheme_data = json.load(raw_data_file)
                data = scheme_data['data']
                cagrs = [cagr(data[projection_day - 1], data[projection_day - PROJECTION_DAYS])]
                for i in range(projection_day, MINIMUM_HISTORICAL_DAYS):
                    cagrs.append(cagr(data[i], data[projection_day - 1]))
                cagrs_for_all_schemes.append(cagrs)
        multiple_time_length_cagrs = numpy.array(cagrs_for_all_schemes)
        mean_array = numpy.around(numpy.mean(multiple_time_length_cagrs, axis=0), 2)
        return multiple_time_length_cagrs - mean_array

    def calculate_correlation_between_projection_and_history(self):
        correlations = {}
        for i in range(PROJECTION_DAYS, PROJECTION_DAYS + ANALYSIS_DAYS):
            multiple_time_length_cagravs = self.multiple_time_length_cagrav_for_schemes(i)
            projection = multiple_time_length_cagravs[:, 0]
            for j in range(1, MINIMUM_HISTORICAL_DAYS - (PROJECTION_DAYS + ANALYSIS_DAYS) + 1):
                if str(j) in correlations:
                    correlations[str(j)] = (correlations[str(j)] +
                                            numpy.corrcoef(projection, multiple_time_length_cagravs[:, j])[0, 1]) / 2
                else:
                    correlations[str(j)] = numpy.corrcoef(projection, multiple_time_length_cagravs[:, j])[0, 1]
        print(sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:20])


def main():
    start = datetime.now()
    print(start)
    correlation = CAGRAVCorrelation('Equity')
    correlation.calculate_correlation_between_projection_and_history()
    end = datetime.now()
    print(end)
    print(end - start)


if __name__ == '__main__':
    main()
