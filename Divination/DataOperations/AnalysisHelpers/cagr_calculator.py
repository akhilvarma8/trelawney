import datetime
import json
import os

from Divination import parameters
from Divination.DataOperations.helper_functions import convert_to_datetime_format


def cagr_for_mutual_fund(start: dict, end: dict) -> float:
    """
    This function calculates and returns the CAGR (compound annual growth rate) for the time period.

    :param start: The {'date': 'dd-mm-YYYY', 'nav': `23.1312`} of the start of time period.
    :param end: The {'date': 'dd-mm-YYYY', 'nav': `23.1312`} of the end of time period.
    :return: The CAGR (compound annual growth rate) for the time period.
    """
    if float(start['nav']) == 0.0:
        return 0

    start_date = convert_to_datetime_format(start["date"])
    start_value = float(start["nav"])

    end_date = convert_to_datetime_format(end["date"])
    end_value = float(end["nav"])

    years = float((end_date - start_date).days) / 365
    growth_rate: float = (((end_value / start_value) ** (1 / years)) - 1) * 100

    return round(growth_rate, 2)


def cagr_for_days(start_amount: float, end_amount: float, days: int):
    years = float(days) / 365
    growth_rate: float = (((end_amount / start_amount) ** (1 / years)) - 1) * 100

    return round(growth_rate, 2)


def cagrs_for_schemes(start_index: int, end_index: int, schemes: list) -> dict:
    """
    Calculates the CAGR (compound annual growth rate) for all the schemes provided from start_index to end_index in
    scheme data.

    :param start_index: The starting index in scheme data, This data is a list of NAVs in format {'date':
    'dd-mm-YYYY', 'nav': `23.1312`}.
    :param end_index: The ending index in scheme data, This data is a list of NAVs
    in format {'date': 'dd-mm-YYYY', 'nav': `23.1312`}.
    :param schemes: The list of schemes for which the CAGRs have
    to calculated, The list contains dictionaries for metadata of each scheme.
    :return: A dictionary with a CAGR in float for each scheme_code.
    """
    cagrs = {}
    for scheme in schemes:
        with open(os.path.join(parameters.RAW_DATA_PATH, str(scheme['scheme_code']) + ".json")) as raw_data_file:
            scheme_data = json.load(raw_data_file)
            start = scheme_data['data'][start_index]
            end = scheme_data['data'][end_index]
            cagrs[str(scheme['scheme_code'])] = cagr_for_mutual_fund(start, end)
        raw_data_file.close()

    return cagrs
