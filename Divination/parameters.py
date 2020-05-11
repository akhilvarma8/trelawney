# Parameters for fetching data
API_URL = 'https://api.mfapi.in/mf/'

# Parameters for storing and accessing fetched data
ABSOLUTE_PATH = '/Users/akhilvarma/Documents/Development/Mutual Fund Data/'
LATEST_DATA_FOLDER = '2020-05-07/'
RAW_DATA_PATH = ABSOLUTE_PATH + LATEST_DATA_FOLDER + "Data/"


# Parameters for analysing data
ANALYSIS_PATH = ABSOLUTE_PATH + LATEST_DATA_FOLDER + "Analysis"


def update_latest_data_folder(folder: str):
    global LATEST_DATA_FOLDER, RAW_DATA_PATH, ANALYSIS_PATH

    LATEST_DATA_FOLDER = folder
    RAW_DATA_PATH = ABSOLUTE_PATH + LATEST_DATA_FOLDER + "Data"
    ANALYSIS_PATH = ABSOLUTE_PATH + LATEST_DATA_FOLDER + "Analysis"
