from gc import callbacks
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback,ctx
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate
import os
from utility import map_functions
from utility.map_functions import *
from pandas import read_csv
from pages import list_page
#from utility.util_functions import *
from components.sidebar import get_sidebar
from utility.data_functions import *
from utility.filter_funktion import *
import pages.global_vars as glob_vars
from collections import defaultdict



CONTENT_STYLE = { #style the content of map_page so that it aligns with the sidebar
    "position": "fixed",
    "width": "calc(100vw - 250px)",
    "height": "calc(100vh - 50px)",
   # "resize":"both",
    "flex-grow": "1",
    #"border":"none",
    "seamless":"True"

}

#seitentag = "_map"

#html_list = []

#global data, temp_data

#global sid
#sid = get_sidebar(seitentag)

#data = get_data(name_of_csv="Characteristics.csv")
#temp_data = data.copy(deep=True)

#method to create the html which represents the map_page
#returns the layout of the map_page as a HTML List
def create_html_map(data):
    global sid

    html_list = []

    map_functions.create_map(data) # create the map
    html_list.append(  # Append the map tp the map_page
                    html.Iframe( #Create an Iframe element to get an interactive map
                    id="page-layout", # Set the id of the Iframe element
                    srcDoc=open(os.path.join(os.path.dirname(__file__), '../P&R_Karte.html'), "r").read(),# Set the source of the Iframe element to be the previously created map
                     #width="87%", height="800", # set the width and the height of the IFrame Element
                     style = CONTENT_STYLE

                     ))

    #html_list.append(sid)

    return html_list

layout = html.Div( #creating the layout
                    children = create_html_map(glob_vars.data), # the elements of the layout
                    id = "layout_map", # the ID of the layout
                    style = CONTENT_STYLE #style the content of the page
                 )

#filtering the given df for the characteristics in the filter_dict
def filter_content(df: pd.DataFrame, filter_dict:defaultdict):
    """
    df: Dataframe with user content to be filtered
    filter_dict: default dictionary with all characteristics to be filtered for as keys, value to be filtered for as value and default value as none

    returns: filtered dataframe by standards of filter_dict
    """
    #currently only filters for location and occupancy

    #if none then no location name was given the filter, so no filtering
    #print(df, filter_dict
    keys = df.columns.values
    #print("Keys are: ", keys)
    for key in keys:
        if filter_dict[key] == None:
            #print("Es wurde continued")
            continue
        elif key == "location":
            #print("loc is: ", filter_dict[key])
            df = filter_names(df, filter_dict[key])
            #print(df)
        elif type(filter_dict[key]) == str:
            df = filter_for_value(df, key, filter_dict[key])
        elif type(filter_dict[key]) == list:
            #print(filter_dict[key])
            df = filter_for_list(df, key, filter_dict[key])
            #print(df)
        elif type(filter_dict[key]) == int or type(filter_dict[key]) == float:
            df = filter_max_value(df, key, filter_dict[key])

    #print("Am Ende: ", df)
    #filtered dataframe
    return df


#---------------------------------------------------------------------
#Callbacks:


#------


#layout refresh callback and sidebar handling
@callback(
    Output("layout_map", "children"),
    [Input("update_map_div", "n_clicks")],
    prevent_initial_call=True
)
def update_layout(*args):

    return create_html_map(glob_vars.data)



#function to replace the filtered dataframe with the original
#returns layout of page
def reverse_Map():
    #lobal data

    glob_vars.data = get_data(name_of_csv="Characteristics.csv")

    return create_html_map(glob_vars.data)


def reset_global_filter():
    glob_vars.current_filter = defaultdict(lambda: None)



def filter_data():#filter_dict: dict[str:str]):
    #global data

    glob_vars.data = filter_content(glob_vars.data, glob_vars.current_filter)


#function to replace the filtered dataframe with itself, not changing anything
#returns layout of page
def keep_layout_Map():
    reset_data()
    filter_data()
    #global data, temp_data

    return create_html_map(glob_vars.data)


def reset_data(name="Characteristics.csv"):
    glob_vars.data = get_data(name)

#function to replace the current dataframe with the filtered version of the original
#returns layout of page
def filter_buttons_Map(filter_dict):

    global data, temp_data
    temp_data = data.copy(deep=True)

    temp_data = list_page.filter_content(temp_data, filter_dict)

    return create_html_map(temp_data)


#function to update the dataframe according to the data (checking for potentiell changes in the data)
# returns the updated layou of the page
def update(nr_clicks):
    global data, temp_data

    if nr_clicks == None:
        raise PreventUpdate
    data = get_data()
    temp_data = data.copy(deep=True)
    #only for testing
    #temp_data.drop(temp_data.loc[temp_data['location'] == "Heidelberg"].index, inplace = True )

    return create_html_map(temp_data)
