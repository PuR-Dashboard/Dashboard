import sklearn, numpy
import pandas as pd
from utility.util_functions import *
from collections import defaultdict
import pages.global_vars as glob_vars


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

def filter_max_value(df, category, max_value):
    if max_value == None:
        return df

    #df2 = df.drop(df.loc[df[category] > str(max_value)].index)
    df2 = df.drop(df.loc[df[category] > max_value].index)
    df2 = df2.reset_index(drop = True)
    return df2


def filter_for_value(df:pd.DataFrame, category:str, set_value:str):
    if set_value == None:
        return df

    df2 = df.drop(df.loc[df[category] != set_value].index)
    df2 = df2.reset_index(drop = True)
    return df2

def filter_for_list(df:pd.DataFrame, category:str, set_list:list):
    if set_list == None or len(set_list) == 0:
        return df

    df2 = df.drop(df.loc[~df[category].isin(set_list)].index)
    df2 = df2.reset_index(drop = True)
    return df2


def filter_for_index(df, index):
    df.drop(index)
    df.reset_index(drop = True)
    return df


def filter_names(df, filteraspect):

    to_delete = []
    index = []
    Deleted = False

    filterchar = [char for char in filteraspect]

    index = 0
    while (index < len(df['location'])):

        Deleted = False

        location = df.iloc[index]['location']
        locationchar =  [char for char in location]

        #einzelnen Buchstaben vergleichen
        for i in range(len(filterchar)):

            #wenn filterwort zu lang ist
            if ( i >= (len(locationchar))):
                Deleted = True
                df.drop(df.loc[df['location']== location].index, inplace = True )
                df.reset_index(drop = True, inplace = True)
                break
                #z = z-1

            #wenn eins nicht identisch ist -> raus löschen
            elif (filterchar[i] != locationchar[i]):
                Deleted = True
                df.drop(df.loc[df['location']== location].index, inplace = True )
                df.reset_index(drop = True, inplace = True)
                break
                #z = z-1


        if (not Deleted):
            index += 1


    return df


def get_occupancy_list_from_vals(occupancy_vals):
    if occupancy_vals == None:
        return []

    #occupancy csv auslesen
    occupancy_csv = get_data("Occupancy.csv")
    #alle namen(=Spalten) filtern wo letzte occupancy zeile in values ist
    name_list = []
    for col in occupancy_csv.columns.values:
        if occupancy_csv[col].empty or occupancy_csv[col].tolist()[-1] == None:
            continue
        elif occupancy_csv[col].tolist()[-1] in occupancy_vals:
            name_list.append(col)

    return name_list
    #an der stelle occupancy die lsite an locations einfügen


def reset_global_filter():
    glob_vars.current_filter = defaultdict(lambda: None)


def filter_data():#filter_dict: dict[str:str]):
    #global data

    glob_vars.data = filter_content(glob_vars.data, glob_vars.current_filter)

def reset_data(name="Characteristics.csv"):
    glob_vars.data = get_data(name)


#filtering the given df for the characteristics in the filter_dict
def filter_content(df: pd.DataFrame, filter_dict:defaultdict):
    """
    df: Dataframe with user content to be filtered
    filter_dict: default dictionary with all characteristics to be filtered for as keys, value to be filtered for as value and default value as none

    returns: filtered dataframe by standards of filter_dict
    """
    

    #if none then no location name was given the filter, so no filtering
    keys = df.columns.values
    for key in keys:
        if filter_dict[key] == None:
            continue
        elif key == "location":
            df = filter_names(df, filter_dict[key])
        #value for occupation key is a list of location names that fulfill occupancy filter criteria
        elif key == "occupancy":
            df = df = filter_for_list(df, "location", get_occupancy_list_from_vals(filter_dict[key]))
        elif type(filter_dict[key]) == str:
            df = filter_for_value(df, key, filter_dict[key])
        elif type(filter_dict[key]) == list:
            df = filter_for_list(df, key, filter_dict[key])
        elif type(filter_dict[key]) == int or type(filter_dict[key]) == float:
            df = filter_max_value(df, key, filter_dict[key])

    return df
