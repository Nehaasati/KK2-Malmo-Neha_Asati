from app.data import load_csv

metadata = load_csv("datasets/amazon_reviews.csv")

print(metadata)

import pandas as pd

# this code is used to load a CSV file and get statistics about the loaded dataset. It uses the pandas library to handle CSV files and data manipulation.
# Global variable in order to store the loaded dataset. Initially set to None, it will hold the DataFrame once a CSV file is loaded using the load_csv function.
DATA = None

# Function in order to load a CSV file into the global DATA variable. It reads the CSV file using pandas and stores it in DATA. The function returns a dictionary containing the number of rows, the list of column names, and the data types of each column in the loaded dataset.
def load_csv(file) -> dict:
    global DATA
    DATA = pd.read_csv(file)
    return {
        "rows": len(DATA),
        "columns": list(DATA.columns),
        "dtypes": DATA.dtypes.astype(str).to_dict()
    }

# Function in order to get statistics about the loaded dataset. If no dataset has been loaded, it returns None. Otherwise, it returns a description of the dataset in the form of a dictionary.
def get_stats():
    if DATA is None:
        return None
    return DATA.describe().to_dict()