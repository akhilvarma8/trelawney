import json
import os
import parameters

data_path = parameters.SCHEME_DATA_PATH
schemes_file_path = parameters.ABSOLUTE_PATH + parameters.LATEST_DATA_FOLDER
if not os.path.exists(parameters.ANALYSIS_PATH):
    os.makedirs(parameters.ANALYSIS_PATH)
analysis_file_name = parameters.ANALYSIS_DATE + ":" + str(parameters.ANALYSIS_DAYS) + "Days" + ".json"

filtered_schemes = []


def filter_schemes(fund_type_key_words: dict, file_prefix: str):
    global analysis_file_name
    analysis_file_name = file_prefix + ":" + analysis_file_name
    with open(os.path.join(schemes_file_path, "schemes.json")) as schemes_file:
        schemes_data = json.load(schemes_file)
        for scheme in schemes_data:
            with open(os.path.join(data_path, str(scheme['scheme_code']) + '.json')) as scheme_file:
                scheme_data = json.load(scheme_file)
                active = False
                for daily_nav in scheme_data['data']:
                    if daily_nav['date'] == parameters.ANALYSIS_DATE:
                        active = True
                        break

                if active:
                    if len(scheme_data['data']) > parameters.ANALYSIS_DAYS:
                        if filter_for_direct_growth(scheme_data['meta']):
                            if filter_for_fund_type(scheme_data['meta'], fund_type_key_words):
                                filtered_schemes.append(scheme)

            scheme_file.close()
    schemes_file.close()

    with open(os.path.join(parameters.ANALYSIS_PATH, analysis_file_name), 'w') as json_file:
        json.dump(filtered_schemes, json_file)
    json_file.close()


def filter_for_direct_growth(scheme: dict) -> bool:
    return "Direct" in scheme["scheme_name"] and "Growth" in scheme["scheme_name"]


def filter_for_fund_type(scheme: dict, fund_type_key_words: dict) -> bool:
    for out_key_word in fund_type_key_words['out']:
        if out_key_word in scheme['scheme_category']:
            return False

    for in_key_word in fund_type_key_words['in']:
        if in_key_word in scheme['scheme_category']:
            return True

    return False


def main():
    filter_schemes(parameters.ELSS_KEY_WORDS, "ELSS")


if __name__ == '__main__':
    main()
