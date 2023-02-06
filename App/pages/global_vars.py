import pandas as pd
from utility.data_functions import get_data
from collections import defaultdict

#IDEAS FOR THIS FILE:
#- add occupancy csv and urls as global variables for easier accessing?
#- move more functions over here? e.g. reset_data etc


#global variables defined here will be accesible in files that import this file
global data, current_filter
#dataframe that stores all location data that is currently displayed
data = None
#dictionary with key:value pairs of "characteristic name" : [accepted values of characteristics]
#will be used to filter data
current_filter = None

#these vars will be used to import files and tmporarily save the inputs
temp_csv = None
temp_json = None

#initialize all global variables
def init():
    #initialize data with all data in characteristics csv
    global data
    try:
        data = get_data(name_of_csv="Characteristics.csv")
    except:
        raise Exception("Something went wrong when intialising the global data!")
    #initialise dictionary as default dictionary where not having a value returns None
    global current_filter
    current_filter = defaultdict(lambda: None)


def reset_global_filter():
    """
    function that resets the dictionary that tracks the current filters
    """
    global current_filter
    current_filter = defaultdict(lambda: None)


def reset_data(name="Characteristics.csv"):
    """
    Resets the data with reading it new from a csv in the data folder with the given name
    """
    global data
    data = get_data(name)
