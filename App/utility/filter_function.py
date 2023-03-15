import pandas as pd
from utility.data_functions import *
from collections import defaultdict
import pages.global_vars as glob_vars
import ast

#------helping functions----------------


def filter_max_value(df: pd.DataFrame, category:str, max_value:int) -> pd.DataFrame:
    """
    This function creates a dataframe which is based on the given DataFrame and filtered by the category and the maximum value.

    Parameters
    ----------
    df:
        The Dataframe to be filtered on.

    category:
        The column(characteristic) name in which should be filtered.

    max_value:
        A maximum value for the filtering process. All values for the category which are over this value should be filtered out.

    Returns
    -------
    df2:
        A filtered DataFrame based on the parameters.

     Raises
    ------
    Exception
        If filtering the df based on the category and the max value went wrong.
    """

    #if no value given, dont filter

    if max_value == None:
        return df

    #filtering process
    try:
        df2 = df.drop(df.loc[df[category] > float(max_value)].index) #dropping all rows of the datframe which value for the given category is higher than the max_value
    except Exception as e:

        raise Exception("Something went wrong while filtering for a maximum value!")

    #reset the index and return df
    df2 = df2.reset_index(drop = True)
    return df2


def filter_for_value(df:pd.DataFrame, category:str, set_value:str) -> pd.DataFrame:
    """
    This function creates a dataframe which is based on the given DataFrame and filtered by the category and the certain value of the characteristic.

    Parameters
    ----------
    df:
        The Dataframe to be filtered on.

    category:
        The column(characteristic) name in which should be filtered.

    set_value:
        The value to be filtered by.

    Returns
    -------
    df2:
        A filtered DataFrame based on the parameters.

    Raises
    ------
    Exception
        If filtering the df based on the category and the set value went wrong.
    """
    print(set_value)
    #if no value given, dont filter
    if set_value == None:
        return df

    #filtering process
    try:
        df2 = df.drop(df.loc[df[category].apply(lambda x: x.lower()) != set_value.lower()].index) #dropping all rows of the datframe which value for the given category does not euqal the given value
    except Exception as e:
         raise Exception("Something went wrong when filtering for a value!")

    #reset index and return df
    df2 = df2.reset_index(drop = True)
    return df2


def filter_for_list(df:pd.DataFrame, category:str, set_list:list,  filter_occupancy=False) -> pd.DataFrame:
    """
    This function creates a dataframe which is based on the given DataFrame and filtered by the category and the list of certain values.

    Parameters
    ----------
    df:
        The Dataframe to be filtered on.

    category:
        The column(characteristic) name in which should be filtered.

    set_list:
        A list of value to be filtered by.

    filter_occupancy:
        Whether it should be filtered by the occupancy.

    Returns
    -------
    df2:
        A filtered DataFrame based on the parameters.

    Raises
    ------
    Exception
        If filtering the df based on the category and the set list went wrong.
    """

    #if we want to filter for the occupany but the set list is empty returning the first element of the dataframe
    if filter_occupancy and len(set_list) == 0:
        return df[0:0]

    #if no list given or if empty list, dont filter
    if set_list == None or len(set_list) == 0:
        return df
    
    set_list = [x.lower() for x in set_list]

    #filtering process
    try:
        df2 = df.drop(df.loc[~df[category].apply(lambda x: x.lower()).isin(set_list)].index) #dropping all rows of the datframe which value for the given category is not on the list of possible values
    except Exception as e:
        raise Exception("Something went wrong when filtering for a list of values!")


    #drop index and return df
    df2 = df2.reset_index(drop = True)
    return df2



