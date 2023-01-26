import pandas as pd
import os
import pathlib
from collections import defaultdict
#import pages.global_vars as glob_vars


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


def get_path_to_csv(name_of_csv="Characteristics.csv", app_name="App"):
    data_path = get_root_dir(app_name)

    return os.path.join(data_path, os.path.join("Data", name_of_csv))


#get data stored in our Location Data and return DataFrame
def get_data(name_of_csv="Characteristics.csv", app_name="App"):
    #data_path = get_root_dir(app_name)
    #print(os.path.join(data_path, os.path.join("Data", name_of_csv)))
    df = pd.read_csv(get_path_to_csv(name_of_csv, app_name))
    return df

#DEPRECATED?
def reverse_parking_lot_list(value_list, marks):
    if value_list == None:
        return None

    index_list = set()
    for i in range(1, len(marks)):
        if marks[str(i)] + "-" + marks[str(i+1)] in value_list:
            index_list.add(i)
            index_list.add(i + 1)
    
    index_list = list(index_list)
    return [index_list[0], index_list[-1]]

#DEPRECATED?
def make_parking_lot_list(mini, maxi, values):
    value_list = []

    for i in range(mini, maxi):
        i_range = values[str(i)] + "-" + values[str(i+1)]
        value_list.append(i_range)

    return value_list


