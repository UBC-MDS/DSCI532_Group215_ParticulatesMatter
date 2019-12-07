#This script processes PM10 and PM25 datasets that were taken from the source below:
#https://catalogue.data.gov.bc.ca/dataset/air-quality-monitoring-unverified-hourly-air-quality-and-meteorological-data

# Import Dependencies for processing
import pandas as pd
import numpy as np

# Dictionary containing city name key values for each station
name_filter = {"Abbotsford Central": "Abbotsford",
              "Burnaby Kensington Park": "Burnaby",
             'Burnaby South': "Burnaby",
             'Burns Lake Fire Centre': "Burns Lake",
             'Campbell River Tyee Spit': "Campbell River",
             'Castlegar Zinio Park': "Castlegar",
              'Chilliwack Airport': "Chilliwack",
             'Colwood City Hall': "Colwood",
             'Cranbrook Forest Fire': "Cranbrook",
             'Creston PC School': "Creston",
             'Crofton Substation': "Crofton",
             'Duncan Deykin Avenue': "Duncan",
             'Duncan Mobile Transfer Station':"Duncan",
             'Elk Falls Dogwood':"Elk Falls",
             'Farmington MAML': "Farmington",
             'Fort Nelson Chalo School':"Fort Nelson",
             'Fort St John Key Learning Centre':"Fort St. John",
             'Fort St John NP Cultural Centre': "Fort St. John",
             'Golden CPR': "Golden",
             'Golden Golf Course': "Golden",
             'Golden Helipad' : "Golden",
             'Golden Hospital' : "Golden",
             'Golden Townsite' : "Golden",
             'Groundbirch MAML' : "Groundbirch",
             'Harmac Cedar Woobank' : "Harmac",
             'Hope Airport': "Hope",
             'Houston Firehall': "Houston",
             'Kamloops Aberdeen' : "Kamloops",
             'Kamloops Brocklehurst' : "Kamloops",
             'Kelly Lake MAML': "Kelly Lake",
             'Kelowna College' : "Kelowna",
             'Kitimat City Centre MAML': "Kitimat",
             'Kitimat Haul Road': "Kitimat",
             'Kitimat Rail': "Kitimat",
             'Kitimat Riverlodge': "Kitimat",
             'Kitimat Whitesail': "Kitimat",
             'Langdale Elementary': "Langdale",
             'Langley Central':"Langley",
             'Merritt Granite-Garcia Mobile':"Meritt",
             'Moricetown MAML': "Moricetown",
             'Nanaimo Labieux Road': "Nanaimo",
             'Nelson Kutenai Place':"Nelson",
             'North Vancouver Mahon Park':"North Vancouver",
             'Osoyoos Shaw Gardens': "Osoyoos",
             'Pitt Meadows Meadowlands School':"Pitt Meadows",
             'Port Moody Rocky Point Park':"Port Moody",
             'Powell River Cranberry Lake':"Powell River",
             'Powell River James Thomson School':"Powell River",
             'Powell River Wildwood':"Powell River",
             'Prince George Gladstone School': "Prince George",
             'Prince George Hwy 16/97 MAML': "Prince George",
             'Prince George Plaza 400': "Prince George",
             'Quadra Island Cape Mudge Village': "Quadra Island",
             'Quesnel Maple Drive': "Quesnel",
             'Quesnel Pinecrest Centre': "Quesnel",
             'Quesnel Senior Secondary': "Quesnel",
             'Quesnel West Correlieu School': "Quesnel",
             'Revelstoke Mt Begbie School':"Revelstoke",
             'Richmond South':"Richmond",
             'Rolla MAML':"Rolla",
             'Smithers St Josephs':"Smithers",
             "Squamish Gov't Bldg":"Squamish",
             'Surrey East':"Surrey",
             'Terrace BC Access Centre':"Terrace",
             'Tomslake MAML':"Tomslake",
             'Trail Aquatic Centre':"Trail",
             'Valemount Firehall':"Valemount",
             'Vancouver International Airport #2':"Vancouver",
             'Vancouver Kitsilano':"Vancouver",
             'Vanderhoof Courthouse':"Vanderhoof",
             'Vernon Science Centre':"Vernon",
             'Victoria James Bay MAML':"Victoria",
             'Whistler Function Junction MAML':"Whistler",
             'Williams Lake CRD Library':"Williams Lake",
             'Williams Lake Columneetza School':"Williams Lake",
             'Williams Lake Skyline School':"Williams Lake"}


