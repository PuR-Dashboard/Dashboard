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
from components.sidebar import get_sidebar
from utility.data_functions import *
from utility.filter_function import *
import pages.global_vars as glob_vars
from collections import defaultdict
import folium
from csv import reader


 #style the content of map_page so that it aligns with the sidebar
CONTENT_STYLE = {
    "position": "fixed",
    "width": "calc(100vw - 250px)",
    "height": "calc(100vh - 50px)",
    "flex-grow": "1",
    "seamless":"True"

}





def define_chracteristics()-> list:
    """
    This functions creates a list with the names of all current characteristics.

    Returns
    -------
    characteristics2:list
        A list of all chracters in the data.
    """

    temp_data = get_data("Characteristics.csv") # the current data of the locations
    csv_reader = reader(temp_data) # a reader to work with the csv filter

    characteristics2 = []

    counter = 0

    #iterating through all the data and save the names of the current characteristics
    for row in csv_reader:
        if counter < 3: # the first three characteristics(name, location(lat,lon)) are unimportant
            counter +=1
            continue
        characteristics2.append(row[0]) #

    return characteristics2



def create_html_map(data:pd.DataFrame)-> list:
    """
    This function creates a map and adds it to the map_page.

    Parameters
    ----------
    data: Panda DataFrame
        The data which should be visualized.

    Returns
    -------
    html_list:
        Represents the componentents which should be visualized in the map_page.
    """
    global sid

    html_list = []

    try:
        map_functions.create_map(data) # create the map
        html_list.append(  # Append the map tp the map_page
                        html.Iframe( #Create an Iframe element to get an interactive map
                        id="page-layout", # Set the id of the Iframe element
                        srcDoc=open(os.path.join(os.path.dirname(__file__), '../P&R_Karte.html'), "r").read(),# Set the source of the Iframe element to be the previously created map
                        #width="87%", height="800", # set the width and the height of the IFrame Element
                        style = CONTENT_STYLE

                        ))
    except:
        glob_vars.curr_error = Exception("Error while creating the map! Look in map_functions.py or check P&R_Karte.html")


    return html_list


 #creating the layout of the map_page
layout = html.Div(
                    children = create_html_map(glob_vars.data), # the elements of the layout
                    id = "layout_map", # the ID of the layout
                    style = CONTENT_STYLE #style the content of the page
                 )



def reverse_Map()->list:
    """
    This function reverses the map (all filters are removed).

    Returns
    -------
    html_map :
        A list of all components of the map page with the reversed data.
    """

    try:
        glob_vars.data = get_data(name_of_csv="Characteristics.csv") # reversing the global variable data based on the data in the characteristics csv
    except Exception as e:
        glob_vars.curr_error = e
        return []

    #redefining and creating the map page based on the reversed data
    return create_html_map(glob_vars.data)


def keep_layout_Map()-> list:
    """
    This function replaces the current dataframe with itself.
    Nothing should change.

    Returns
    -------
    html_map :
        A list of all components/layout of the map page.
    """
    glob_vars.reset_data() # resting the data
    try:
        filter_data() #filters the data based on the current filter
    except:
        glob_vars.curr_error = Exception("Error while filtering. Check filter_functiions.py.")

    #redefining and creating the map page based on the reseted data
    return create_html_map(glob_vars.data)


def filter_buttons_Map(filter_dict:pd.DataFrame)-> list:
    """
    This function replaces the current dataframe with the filtered version of the original.

    Parameters
    -------
    filter_dict :
        The filtered version of the dictionary.

    Returns
    -------
    layout:
        The layout with the filtered data.
    """

    global data, temp_data
    temp_data = data.copy(deep=True)
    try:
        temp_data = filter_content(temp_data, filter_dict) # filtering the data based on the given filter aspects
    except Exception as e:
        glob_vars.curr_error = e 

    #creating the map page based on the filtered data
    return create_html_map(temp_data)


def update(nr_clicks:int)-> list:
    """
    This function updates the dataframe according to the data (checking for potentiell changes in the data)

    Parameters
    -------
    nr_clicks:
        Number of clicks.

    Returns
    -------
    layout:
        The updated layout of the page.
    """
    global data, temp_data

    if nr_clicks == None: #the map page should only be updated if a button was clicked which should lead to updating the page
        raise PreventUpdate


    data = get_data() # getting the stored data
    temp_data = data.copy(deep=True)

    #creating the map page based on the data
    return create_html_map(temp_data)



#---------------------------------------------------------------------
#Callback functions
@callback(
    Output("show_my_location", "children"),
    Input("my_location", "n_clicks"),
    prevent_initial_call=True
)

def my_location(m):
    html.Div(
    folium.plugins.LocateControl(
        position = 'topright',returnToPrevBounds = True,
        width = "1000%",
        strings={"title":"Show me where I am"},
        icon = "fa-solid fa-location-dot fa-2x text-success",
        setView = False).add_to(m), id="show_my_location")



#layout refresh callback and sidebar handling
@callback(
    Output("layout_map", "children"),
    [Input("update_map_div", "n_clicks"),
    Input("refresh_page","n_clicks")],
    prevent_initial_call=True
)
def update_layout(*args):
    """
    This function updates the layout of the map page by confirmation of other components like the refresh button.

    Inputs
    ----------
    update_map_div:
        A placeholder as an integer value to indicate that the map_page should be refreshed(can be from different sources)
    refresh_page:
        Number of clicks on the refresh button to refresh/update the page.

    Outputs
    -------
    layout_map:
        A list of all components which will represent the new layout of page.
    """

    triggered_id = ctx.triggered_id # the id of the triggered input

    if triggered_id == "refresh_page": # if the function was triggered by the component "refresh_page" the data should be reseted
        glob_vars.reset_data()
        create_html_map(glob_vars.data)

    # the page should be recreated any way
    return create_html_map(glob_vars.data)
