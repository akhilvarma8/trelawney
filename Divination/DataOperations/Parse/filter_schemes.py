import json
import os
from Divination import parameters
from Divination.DataOperations.helper_functions import fund_type_to_key_words


class FilterSchemes:

    def __init__(self):
        self.data_path = parameters.RAW_DATA_PATH
        self.schemes_file_path = parameters.ABSOLUTE_PATH + parameters.LATEST_DATA_FOLDER

    def filter_schemes_for_keywords(self, fund_type_key_words: dict, analysis_date: str, minimum_historical_days: int):
        """
        This method filters the funds for the following
            - Key words in the scheme_category
            - Only Direct and Growth Schemes
            - Is active on analysis_date
            - Contains at least minimum_historical_days history to and including the analysis_date.
        :param fund_type_key_words: A dictionary for in and out type keywords.
        :param analysis_date: The date for which the filter is anchored to.
        :param minimum_historical_days: The number of days in the past including the analysis_date for which the fund
        has to be active to be filtered.
        :return: Returns a list of schemes that pass the filter parameters.
        """
        filtered_schemes = []
        with open(os.path.join(self.schemes_file_path, "schemes.json")) as schemes_file:
            schemes_data = json.load(schemes_file)
            for scheme in schemes_data:
                if self.filter_for_direct_growth(scheme):
                    if self.filter_for_fund_type(scheme, fund_type_key_words):
                        with open(os.path.join(self.data_path, str(scheme['scheme_code']) + '.json')) as scheme_file:
                            scheme_data = json.load(scheme_file)
                            active = False
                            index_of_analysis_date = 0
                            # Replace this with BST.
                            for daily_nav in scheme_data['data']:
                                if daily_nav['date'] == analysis_date:
                                    active = True
                                    break
                                index_of_analysis_date += 1

                            if active:
                                if len(scheme_data['data']) >= minimum_historical_days + index_of_analysis_date:
                                    scheme['endIndex'] = index_of_analysis_date
                                    scheme['startIndex'] = index_of_analysis_date + minimum_historical_days - 1
                                    filtered_schemes.append(scheme)

                        scheme_file.close()
        schemes_file.close()

        return filtered_schemes

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
    filtered_schemes = filtered.filter_schemes_for_keywords(fund_type_to_key_words("ELSS"), '07-05-2020', 2000)
    scheme_categories = []
    for scheme in filtered_schemes:
        print(scheme['scheme_name'], scheme['scheme_category'])


if __name__ == '__main__':
    main()
