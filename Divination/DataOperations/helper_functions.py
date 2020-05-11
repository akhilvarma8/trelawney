from datetime import timedelta, date


def date_range(start_date: date, end_date: date):
    """
    This function returns an iterable from start_date to and not including end_date.

    :param start_date: The starting date in datetime.date format.
    :param end_date: The ending date in datetime.date format.
    """
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def convert_to_datetime_format(date_from_nav: str) -> date:
    """
    This function converts the date string with format dd-mm-YYYY to datetime.date format and returns it.
    This method throws a ValueError if the values are no in range.

    :param date_from_nav: Date string in dd-mm-YYYY format.
    :return: datetime.date if year, month and day are in range.
    """
    split_values = date_from_nav.split("-")
    return date(int(split_values[2]), int(split_values[1]), int(split_values[0]))


def fund_type_to_key_words(fund_type: str) -> dict:
    """
    This function returns the keywords from parameters for a particular type of fund. The below funds are now supported
        - Equity
        - Debt
        - Hybrid
        - ELSS

    :param fund_type: The type of fund, This is case insensitive.
    :return: A dictionary containing the 'in' and 'out' lists containing the keywords,
    The filter in words in the 'in' list and filter our words in 'out' list from fund scheme name.
    """
    fund_type_lower = fund_type.lower()
    if fund_type_lower == 'equity':
        return {'in': ["Equity", "Index"], 'out': ['ELSS']}
    elif fund_type_lower == 'elss':
        return {'in': ["Debt"], 'out': []}
    elif fund_type_lower == 'debt':
        return {'in': ["ELSS"], 'out': []}
    elif fund_type_lower == 'hybrid':
        return {'in': ["Hybrid"], 'out': []}
    else:
        print("Choose a valid fund type")


def redeemed_amount_for(investment_amount: float, start: dict, end: dict) -> float:
    """
    This function calculates the redeemed amount for an investment.

    :param investment_amount: The amount invested in Rupees.
    :param start: The start dictionary. This contains the
    date and nav on that date in format {'date': 'dd-mm-YYYY', 'nav': `23.1312`}.
    :param end: The end dictionary. This contains the
    date and nav on that date in format {'date': 'dd-mm-YYYY', 'nav': `23.1312`}.
    :return: A float for the amount redeemed at end date.
    """
    if float(start['nav']) == 0.0:
        return 0

    units_purchased = investment_amount / float(start['nav'])
    redeemed_amount = units_purchased * float(end['nav'])
    return redeemed_amount


def add_non_working_day_nav(data: dict) -> dict:
    """
    This function adds the nav for any missing days between start and end. It uses the previous day's nav as reference.

    :param data: The dictionary containing the data for the scheme, The dictionary should contain a key called 'data'
    and the value of that keey has to be a list of dictionaries containing navs in the format {'date': 'dd-mm-YYYY',
    'nav': `23.1312`}.
    :return: Returns a dict in the format of argument data but with missing navs filled.
    """
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
