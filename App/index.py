# Import necessary libraries
from dash import html, dcc, ctx
from dash.dependencies import Input, Output, State
import dash
#from components import sidebar
# Connect to main app.py file
from app import app
import dash_bootstrap_components as dbc
# Connect to your app pages
from pages import map_page, list_page
from utility.filter_funktion import *
# Connect the components to the index
from components import navbar, sidebar
#from components import sidebar
import pages.global_vars as glob_vars
from dash.exceptions import PreventUpdate
from utility.data_functions import *
from collections import defaultdict
import fontstyle
import base64
import datetime
import io
from csv import reader

"""
This is the main index file to control the app layout.
Further, it includes callback functions for the different pages of the application.
"""


nav = navbar.get_navbar()  # Create the navbar
sid = sidebar.get_sidebar()
# sid = sidebar.get_sidebar()  # Create the sidebar

app.layout = html.Div([  # Create a Div containing the navbar and the content
    dcc.Location(id='url', refresh=True),  # Track current URL of the page
    nav,  # Add the navbar
    dcc.Interval(
            id='auto_refresh_interval',
            interval=60 * 60 * 1000, #factor meaning left to right: minutes, seconds, miliseconds, current refresh rate every 60 minutes
            n_intervals=0
    ),
    html.Div(id="placeholder_interval_check", style={"display":"none"}),
    html.Div(id="update_list_div", style={"display":"none"}),
    html.Div(id="update_map_div", style={"display":"none"}),
    html.Div(id='page-content', children=[]),  # Add the page content
    sid,  # Add the sidebar
])


@app.callback(  # Create a callback for the index page
    Output('page-content', 'children'),  # Output for the page content
    [Input('url', 'pathname')]  # Input for the current URL of the page
)
def display_page(pathname):
    """
    This function updates the content of the page based on the URL
    :param pathname:    The URL of the new page
    :return:    The new page content
    """
    if pathname == '/map_page':  # If the URL is map_page
        return map_page.layout  # Return the layout of the map page
    if pathname == '/list_page':  # If the URL is list_page
        return list_page.layout  # Return the layout of the list page
    else:  # If the URL is not map_page or list_page
        return map_page.layout  # Return the layout of the map page

"""
#callback to periodically refresh
@app.callback(
    [Output("update_list_div", "n_clicks"),
     Output("update_map_div", "n_clicks"),],
    [Input('url', 'pathname'),
     Input("auto_refresh_interval", 'n_intervals')],
    prevent_initial_call=True
)
def testing_pls(path, a):
    ctxx = dash.callback_context
    triggered_id = ctx.triggered_id


    #parse/refresh urls/occupancy
    if triggered_id == "url":
        #dont update only because view is changed

        return dash.no_update, dash.no_update
    
    #still add url refreshing!!!!!!-----------------------
    if path == "/list_page":
        #update list page layout
        return 1, dash.no_update
    elif path == "/map_page":
        #update map page layout
        return dash.no_update, 1

    
    #no update else
    raise PreventUpdate
"""

def define_chracteristics()->list:
    """
    This functions creates a list with all current characteristics.

    Returns
    -------
    characteristics2:list
        A list of all chracters in the data.
    """

    temp_data = get_data("Characteristics.csv")
    csv_reader = reader(temp_data)
    characteristics2 = []

    counter = 0


    for row in csv_reader:
        if counter < 3:
            counter +=1
            continue
        characteristics2.append(row[0])

    return characteristics2

def define_inputs_add_location(special_ones:list)-> list:
    """
    This function creates a list of all inpus for the callback to add a new location.

    Parameters
    ----------
    special_ones:
        A list of inputs which are final.

    Returns
    -------
    inputs :
        A list of all inputs to add a new location.
    """

    inputs = []

    for one in special_ones:
        inputs.append(one)


    characteristics= define_chracteristics()


    for characs in characteristics:
        inputs.append(Input("modal_add_location_"+ characs, "value"))

    return inputs



