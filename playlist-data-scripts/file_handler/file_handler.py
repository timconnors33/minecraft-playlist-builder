from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd

load_dotenv(find_dotenv())

# TODO: Add error handling
def writeToCsv(df, filepath):
    if os.environ.get('ENVIRONMENT') == 'production' or not os.path.exists(filepath):
        df.to_csv(filepath)
    return filepath
    
def readFromCsv(filepath):
    return pd.read_csv(filepath)