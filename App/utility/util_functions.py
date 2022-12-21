import pandas as pd
import os
import pathlib


# get the top directory of our app, regardless of depth
# TODO: Error if while loop breaks and nothing matching was found
def get_root_dir(name_of_top_folder="Dashboard-main"):
    """
    Get the top directory of our app, regardless of depth
    :param name_of_top_folder:
    :return:
    """
    current_path = pathlib.Path(__file__).parent.resolve()  # Get the current path

    parent_path = current_path  # Set the parent path to the current path

    while os.path.basename(parent_path) != name_of_top_folder:  # While the parent path is not the top directory
        parent_path = parent_path.parent.absolute()  # Set the parent path to the parent of the current path

        if parent_path.parent.absolute() == parent_path:  # If the parent path is the same as the current path
            break  # Break the loop

    return parent_path  # Return the parent path


# Get data stored in our Location Data and return DataFrame
def get_data(name_of_csv="Location_Data.csv"):
    """
    Get data stored in our Location Data and return DataFrame
    :param name_of_csv: The name of the csv file
    :return: The DataFrame containing the data
    """
    data_path = get_root_dir()  # Get the top directory of our app

    df = pd.read_csv(os.path.join(data_path, os.path.join("Data", name_of_csv)))  # Read the csv file

    return df  # Return the DataFrame