def define_outputs_add_loction(special_ones:list)-> list:
    """
    This function creates a list of all outputs for the callback to add a new location.

    Parameters
    ----------
    special_ones:
        A list of outputs which are final.

    Returns
    -------
    outputs :
        A list of all outputs to add a new location.
    """


    outputs = []

    for one in special_ones:
        outputs.append(one)


    characteristics= define_chracteristics()


    for characs in characteristics:
        outputs.append(Output("modal_add_location_"+ characs, "value"))

    return outputs


#callback for adding new locations
#receives button inputs and inputs from the modal input fields
@app.callback(define_outputs_add_loction([Output("placeholder_div_adding", "n_clicks"),
    Output("modal_add_location", "is_open"),
    Output("modal_field_warning" , "style"),
    Output("modal_add_location_url" , "value"),
    Output("modal_add_location_name" , "value")]),
    define_inputs_add_location([Input("modal_add_location_submit_button" , "n_clicks"),Input("open_modal_add_location_button" , "n_clicks"), Input("modal_add_location_cancel_button", "n_clicks"),Input("modal_add_location_url" , "value"),Input("modal_add_location_name", "value")]),
    [State("modal_add_location", "is_open")],
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

    #get characteristics from data
    characteristics = list(glob_vars.data.columns.values)

    #latitude and longitude not given by pop up
    non_changeable = ["lat", "lon"]
    #remvove lat and lon
    for n in non_changeable:
        if n in characteristics:
            characteristics.remove(n)

    #extract state of pop up and characteristics
    modal_state = params[-1]
    characs = params[:-1]

    #check for error
    assert len(characs) == len(characteristics), "Number of characteristic inputs and characteristics in data must be the same"

    triggered_id = ctx.triggered_id

    #if cancel button was pressed return refresh confirmation, invisible style for error warning and list with empty values
    if triggered_id == "modal_add_location_cancel_button" :
        return (1, not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    #if open modal button was pressed
    elif triggered_id == "open_modal_add_location_button" :
        return (dash.no_update, not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    elif triggered_id == "modal_add_location_submit_button" :
        #check if URL and name are given
        #url must be given
        if URL_value == None or URL_value == "":

            return (dash.no_update, modal_state, {"display":"block", "color":"red"}, URL_value) + tuple(characs)

        #location name must be given
        if characs[0] == None or characs[0] == "":

            return (dash.no_update, modal_state, {"display":"block", "color":"red"}, URL_value) + tuple(characs)


        #make dictionary for function
        add_dictionary = {}

        for c, charac in zip(characs, characteristics):
            add_dictionary[charac] = c

        # NOW FUNCTION TO ADD LOCATION TO CSV
        add_location(url=URL_value, dic=add_dictionary)

        return (1, not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    else:
        raise PreventUpdate

@app.callback(
        [Output("update_list_div", "n_clicks"),
        Output("update_map_div", "n_clicks"),
        Output("sideboard_name_filter", "value"),
        Output("sideboard_address_filter", "value"),
        Output("sideboard_occupancy_filter", "value"),
        Output("sideboard_price_filter", "value"),],
        [Input('url', 'pathname'),
        Input("auto_refresh_interval", 'n_intervals'),
        Input("placeholder_div_filter", "n_clicks"),
        Input("placeholder_div_adding", "n_clicks"),
        Input("clear_filter_button", "n_clicks"),
        Input("refresh_page", "n_clicks"),
        Input("sideboard_name_filter", "value"),
        Input("sideboard_address_filter", "value"),
        Input("sideboard_occupancy_filter", "value"),
        Input("sideboard_price_filter", "value"),],
        prevent_initial_call=True
)
def choose_correct_update(*args):
    """
    last x args are input values from sidebar
    first args element is name of page
    order important according to sidebar_characs list

    first output updates list, second one the map
    """
    #print(args)
    triggered_id = ctx.triggered_id
    
    #name of current page, important to decide which page to update
    page_name = args[0]

    #manually write characteristics of quick filters
    sidebar_characs = ["location", "address", "occupancy", "price"]

    #num is amount of sidebar elements that are quickfilter, i.e. the last num inputs of this callback
    num = 4
    sidebar_values = args[-num:]
    # index of callback input for


    if triggered_id == "clear_filter_button":
        #reset data and filter dictionary
        glob_vars.reset_data()
        glob_vars.reset_global_filter()
        #return refreshed layout with new data and empty value list for inputs
        sidebar_values = [None for x in sidebar_values]

    elif triggered_id == "sideboard_price_filter" or triggered_id == "sideboard_occupancy_filter" or triggered_id == "sideboard_address_filter" or triggered_id == "sideboard_name_filter":
        #sidebar filter triggered
        print("sidebar triggered")
        #first reset data
        glob_vars.reset_data()
        #check for error
        assert len(sidebar_characs) == len(sidebar_values), "Number of filter inputs in sidebar and hardcoded characteristics must be equal"

        #add filter values to dictionary
        for s, val in zip(sidebar_characs, sidebar_values):

            if val == "":
                val = None

            glob_vars.current_filter[s] = val

        #filter with new filter dictionary
        
        filter_data()


    #if triggered_id == "placeholder_div_filter" or triggered_id == "placeholder_div_adding" or triggered_id == "url" or triggered_id == "refresh_page":
    if page_name == "/list_page":
        return (1, dash.no_update) + tuple(sidebar_values)
    elif page_name == "/map_page":
        return (dash.no_update, 1) + tuple(sidebar_values)
    else: #error or page not accounted for
        #print("Hoffentlich Startcallback")
        raise PreventUpdate

        #raise ValueError("A Page is not accounted for in the update method")

def define_inputs_advanced_filter(special_ones:list)-> list:
    """
    This function creates a list of all inpus for the callback to conduct the advanced filter.

    Parameters
    ----------
    special_ones:
        A list of inputs which are final.

    Returns
    -------
    inputs :
        A list of all inputs to conduct the advanced filter.
    """


    inputs = []

    for one in special_ones:
        inputs.append(one)

    characteristics= define_chracteristics()

    for characs in characteristics:
        inputs.append(Input("modal_advanced_filter_"+ characs, "value"))

    return inputs


def define_outputs_advanced_filter(special_ones:list)->list:
    """
    This function creates a list of all outputs for the callback to to conduct the advanced filter.

    Parameters
    ----------
    special_ones:
        A list of outputs which are final.

    Returns
    -------
    outputs :
        A list of all outputs to to conduct the advanced filter.
    """


    outputs = []

    for one in special_ones:
        outputs.append(one)


    characteristics= define_chracteristics()


    for characs in characteristics:
        outputs.append(Output("modal_advanced_filter_"+ characs, "value"))

    return outputs


#callback to handle everything about the advanced filter
#gets input from the button on the sidebar, the buttons in the modal footer and the input elements in the modal
@app.callback(
    define_outputs_advanced_filter([Output("placeholder_div_filter" , "n_clicks"),
                                    Output("modal_filter_window" , "is_open"),
                                    Output("modal_advanced_filter_occupancy" , "value"),
                                    Output("modal_advanced_filter_name" , "value"),]),
    define_inputs_advanced_filter([Input("advanced_filter_button" , "n_clicks"),
                                   Input("modal_filter_submit_button" , "n_clicks"),
                                   Input("modal_filter_cancel_button" , "n_clicks"),
                                   #Input("modal_advanced_filter_number_parking_lots" , "marks"),
                                   Input("modal_advanced_filter_occupancy" , "value"),
                                   #Input("modal_advanced_filter_occupancy" , "marks"),
                                   Input("modal_advanced_filter_name", "value")]),
    [State("modal_filter_window" , "is_open")],
    prevent_initial_call=True
)
def advanced_filter_handling(_n1, _n2, _n3, occupancy_vals, *params):
    """
    - variables with _ are n_clicks and not important
    - params is list with characteristics and modal state at the end

    - order of parameters(Input and Output) is important, especially in combination with filter dict handling
    """
    print(params, glob_vars.current_filter)
    #get origin of callback
    triggered_id = ctx.triggered_id

    #list of characteristics according to data
    characteristics = list(glob_vars.data.columns.values)
    #latitude and longitude not given by pop up
    non_changeable = ["lat", "lon"]
    #remove lat and lon from characteristics
    for n in non_changeable:
        if n in characteristics:
            characteristics.remove(n)

    #extract modal state and characteristics
    modal_state = params[-1]
    characs = params[:-1]

    #check for possible error
    assert len(characs) == len(characteristics), "Number of characteristic inputs and characteristics in data must be the same"

    #create list in case of filter reset
    empty_ret_list = [None]

    for c in characteristics:
        empty_ret_list.append(None)

    #if cancel filter of modal, renew all inputs in advanced filter
    if triggered_id == "modal_filter_cancel_button" :
        return (0, not modal_state,) + tuple(empty_ret_list)
    #if apply button of modal, apply filters and keep values in input fields
    elif triggered_id == "modal_filter_submit_button" :
        #rest data to filter on all data available
        glob_vars.reset_data()
        #insert occupancy values to filter dict
        #occupancy not in characteristics csv therefore seperate assignment
        glob_vars.current_filter["occupancy"] = occupancy_vals

        #if characteristic is None, remove from filter dict(so no residual values from previous filters are used)
        for c, chara in zip(characs, characteristics):
            if c == None:
                glob_vars.current_filter.pop(chara, None)
                continue
            #assign values to filter dictionary
            glob_vars.current_filter[chara] = c

        #print(glob_vars.current_filter)
        #filter data with filter dictionary
        filter_data()
        #return confirmation to filter placeholder, modal state and input values
        return (1, not modal_state, occupancy_vals) + tuple(characs)
    #if button to open modal was pressed
    elif triggered_id == "advanced_filter_button" :
        characs = list(characs)

        #assign existing characteristics from filter dictionary to the input fields to "keep" existing filters
        for i in range(len(characteristics)):
            key = characteristics[i]

            characs[i] = glob_vars.current_filter[key]

        #return no confirmation, open modal and existing input values
        return (dash.no_update, not modal_state, glob_vars.current_filter["occupancy"]) + tuple(characs)
    else:
        raise PreventUpdate


@app.callback([Output("modal_import_file", "is_open"),
           Output("modal_uploaded_csv", "value"),
           Output("modal_uploaded_json", "value"),
           Output("modal_import_warning", "children")],
          [Input("upload_import_files", "contents"),
           Input("modal_uploaded_csv", "value"),
           Input("modal_uploaded_json", "value"),
           Input("import_button", "n_clicks"),
           Input("modal_import_file_upload_button", "n_clicks"),
           Input("modal_import_file_cancel_button", "n_clicks"),],
          [State('upload_import_files', 'filename'),
           State("modal_import_file", "is_open")],
          prevent_initial_call=True)
def import_data_files(contents, csv_val, json_val, _n, _n2, _n3, filenames, modal_state):
    triggered_id = ctx.triggered_id
    #print(triggered_id)
    #print(contents, filenames)

    if triggered_id == "import_button" or triggered_id == "modal_import_file_cancel_button":
        glob_vars.temp_csv = None
        glob_vars.temp_json = None
        return not modal_state, None, None, ""
    elif triggered_id == "upload_import_files":
        #if too many files were passed, either simultaneously or both places for the files are already occupied
        if len(contents) > 2:# or (glob_vars.temp_csv != None and glob_vars.temp_json != None):
            glob_vars.temp_csv = None
            glob_vars.temp_json = None
            return modal_state, csv_val, json_val, "Too many files uploaded!"


        #check if correct file types were uploaded
        admissible_types = [".json", ".csv"]

        for f in filenames:
            valid = False
            for a in admissible_types:
                if a in f:
                    valid = True
            
            if not valid:
                return modal_state, csv_val, json_val, "Wrong file type uploaded!"

        #iterate through uploaded files
        for c, f in zip(contents, filenames):
            try:
                #read content from given file
                df = parse_contents(c, f)
            except: #exception at parse contents means wrong file type? maybe somewhere else?
                raise PreventUpdate
            #if json file then save json file and update check input
            if ".json" in f:
                glob_vars.temp_json = df
                json_val = f
            #other option is csv
            elif ".csv" in f:
                glob_vars.temp_csv = df
                csv_val = f

        return modal_state, csv_val, json_val, ""        

    elif triggered_id == "modal_import_file_upload_button":
        #if one of the necessary files hasnt beent uploaded dont upload
        if glob_vars.temp_csv is None or glob_vars.temp_json is None:
            return modal_state, csv_val, json_val, "Not all necessary files uploaded!"

        #check validity of both files

        if not check_csv_validity(glob_vars.temp_csv):
            glob_vars.temp_csv = None
            return modal_state, None, json_val, "CSV File does not meet conventions!"
        
        #csv data is okay now
        location_names = list(glob_vars.temp_csv["location"])

        if not check_json_validity(glob_vars.temp_json, location_names):
            glob_vars.temp_json = None
            return modal_state, csv_val, None, "JSON File does not meet conventions!"

        #add both files to existing files

        #obtain which locations are new
        new_locations = []
        old_locatiions = list(glob_vars.data["location"])

        for l in location_names:
            if l not in old_locatiions:
                new_locations.append(l)

        #add new locations to characteristics csv
        #get all rows with location names of the new locations
        df_to_append = glob_vars.temp_csv.loc[glob_vars.temp_csv['location'].isin(new_locations)]
        #append new rows to old data
        temp_data = pd.concat([glob_vars.data, df_to_append])
        temp_data.reset_index(drop = True, inplace=True)

        #save combined df to csv
        path = get_path_to_csv(name_of_csv="Characteristics.csv")
        temp_data.to_csv(path, index=False)
        
        #add new locations to json
        #read current json file
        path_to_urls = get_path_to_csv("Urls.json")
        with open(path_to_urls) as json_file:
            json_decoded = json.load(json_file)

        #transfer links of new locations
        for l in new_locations:
            json_decoded[l] = glob_vars.temp_json[l]
        #save json file
        with open(path_to_urls, 'w') as json_file:
            json.dump(json_decoded, json_file)

        #add new locations to occupancy
        occupancy_df = get_data(name_of_csv="Occupancy.csv")
        
        for l in new_locations:
            occupancy_df[l] = None

        #save Occupancy
        o_path = get_path_to_csv(name_of_csv="Occupancy.csv")
        occupancy_df.to_csv(o_path, index=False)

        #renew global data
        glob_vars.reset_data()
        filter_data()

        #TO-DO:
        #update Occupancy for every location

        return not modal_state, None, None, ""
    else:
        
        raise PreventUpdate
    

def check_csv_validity(temp_df: pd.DataFrame) -> bool:
    #things to check when given a dataframe:
    #- check if columns align with our columns
    #- check if data is rectangular - is dataframe always rectangular?
    #- check if every row has a location name and no duplicate locations exist

    #columns do not match
    for tv, v in zip(list(temp_df.columns.values), list(glob_vars.data.columns.values)):
        if tv != v:
            return False
    
    #check that location name exists for every row
    location_names = list(temp_df["location"])
    #check for duplicates
    temp_set = set(location_names)
    if len(temp_set) != len(location_names):
        return False

    assert len(location_names) == len(temp_df)

    #check for None values
    for l in location_names:
        if l == None:
            return False


    return True

def check_json_validity(json_object:dict[str:str], csv_locations: list[str]) -> bool:
    """
    Checks if the given dictionary is according to the acceptance criteria

    json_object: dictionary with key:value pairs as location:api-link
    csv_locations: location names from the simultaniouisly uploaded csv file 
    
    returns: whether the dictionary is valid or not
    """
    
    #validity of json file is guaranteed by:
    #- every location from the csv file is represenmted in the json file -> meaning every location has a link
    #- maybe also check that links are working? -> time expensive but okay when importing
    print(json_object, csv_locations)

    for l in csv_locations:
        if l not in json_object:
            return False

    return True

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if '.csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif '.json' in filename:
            # Assume that the user uploaded an excel file
            df = json.loads(decoded)
        else:
            df = None

        return df
    
    except Exception as e:
        raise e


# Run the app on localhost:8050
if __name__ == '__main__':
    update_occupancies()
    app.run_server(debug=True)
