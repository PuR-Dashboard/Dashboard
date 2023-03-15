from utility.data_functions import get_data
from collections import defaultdict


#-----------variable declaration-------------


#global variables defined here will be accesible in files that import this file
global data, current_filter, occupancy

#dataframe that stores all location data that is currently displayed
data = None

#dictionary with key:value pairs of "characteristic name" : [accepted values of characteristics]
#will be used to filter data
current_filter = None

#these vars will be used to import files and tmporarily save the inputs
temp_csv = None
temp_json = None

#current error message to display between callbacks
curr_error = None

#-------------------------------------



#-----------functions-----------------

def init()-> None:
    """
    This function initializes all global variables accirding to the data(chracteristics.csv).

    Raises
    ------
    Exception
        If it was not possible to inalize the global variables according to the csv files.
    """


    global data,occupancy

    #initialization of the global variabls data and occupancy
    try:
        data = get_data(name_of_csv="Characteristics.csv")
        occupancy = get_data(name_of_csv="Occupancy.csv")
    except:
        raise Exception("Something went wrong when intialising the global data!") # throws an exception if an error occurs during the inialization of the global variabls data and occupancy

    #initialise filter dictionary as default dictionary
    global current_filter
    current_filter = defaultdict(lambda: None)


def reset_global_filter()-> None:
    """
    This function resets the dictionary that tracks the current filters.
    """

    global current_filter
    current_filter = defaultdict(lambda: None) #reseting the current filter dict to a default(empty) dictionary


def reset_data(name="Characteristics.csv")->None:
    """
    Thid function resets the data(global variable) by the given file name.

    Parameters
    ----------
    name:
        The name of the csv file which data should be saved in the global data variable.
    """
    global data
    data = get_data(name) # reseting the data according to the stored informations in the given file name


#---------------------------------------
