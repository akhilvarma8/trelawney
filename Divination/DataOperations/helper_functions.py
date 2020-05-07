import json
import os

from Divination import parameters
from datetime import timedelta, date


def date_range(start_date: date, end_date: date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def convert_to_datetime_format(date_from_nav: str) -> date:
    split_values = date_from_nav.split("-")
    return date(int(split_values[2]), int(split_values[1]), int(split_values[0]))


def fund_type_to_key_words(fund_type: str) -> dict:
    fund_type_lower = fund_type.lower()
    if fund_type_lower == 'equity':
        return parameters.EQUITY_KEY_WORDS
    elif fund_type_lower == 'elss':
        return parameters.ELSS_KEY_WORDS
    elif fund_type_lower == 'debt':
        return parameters.DEBT_KEY_WORDS
    elif fund_type_lower == 'hybrid':
        return parameters.HYBRID_KEY_WORDS
    else:
        print("Choose a valid fund type")


def redeemed_amount_for(investment_amount: float, start: dict, end: dict) -> float:
    if float(start['nav']) == 0.0:
        return 0

    units_purchased = investment_amount / float(start['nav'])
    redeemed_amount = units_purchased * float(end['nav'])
    return redeemed_amount


def add_non_working_day_nav(data: dict) -> dict:
    nav_data = data['data']
    updated_nav_data = []

    for index in range(len(nav_data) - 1):
        updated_nav_data.append(nav_data[index])
        start_date = convert_to_datetime_format(nav_data[index + 1]['date'])
        end_date = convert_to_datetime_format(nav_data[index]['date'])
        if (end_date - start_date).days > 1:
            non_working_day_navs = []
            for single_date in date_range(start_date + timedelta(1), end_date):
                nav = {'date': single_date.strftime("%d-%m-%Y"), 'nav': nav_data[index + 1]['nav']}
                non_working_day_navs.append(nav)
            non_working_day_navs.reverse()
            updated_nav_data += non_working_day_navs

    updated_nav_data.append(nav_data[-1])
    data['data'] = updated_nav_data
    return data
