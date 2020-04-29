from Divination import parameters


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
