import json
import os
from Divination import parameters
from Divination.DataOperations.helper_functions import fund_type_to_key_words


class FilterSchemes:

    def __init__(self):
        self.data_path = parameters.RAW_DATA_PATH
        self.schemes_file_path = parameters.ABSOLUTE_PATH + parameters.LATEST_DATA_FOLDER
        self.filtered_schemes = []

    def filter_schemes_for_keywords(self, fund_type_key_words: dict, analysis_date: str, minimum_historical_days: int):
        with open(os.path.join(self.schemes_file_path, "schemes.json")) as schemes_file:
            schemes_data = json.load(schemes_file)
            for scheme in schemes_data:
                if self.filter_for_direct_growth(scheme):
                    if self.filter_for_fund_type(scheme, fund_type_key_words):
                        with open(os.path.join(self.data_path, str(scheme['scheme_code']) + '.json')) as scheme_file:
                            scheme_data = json.load(scheme_file)
                            active = False
                            number_of_days_to_analysis_date = 0
                            for daily_nav in scheme_data['data']:
                                if daily_nav['date'] == analysis_date:
                                    active = True
                                    break
                                number_of_days_to_analysis_date += 1

                            if active:
                                if len(scheme_data['data']) > minimum_historical_days + number_of_days_to_analysis_date:
                                    scheme['endIndex'] = number_of_days_to_analysis_date
                                    scheme['startIndex'] = number_of_days_to_analysis_date + minimum_historical_days
                                    self.filtered_schemes.append(scheme)

                        scheme_file.close()
        schemes_file.close()

        return self.filtered_schemes

    @staticmethod
    def filter_for_direct_growth(scheme: dict) -> bool:
        """
        This method filters the scheme for Direct & Growth variants.

        :param scheme: The dictionary representing the meta data of a scheme.
        :return: A boolean, True if both Direct and Growth are present in the scheme_name.
        """
        return "Direct" in scheme["scheme_name"] and "Growth" in scheme["scheme_name"]

    @staticmethod
    def filter_for_fund_type(scheme: dict, fund_type_key_words: dict) -> bool:
        """
        This method filters the scheme based on keywords.

        :param scheme: The dictionary representing the meta data of a scheme.
        :param fund_type_key_words: Keywords dictionary with in and out lists.
        :return: A boolean, True if any of the in keywords are present and none of out keywords are
        present in scheme_category.
        """
        for out_key_word in fund_type_key_words['out']:
            if out_key_word in scheme['scheme_category']:
                return False

        for in_key_word in fund_type_key_words['in']:
            if in_key_word in scheme['scheme_category']:
                return True

        return False


def main():
    filtered = FilterSchemes()
    filtered_schemes = filtered.filter_schemes_for_keywords(fund_type_to_key_words("equity"), '31-12-2019', 2000)
    scheme_categories = []
    for scheme in filtered_schemes:
        scheme_categories.append(scheme['scheme_category'])

    print(set(scheme_categories))


if __name__ == '__main__':
    main()