### Define Functions
def process_dataset(original_df, baseline = False):
    """
    Takes in a dataframe and processes it, and then returns a processed Pandas DataFrame

    Arguments:
    original_df -- (DataFrame) the dataframe that will be processed
    """


    # Keep only useful columns
    processed_df = original_df[["STATION_NAME","PARAMETER", "RAW_VALUE"]]

    # Alter the datetime format to one that contains only months and years
    # https://medium.com/@deallen7/managing-date-datetime-and-timestamp-in-python-pandas-cc9d285302ab
    processed_df.index =  processed_df.index.strftime('%Y-%m')

    # Obtain mean value of pollutant concentration for each month (and each location if baseline parameter is False)
    if baseline == False:
        processed_df = processed_df.reset_index().groupby(["index","STATION_NAME","PARAMETER"]).agg({"RAW_VALUE": "mean"})
    else:
        processed_df = processed_df.reset_index().query('STATION_NAME in @shared_locations').groupby(["index","PARAMETER"]).agg({"RAW_VALUE": "mean"})

    return(processed_df)

def get_summary(df_combined):
    """
    Takes in combined DataFrame object, and calculates summary statistics for every location and pollutant type

    Arguments:
    df_combined -- (DataFrame) Input dataset
    """

    summary_stats = df_combined.groupby(["STATION_NAME", "PARAMETER"]).agg({"RAW_VALUE": ["max", "min", "mean", "median", "std", "var"]})
    return summary_stats

### Main Processes

# Read in data
PM10_data = pd.read_csv('ftp://ftp.env.gov.bc.ca/pub/outgoing/AIR/AnnualSummary/2000-2016/pm10.csv', 
                        index_col = 'DATE_PST', 
                        parse_dates = True)


PM25_data = pd.read_csv('ftp://ftp.env.gov.bc.ca/pub/outgoing/AIR/AnnualSummary/2000-2016/pm25.csv', 
                        index_col = 'DATE_PST', 
                        parse_dates = True)

# Change name of each location to reflect just the city name
for key,value in name_filter.items():
    PM10_data["STATION_NAME"] = PM10_data["STATION_NAME"].replace(key, value)
    PM25_data["STATION_NAME"] = PM25_data["STATION_NAME"].replace(key, value)
    
# Find all the Station Locations that PM10 and PM25 datasets have in common
shared_locations = ["Powell River", "Prince George", "Quesnel", "Williams Lake", "Houston", "Kitimat", "Golden", "Kelowna", "Smithers", "Vancouver"]
#shared_locations = set(PM10_data["STATION_NAME"].unique()).intersection(set(PM25_data["STATION_NAME"].unique()))

# Get avg pollutant concentrations for each location, as well as the overall trend (baseline)
PM10_processed = process_dataset(PM10_data)
PM25_processed = process_dataset(PM25_data)
PM10_baseline = process_dataset(PM10_data, baseline = True)
PM25_baseline = process_dataset(PM25_data, baseline = True)

# Combine the PM10 and PM25 Dataframes by row
combined_data = pd.concat([PM10_processed, PM25_processed]).query('STATION_NAME in @shared_locations').reset_index().sort_values(by = ["STATION_NAME", 'index'])
combined_baseline_data = pd.concat([PM10_baseline, PM25_baseline]).reset_index().sort_values(by = ['index'])

combined_data['index'] = pd.to_datetime(combined_data['index']).astype('str')
combined_baseline_data['index'] = pd.to_datetime(combined_baseline_data['index']).astype('str')

# Export the processed files
combined_data.to_csv("/data/processed_data.csv")
combined_baseline_data.to_csv("/data/processed_baseline_data.csv")
get_summary(combined_data).to_csv("/data/location_summary.csv")

