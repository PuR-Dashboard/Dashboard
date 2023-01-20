import pandas as pd
import os
import pathlib


#get the top directory of our app, regardless of depth
#TO-DO: Error if while loop breaks and nothing matching was found
def get_root_dir(name_of_top_folder="App"):
    current_path = pathlib.Path(__file__).parent.resolve()
    parent_path = current_path
    while os.path.basename(parent_path) != name_of_top_folder:
        parent_path = parent_path.parent.absolute()

        if parent_path.parent.absolute() == parent_path:
            break


    parent_path = parent_path.parent.absolute()

    return parent_path


def get_path_to_csv(name_of_csv="Location_Data.csv", app_name="App"):
    data_path = get_root_dir(app_name)

    return os.path.join(data_path, os.path.join("Data", name_of_csv))


#get data stored in our Location Data and return DataFrame
def get_data(name_of_csv="Location_Data.csv", app_name="App"):
    #data_path = get_root_dir(app_name)
    #print(os.path.join(data_path, os.path.join("Data", name_of_csv)))
    df = pd.read_csv(get_path_to_csv(name_of_csv, app_name))
    return df
