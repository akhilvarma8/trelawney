import datetime
import json
import os

from Divination import parameters


def convert_to_datetime_format(date: str) -> datetime.date:
    split_values = date.split("-")
    return datetime.date(int(split_values[2]), int(split_values[1]), int(split_values[0]))


def cagr(start: dict, end: dict) -> float:
    if float(start['nav']) == 0.0:
        return 0

    start_date = convert_to_datetime_format(start["date"])
    start_value = float(start["nav"])

    end_date = convert_to_datetime_format(end["date"])
    end_value = float(end["nav"])

    years = float((end_date - start_date).days) / 365
    growth_rate: float = (((end_value / start_value) ** (1 / years)) - 1) * 100

    return round(growth_rate, 2)


def cagrs_for_schemes(start_index: int, end_index: int, schemes: dict) -> dict:
    cagrs = {}
    for scheme in schemes:
        with open(os.path.join(parameters.RAW_DATA_PATH, str(scheme['scheme_code']) + ".json")) as raw_data_file:
            scheme_data = json.load(raw_data_file)
            start = scheme_data['data'][start_index]
            end = scheme_data['data'][end_index]
            cagrs[str(scheme['scheme_code'])] = cagr(start, end)
        raw_data_file.close()

    return cagrs
