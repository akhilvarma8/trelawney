import json
import math
import os
import numpy
from datetime import datetime
from Divination import parameters
from Divination.DataOperations.Parse.filter_schemes import FilterSchemes
from Divination.DataOperations.helper_functions import fund_type_to_key_words
from Divination.DataOperations.AnalysisHelpers.cagr_calculator import cagr_for_mutual_fund

ANALYSIS_DATE = '07-05-2020'
MINIMUM_HISTORICAL_DAYS = 2000
CORRELATION_ANALYSIS_DAYS = 365
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
        cagrs_for_all_schemes = []
        for scheme in self.filtered_schemes:
            with open(os.path.join(parameters.RAW_DATA_PATH, str(scheme['scheme_code']) + ".json")) as raw_data_file:
                scheme_data = json.load(raw_data_file)
                data = scheme_data['data']
                projection_index = projection_day + scheme['endIndex']
                cagrs = [cagr_for_mutual_fund(data[projection_index], data[projection_index - PROJECTION_DAYS])]
                # Optimisations as we need same length arrays for correlation average.
                for i in range(projection_index + 1,
                               projection_index + MINIMUM_HISTORICAL_DAYS -
                               (PROJECTION_DAYS + CORRELATION_ANALYSIS_DAYS) + 1):
                    cagrs.append(cagr_for_mutual_fund(data[i], data[projection_index]))
                cagrs_for_all_schemes.append(cagrs)
        multiple_time_length_cagrs = numpy.array(cagrs_for_all_schemes)
        mean_array = numpy.around(numpy.mean(multiple_time_length_cagrs, axis=0), 2)
        return multiple_time_length_cagrs - mean_array

    def calculate_correlation_between_projection_and_history(self):
        correlation_arrays = {}
        for i in range(PROJECTION_DAYS, PROJECTION_DAYS + CORRELATION_ANALYSIS_DAYS):
            multiple_time_length_cagravs = self.multiple_time_length_cagrav_for_schemes(i)
            projection = multiple_time_length_cagravs[:, 0]
            for j in range(1, MINIMUM_HISTORICAL_DAYS - (PROJECTION_DAYS + CORRELATION_ANALYSIS_DAYS) + 1):
                corrcoef = numpy.corrcoef(projection, multiple_time_length_cagravs[:, j])[0, 1]
                if math.isnan(corrcoef):
                    continue
                if str(j) in correlation_arrays:
                    correlation_arrays[str(j)].append(corrcoef)
                else:
                    correlation_arrays[str(j)] = [corrcoef]

        correlations = {}
        for key, value in correlation_arrays.items():
            numpy_array = numpy.array(value)
            mean = numpy.mean(numpy_array)
            correlations[key] = mean
        print(sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:20])


def main():
    start = datetime.now()
    print(start)
    correlation = CAGRAVCorrelation('ELSS')
    correlation.calculate_correlation_between_projection_and_history()
    end = datetime.now()
    print(end)
    print(end - start)


if __name__ == '__main__':
    main()
