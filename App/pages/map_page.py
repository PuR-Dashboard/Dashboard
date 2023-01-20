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
from utility.util_functions import *
from components.sidebar import get_sidebar
from utility.data_functions import add_location
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

seitentag = "_map"

#html_list = []

#global data, temp_data

global sid
sid = get_sidebar(seitentag)

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
                    srcDoc=open(os.path.join(os.path.dirname(__file__), '../../P&R_Karte.html'), "r").read(),# Set the source of the Iframe element to be the previously created map
                     #width="87%", height="800", # set the width and the height of the IFrame Element
                     style = CONTENT_STYLE

                     ))

    html_list.append(sid)

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
    print("Keys are: ", keys)
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

#open adding module, add location etc
@callback(
    [Output("placeholder_div_adding" + seitentag, "n_clicks"),
    Output("modal_add_location" + seitentag, "is_open"),
    Output("modal_field_warning" + seitentag, "style"),
    Output("modal_add_location_url" + seitentag, "value"),
    Output("modal_add_location_name" + seitentag, "value"),
    Output("modal_add_location_address" + seitentag, "value"),
    Output("modal_add_location_administration" + seitentag, "value"),
    Output("modal_add_location_kind" + seitentag, "value"),
    Output("modal_add_location_parking_lots" + seitentag, "value"),
    Output("modal_add_location_price" + seitentag, "value"),
    Output("modal_add_location_connection" + seitentag, "value"),
    Output("modal_add_location_num_connections" + seitentag, "value"),
    Output("modal_add_location_infrastructure" + seitentag, "value"),],
    [Input("modal_add_location_submit_button" + seitentag, "n_clicks"),
    Input("open_modal_add_location_button" + seitentag, "n_clicks"),
    Input("modal_add_location_cancel_button" + seitentag, "n_clicks"),
    Input("modal_add_location_url" + seitentag, "value"),
    Input("modal_add_location_name" + seitentag, "value"),
    Input("modal_add_location_address" + seitentag, "value"),
    Input("modal_add_location_administration" + seitentag, "value"),
    Input("modal_add_location_kind" + seitentag, "value"),
    Input("modal_add_location_parking_lots" + seitentag, "value"),
    Input("modal_add_location_price" + seitentag, "value"),
    Input("modal_add_location_connection" + seitentag, "value"),
    Input("modal_add_location_num_connections" + seitentag, "value"),
    Input("modal_add_location_infrastructure" + seitentag, "value"),],
    [State("modal_add_location" + seitentag, "is_open")],
    prevent_initial_call=True,
    suppress_callback_exceptions=True
)
def add_new_location(_1, _2, _3, URL_value, *params):
    """
    structure of parameters:
    - variables with underscore(_1,...) are n_clicks of buttons and not relevant
    - URL_value is the given url
    - params is every dash component that is also a characteristic and the pop up open state at the end
    -> !!! order or parameters is important. Order is matched 1 to 1 to list of characteristics for adding new locations.
            if new characteristics are added, then the order of the parameters must be changed accordingly!!!
    Also order of putputs is depending on order of input
    """
    #global data
    #print(type(connection))
    #print(URL_value, params)
    characteristics = list(glob_vars.data.columns.values)

    #latitude and longitude not given by pop up
    non_changeable = ["lat", "lon"]

    for n in non_changeable:
        if n in characteristics:
            characteristics.remove(n)


    #state of pop up
    modal_state = params[-1]

    #characteristics
    characs = params[:-1]
    #there has to be equally as much input as there are characteristics
    assert len(characs) == len(characteristics)

    triggered_id = ctx.triggered_id

    if triggered_id == "modal_add_location_cancel_button" + seitentag:
        return (1, not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    elif triggered_id == "open_modal_add_location_button" + seitentag:
        return (dash.no_update, not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    elif triggered_id == "modal_add_location_submit_button" + seitentag:
        #check if URL and name are given
        error_made = [False, False]
        #url must be given
        if URL_value == None or URL_value == "":

            return (dash.no_update, modal_state, {"display":"block", "color":"red"}, URL_value) + tuple(characs)

        #location name must be given
        if characs[0] == None or characs[0] == "":

            return (dash.no_update, modal_state, {"display":"block", "color":"red"}, URL_value) + tuple(characs)


        #make dictionary for function
        add_dictionary = {}
        #print("worked anyways lol")
        for c, charac in zip(characs, characteristics):
            add_dictionary[charac] = c

        # NOW FUNCTION TO ADD LOCATION TO CSV
        add_location(url=URL_value, dic=add_dictionary)

        return (1, not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    else:
        raise PreventUpdate




#modal filter handling
@callback(
    [Output("placeholder_div_filter" + seitentag, "n_clicks"),
    Output("modal_filter_window" + seitentag, "is_open"),
    Output("modal_advanced_filter_occupancy" + seitentag, "value"),
    Output("modal_advanced_filter_name" + seitentag, "value"),
    Output("modal_advanced_filter_address" + seitentag, "value"),
    Output("modal_advanced_filter_administration" + seitentag, "value"),
    Output("modal_advanced_filter_kind" + seitentag, "value"),
    Output("modal_advanced_filter_parking_lots" + seitentag, "value"),
    Output("modal_advanced_filter_price" + seitentag, "value"),
    Output("modal_advanced_filter_connection" + seitentag, "value"),
    Output("modal_advanced_filter_num_connections" + seitentag, "value"),
    Output("modal_advanced_filter_infrastructure" + seitentag, "value"),],
    [Input("advanced_filter_button" + seitentag, "n_clicks"),
    Input("modal_filter_submit_button" + seitentag, "n_clicks"),
    Input("modal_filter_cancel_button" + seitentag, "n_clicks"),
    Input("modal_advanced_filter_parking_lots" + seitentag, "marks"),
    Input("modal_advanced_filter_occupancy" + seitentag, "value"),
    Input("modal_advanced_filter_occupancy" + seitentag, "marks"),
    Input("modal_advanced_filter_name" + seitentag, "value"),
    Input("modal_advanced_filter_address" + seitentag, "value"),
    Input("modal_advanced_filter_administration" + seitentag, "value"),
    Input("modal_advanced_filter_kind" + seitentag, "value"),
    Input("modal_advanced_filter_parking_lots" + seitentag, "value"),
    Input("modal_advanced_filter_price" + seitentag, "value"),
    Input("modal_advanced_filter_connection" + seitentag, "value"),
    Input("modal_advanced_filter_num_connections" + seitentag, "value"),
    Input("modal_advanced_filter_infrastructure" + seitentag, "value"),],
    [State("modal_filter_window" + seitentag, "is_open")],
    prevent_initial_call=True
)
def advanced_filter_handling(_n1, _n2, _n3, parking_lot_marks, occupancy_vals, occupancy_marks, *params):
    """
    - variables with _ are n_clicks and not important
    - params is list with characteristics and modal state at the end

    - order of parameters(Input and Output) is important, especially in combination with filter dict handling
    """

    #global data

    triggered_id = ctx.triggered_id
    #print(triggered_id)
    characteristics = list(glob_vars.data.columns.values)
    #latitude and longitude not given by pop up
    non_changeable = ["lat", "lon"]

    for n in non_changeable:
        if n in characteristics:
            characteristics.remove(n)

    #print(characteristics)
    #modal state
    modal_state = params[-1]

    characs = params[:-1]
    #type_list = [(type(x), x) for x in characs]
    #print(type_list)
    assert len(characs) == len(characteristics)

    #make lists with ground value types for characteristics
    #typical value none
    #charac_with_none = ["location", "road_network_connection", "administration", "surrounding_infrastructure", "kind", "price", "public_transport"]
    #two_value_slider = ["number_parking_lots"]


    empty_ret_list = [None]

    for c in characteristics:
        empty_ret_list.append(None)



    if triggered_id == "modal_filter_cancel_button" + seitentag:
        return (0, not modal_state,) + tuple(empty_ret_list)
    elif triggered_id == "modal_filter_submit_button" + seitentag:
        reset_data()
        #filter_dict = {}

        glob_vars.current_filter["occupancy"] = occupancy_vals

        for c, chara in zip(characs, characteristics):
            if c == None:
                glob_vars.current_filter.pop(chara, None)
                continue
            """if chara == "number_parking_lots":
                if c[0] == 1 and c[1] == 6:
                    #glob_vars.current_filter.pop(chara, None)
                    c = None
                else:
                    c = make_parking_lot_list(c[0], c[1], parking_lot_marks)"""

            glob_vars.current_filter[chara] = c


        #print("Before_filtering: ", glob_vars.current_filter)
        #filter_dict = create_filter_dict(*characs)
        filter_data()#glob_vars.current_filter)
        return (1, not modal_state, occupancy_vals) + tuple(characs)
    elif triggered_id == "advanced_filter_button" + seitentag:
        characs = list(characs)
        #print("characteristics ", characteristics)
        for i in range(len(characteristics)):
            key = characteristics[i]

            characs[i] = glob_vars.current_filter[key]

        #print("charac print: ", characs, modal_state)
        return (dash.no_update, not modal_state, glob_vars.current_filter["occupancy"]) + tuple(characs)
    else:
        raise PreventUpdate

#------


#layout refresh callback and sidebar handling


@callback(
    [Output("layout_map", "children"),
    Output("sideboard_name_filter" + seitentag, "value"),
    Output("sideboard_address_filter" + seitentag, "value"),
    Output("sideboard_occupancy_filter" + seitentag, "value"),
    Output("sideboard_price_filter" + seitentag, "value"),],
    [Input("placeholder_div_filter" + seitentag, "n_clicks"),
    Input("placeholder_div_adding" + seitentag, "n_clicks"),
    Input("clear_filter_button" + seitentag, "n_clicks"),
    Input("refresh_page", "n_clicks"),
    Input("sideboard_name_filter" + seitentag, "value"),
    Input("sideboard_address_filter" + seitentag, "value"),
    Input("sideboard_occupancy_filter" + seitentag, "value"),
    Input("sideboard_price_filter" + seitentag, "value"),],
    prevent_initial_call=True
)
def update_layout(*args):

    triggered_id = ctx.triggered_id
    #print(triggered_id)

    #manually write characteristics of quick filters
    sidebar_characs = ["location", "address", "occupancy", "price"]

    #num is amount of sidebar elements that are quickfilter, i.e. the last num inputs of this callback
    num = 4
    sidebar_values = args[-num:]
    print("VALS: ", sidebar_values)
    # index of callback input for
    marks = args[-4]

    if triggered_id == "clear_filter_button" + seitentag:
        reset_data()
        reset_global_filter()
        new_lay = reverse_Map()

        return (new_lay,) + tuple(sidebar_values)
    #elif triggered_id == "sideboard_name_filter" + seitentag or triggered_id == "sideboard_occupancy_filter" + seitentag:
    elif triggered_id == "refresh_page" or triggered_id == "placeholder_div_filter" + seitentag: #or triggered_id == "placeholder_div_adding" + seitentag:
        reset_data()
        filter_data()
        return (create_html_map(glob_vars.data),) + tuple(sidebar_values)

    else:
        print()
        reset_data()
        #sidebar_characs = ["location", "address", "occupancy", "price"]
        assert len(sidebar_characs) == len(sidebar_values)

        for s, val in zip(sidebar_characs, sidebar_values):

            if val == None or val == "":
                glob_vars.current_filter[s] = None
                continue
            else:
                glob_vars.current_filter[s] = val
        #filter_dict = create_filter_dict(administration=args[-2], parking_lots_range=args[-1])
        #print(glob_vars.current_filter)
        filter_data()#glob_vars.current_filter)

        #print(glob_vars.data)

        return (keep_layout_Map(),) + tuple(sidebar_values)



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
