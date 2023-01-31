import sklearn, numpy
import pandas as pd
from utility.util_functions import *
from collections import defaultdict
import pages.global_vars as glob_vars

#CURRENTLY UNUSED/DEPRECATED
def filter_all(df: pd.DataFrame, filter_df: dict[str:str], negative=False)-> pd.DataFrame:
    df_copy = df.copy(deep=True)

    for k in filter_df:
        df = filter_for_value(df, k, filter_df[k])


    if negative:
        keys = list(df.columns.values)
        i1 = df_copy.set_index(keys).index
        i2 = df.set_index(keys).index
        return df_copy[~i1.isin(i2)]

    else:
        return df

                                                    #maybe max_value ist ein string?????
def filter_max_value(df: pd.DataFrame, category:str, max_value:int) -> pd.DataFrame:
    """
    given a dataframe, a category and a value, then filters the dataframe for all values smaller or equal than that value

    df: Dataframe to be filtered on
    category: column name in which should be filtered
    max_value: maximum value for filtering process

    returns: filtered dataframe
    """
    
    #if no value given, dont filter
    if max_value == None:
        return df

    #filtering process
    try:
        df2 = df.drop(df.loc[df[category] > max_value].index)
    except Exception as e:
        raise e("Something went wrong while filtering for a maximum value!")
    #reset the index and return df
    df2 = df2.reset_index(drop = True)
    return df2


def filter_for_value(df:pd.DataFrame, category:str, set_value:str) -> pd.DataFrame:
    """
    given a dataframe, a category and a value, then filters the dataframe for all rows that have this value

    df: Dataframe to be filtered on
    category: column name in which should be filtered
    set_value:  value for filtering process

    returns: filtered dataframe 
    """
    #if no value given, dont filter
    if set_value == None:
        return df
    #filtering process
    try:
        df2 = df.drop(df.loc[df[category] != set_value].index)
    except Exception as e:
        raise e("Something went wrong when filtering for a value!")
    #reset index and return df
    df2 = df2.reset_index(drop = True)
    return df2


def filter_for_list(df:pd.DataFrame, category:str, set_list:list,  filter_occupancy=False) -> pd.DataFrame:
    """
    given a dataframe, a category and a list of values, then filters the dataframe for all rows that have one of these values

    df: Dataframe to be filtered on
    category: column name in which should be filtered
    set_list: list of values for filtering process

    returns: filtered dataframe
    """
    print(df, set_list)

    if filter_occupancy and len(set_list) == 0:
        return df[0:0]

    #if no list given or if empty list, dont filter
    if set_list == None or len(set_list) == 0:
        return df
    #filtering process
    try:
        df2 = df.drop(df.loc[~df[category].isin(set_list)].index)
    except Exception as e:
        raise e("Something went wrong when filtering for a list of values!")
    #drop index and return df
    df2 = df2.reset_index(drop = True)
    return df2


#DEPRECATED/SOON TO BE DEPRECATED?
def filter_for_index(df, index):
    df.drop(index)
    df.reset_index(drop = True)
    return df



def filter_names(df:pd.DataFrame, filteraspect:str, key:str) -> pd.DataFrame:
    """
    Function that takes a dataframe, a search entry and a category and filters for all row values that could be meant by the entry

    df: Dataframe to be filtered on
    filteraspect: search entry, i.e. start of a location("Heid" from "Heidelberg")
    key: column name to be filtered in

    returns: filtered dataframe
    """
    #initialize and preprocessing
    to_delete = []
    index = []
    Deleted = False

    filterchar = [char for char in filteraspect]

    #iterate through all rows of the dataframe
    index = 0
    while (index < len(df[key])):

        #track if row was deleted(for index management)
        Deleted = False

        #get value of current row at given key
        location = df.iloc[index][key]
        #preprocess value in row
        locationchar =  [char for char in location]

        #compare characterized input and value for similarity
        for i in range(len(filterchar)):

            #if search entry is too long
            if ( i >= (len(locationchar))):
                Deleted = True
                df.drop(df.loc[df[key]== location].index, inplace = True )
                df.reset_index(drop = True, inplace = True)
                break
                

            #if all characters up to this point do not match
            elif (filterchar[i] != locationchar[i]):
                Deleted = True
                df.drop(df.loc[df[key]== location].index, inplace = True )
                df.reset_index(drop = True, inplace = True)
                break

        #adjust index if recently deleted
        if (not Deleted):
            index += 1

    #return filtered dataframe
    return df


def get_occupancy_list_from_vals(occupancy_vals:list[str]) -> list[str]:
    """
    Function to obtain a list of location names that satisfy the given criteria of occupancy.

    occupancy_vals: list of acceptable occupancy values for filtering

    returns: list of location names that satisfy criteria
    """
    #if no list given
    if occupancy_vals == None:
        return None

    #read occupancy csv
    occupancy_csv = get_data("Occupancy.csv")
    
    #names that conform to occupancy values
    name_list = []
    #iterate all location names(=column names) for last column value
    for col in occupancy_csv.columns.values:
        #error prevention if no (valid) values in column then location does not suffice
        if occupancy_csv[col].empty or occupancy_csv[col].tolist()[-1] == None:
            continue
        #if last column value(=latest value) is equal to criteria then add location name
        elif occupancy_csv[col].tolist()[-1] in occupancy_vals:
            name_list.append(col)

    #return list
    return name_list
    


def reset_global_filter():
    """
    function that resets the dictionary that tracks the current filters
    """
    glob_vars.current_filter = defaultdict(lambda: None)


def filter_data():
    """
    filters the current data with the currently applied filters
    """
    glob_vars.data = filter_content(glob_vars.data, glob_vars.current_filter)

def reset_data(name="Characteristics.csv"):
    """
    Resets the data with reading it new from a csv in the data folder with the given name
    """
    glob_vars.data = get_data(name)


def filter_content(df: pd.DataFrame, filter_dict:defaultdict) -> pd.DataFrame:
    """
    df: Dataframe with user content to be filtered
    filter_dict: default dictionary with all characteristics to be filtered for as keys, value to be filtered for as value and default value as None

    returns: filtered dataframe by standards of filter_dict
    """
    #print("inside filter content")
   #iterate over all characteristics/keys of the data
    keys = df.columns.values
    for key in filter_dict:
         #if None then no value to filter for was given, so no filtering
        if filter_dict[key] == None:
            continue
        #location and address are filtered by the autocomplete method filter names
        elif key == "location" or key == "address":
            df = filter_names(df, filter_dict[key], key)
        #occupancy values have to be preprocessed, and filtering happens on location names based on that, hence own if statement
        elif key == "occupancy":
            #print("gotscha")
            df = filter_for_list(df, "location", get_occupancy_list_from_vals(filter_dict[key]), filter_occupancy=True)
        #if single string is given, only filter for that value(this statement will probably not be called)
        elif type(filter_dict[key]) == str:
            df = filter_for_value(df, key, filter_dict[key])
        #if type is list, filter for list values
        elif type(filter_dict[key]) == list:
            df = filter_for_list(df, key, filter_dict[key])
        #if number is given, filter for maximum number
        elif type(filter_dict[key]) == int or type(filter_dict[key]) == float:
            df = filter_max_value(df, key, filter_dict[key])

    return df
