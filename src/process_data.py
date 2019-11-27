#This script processes PM10 and PM25 datasets that were taken from the source below:
#https://catalogue.data.gov.bc.ca/dataset/air-quality-monitoring-unverified-hourly-air-quality-and-meteorological-data

# Import Dependencies for processing
import pandas as pd
import numpy as np

# Read in data from server
PM10_data = pd.read_csv('ftp://ftp.env.gov.bc.ca/pub/outgoing/AIR/AnnualSummary/2000-2016/pm10.csv', 
                        index_col = 'DATE_PST', 
                        parse_dates = True)
PM25_data = pd.read_csv('ftp://ftp.env.gov.bc.ca/pub/outgoing/AIR/AnnualSummary/2000-2016/pm25.csv', 
                        index_col = 'DATE_PST', 
                        parse_dates = True)

# Find all the Station Locatins that PM10 and PM25 datasets have in common
shared_columns = set(PM10_data["STATION_NAME"].unique()).intersection(set(PM25_data["STATION_NAME"].unique()))

def process_dataset(df):
    """
    Takes in a dataframe and processes it, and then returns a processed Pandas DataFrame

    Arguments:
    df -- (DataFrame) the dataframe that will be processed
    """


    # Keep only useful columns
    df = df[["STATION_NAME","PARAMETER", "RAW_VALUE"]]

    # Alter the datetime format to one that contains only months and years
    # https://medium.com/@deallen7/managing-date-datetime-and-timestamp-in-python-pandas-cc9d285302ab
    df.index =  df.index.strftime('%Y-%m')

    #Obtain mean value of pollutant concentration for each month
    df = df.reset_index().groupby(["index","STATION_NAME","PARAMETER"]).agg({"RAW_VALUE": "mean"})
    return(df)

PM10_data = process_dataset(PM10_data)
PM25_data = process_dataset(PM25_data)

# Combine the PM10 and PM25 Dataframes by row
combined_data = pd.concat([PM10_data, PM25_data]).query('STATION_NAME in @shared_columns').reset_index().sort_values(by = ["STATION_NAME", 'index'])

# Export the processed file
combined_data.to_csv("data/processed_data.csv")

def get_summary(df_combined):

    summary_stats = df_combined.groupby("STATION_NAME").agg({"RAW_VALUE": ["max", "min", "mean", "median", "std", "var"]})
    return summary_stats

get_summary(combined_data).to_csv("data/location_summary.csv")