# Parameters for fetching data
API_URL = 'https://api.mfapi.in/mf/'

# Parameters for storing and accessing fetched data
ABSOLUTE_PATH = '/Users/akhilvarma/Documents/Development/Mutual Fund Data/'
LATEST_DATA_FOLDER = '2020-04-23/'
SCHEME_DATA_PATH = ABSOLUTE_PATH + LATEST_DATA_FOLDER + "Data"

# Parameters for organising data
EQUITY_KEY_WORDS = {'in': ["Equity", "Index"], 'out': ['ELSS']}
DEBT_KEY_WORDS = {'in': ["Debt"], 'out': []}
ELSS_KEY_WORDS = {'in': ["ELSS"], 'out': []}
HYBRID_KEY_WORDS = {'in': ["Hybrid"], 'out': []}


# Parameters for analysing data
ANALYSIS_PATH = ABSOLUTE_PATH + LATEST_DATA_FOLDER + "Analysis"
ANALYSIS_DATE = '21-04-2020'
ANALYSIS_DAYS = 500


def update_latest_data_folder(folder: str):
    global LATEST_DATA_FOLDER, SCHEME_DATA_PATH, ANALYSIS_PATH

    LATEST_DATA_FOLDER = folder
    SCHEME_DATA_PATH = ABSOLUTE_PATH + LATEST_DATA_FOLDER + "Data"
    ANALYSIS_PATH = ABSOLUTE_PATH + LATEST_DATA_FOLDER + "Analysis"
