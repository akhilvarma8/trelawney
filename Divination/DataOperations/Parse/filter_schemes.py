import json
import os
from Divination import parameters


class FilterSchemes:

    def __init__(self):
        self.data_path = parameters.RAW_DATA_PATH
        self.schemes_file_path = parameters.ABSOLUTE_PATH + parameters.LATEST_DATA_FOLDER
        self.filtered_schemes = []

    def filter_schemes_for_keywords(self, fund_type_key_words: dict, analysis_date: str, analysis_days: int):
        with open(os.path.join(self.schemes_file_path, "schemes.json")) as schemes_file:
            schemes_data = json.load(schemes_file)
            for scheme in schemes_data:
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
                        if len(scheme_data['data']) > analysis_days + number_of_days_to_analysis_date:
                            scheme['endIndex'] = number_of_days_to_analysis_date
                            scheme['startIndex'] = number_of_days_to_analysis_date + analysis_days
                            if self.filter_for_direct_growth(scheme_data['meta']):
                                if self.filter_for_fund_type(scheme_data['meta'], fund_type_key_words):
                                    self.filtered_schemes.append(scheme)

                scheme_file.close()
        schemes_file.close()

        return self.filtered_schemes

    @staticmethod
    def filter_for_direct_growth(scheme: dict) -> bool:
        return "Direct" in scheme["scheme_name"] and "Growth" in scheme["scheme_name"]

    @staticmethod
    def filter_for_fund_type(scheme: dict, fund_type_key_words: dict) -> bool:
        for out_key_word in fund_type_key_words['out']:
            if out_key_word in scheme['scheme_category']:
                return False

        for in_key_word in fund_type_key_words['in']:
            if in_key_word in scheme['scheme_category']:
                return True

        return False