def filter_names(df:pd.DataFrame, filteraspect:str, key:str) -> pd.DataFrame:
    """
    This function creates a dataframe which is based on the given DataFrame and filtered in the category by the search entry.

    Parameters
    ----------
    df:
        The Dataframe to be filtered on.

    filteraspect:
        The search entry by filtering of a name of a location.

    key:
        The column(characteristic) name in which should be filtered.

    Returns
    -------
    df2:
        A filtered DataFrame based on the paramters.
    """
    #initialize and preprocessing
    to_delete = []
    index = []
    Deleted = False

    filterchar = [char.lower() for char in filteraspect] # creating an char array of the string we are searching for

    #iterate through all rows of the dataframe
    index = 0
    while (index < len(df[key])):

        #track if row was deleted(for index management)
        Deleted = False

        #get value of current row at given key
        location = df.iloc[index][key]

        #preprocess value in row
        locationchar =  [char.lower() for char in location]

        #compare characterized input and value for similarity
        for i in range(len(filterchar)):

            #if search entry is too long
            if ( i >= (len(locationchar))):
                Deleted = True
                df.drop(df.loc[df[key]== location].index, inplace = True ) #dropping the location which is too short for the string
                df.reset_index(drop = True, inplace = True) # reseting the index
                break


            #if all characters up to this point do not match
            elif (filterchar[i] != locationchar[i]):
                Deleted = True
                df.drop(df.loc[df[key]== location].index, inplace = True ) # dropping the location which does not match to the given string
                df.reset_index(drop = True, inplace = True) # reseting the index
                break

        #adjust index if recently deleted
        if (not Deleted):
            index += 1

    #return filtered dataframe
    return df


def get_occupancy_list_from_vals(occupancy_vals:list[str]) -> list[str]:
    """
    This function obtain a list of location names that satisfy the given criteria of occupancy.

    Parameters
    ----------
    occupancy_vals:
        A list of acceptable occupancy values for filtering.

    Returns
    -------
    name_list:
        A list of the location names that satisfy the given criteria.
    """

    #temporary dictionary while we haven't translated the values yet wil be removed in the end!
    translation_dict = {"high":"keine vorhanden", "medium":"wenige vorhanden", "low":"ausreichend vorhanden"} #korrekte bezeichnung für high occupancy???

    #convert list to german values
    occupancy_vals = [translation_dict[o] for o in occupancy_vals]

    #if no list given
    if occupancy_vals == None:
        return None

    #read occupancy csv
    occupancy_csv = get_data("Occupancy.csv")

    #names that conform to occupancy values
    name_list = []

    #iterate all location names(=column names) for last column value
    for col in occupancy_csv.columns.values[1:]:
        #error prevention if no (valid) values in column then location does not suffice
        if occupancy_csv[col].empty or occupancy_csv[col].tolist()[-1] == None:
            continue

        #if last column value(=latest value) is equal to criteria then add location name
        occ_value_string = occupancy_csv[col].tolist()[-1]
        occ_value = ast.literal_eval(occ_value_string)[-1]

        # changing it to the right language
        if occ_value in occupancy_vals:
            name_list.append(col)

    return name_list




def filter_content(df: pd.DataFrame, filter_dict:defaultdict) -> pd.DataFrame:
    """
    This function creates a dataframe which is based on the given DataFrame and filtered in the category by the search entry.

    Parameters
    ----------
    df:
        The Dataframe to be filtered on.

    filter_dict:
        A default dictionary with all characteristics to be filtered for as keys, value to be filtered for as value and default value as None.

    Returns
    -------
    df:
        The dataframe filtered by the information of the filter_dict.
    """

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

            oc = filter_dict[key]

            if type(oc) != list:
                oc = [oc]
            else:
                if len(oc) == 0:
                    continue

            df = filter_for_list(df, "location", get_occupancy_list_from_vals(oc), filter_occupancy=True)

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

#------------------------------------------------------------

#----------filter the data--------------------------------

def filter_data()-> None:
    """
    This function filters the current data with the currently applied filters.

    Raises
    ------
    Exception
        If an error occurs while filtering the content.
    """
    try:
        glob_vars.data = filter_content(glob_vars.data, glob_vars.current_filter)
    except Exception as e:
        glob_vars.curr_error = e


#------------------------------------------------------------
