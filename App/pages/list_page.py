import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State, MATCH, ALL
import numpy as np
from dash.exceptions import PreventUpdate
from utility.util_functions import *
from utility.filter_funktion import filter_names, filter_for_value, filter_for_index
from components.sidebar import get_sidebar, make_manual_tab, make_url_tab

#global so the filter functions can access the date
global data, temp_data


DEL_BUTTON_STYLE = {  # Define the style of the buttons
    #"width": "8rem",  # Set the width of the buttons to 8rem
    #"height": "2rem",  # Set the height of the buttons to 2rem
    "padding": "2rem 1rem",  # Add some padding to the buttons
    "marginRight": "0%",  # Align the text in the buttons to the right
}
FA_icon_trash= html.I(className="fa fa-trash fa-lg")
FA_icon_pen= html.I(className="fa fa-pencil fa-lg")

ARR_BUTTON_STYLE = { #Define the style of the arrow button
    "color": "black", #set the arrow itself is black
    "background-color":"transparent", #set the background color to transparent
    "border": "transparent" #set the border color to transparent
}
FA_icon_Arrow = html.I(className="fa fa-chevron-down fa-lg") #arrow icon for the arrow button

CONTENT_STYLE = { #style the content of list_page so that it aligns with the sidebar
    "margin-right": "18%", #set the distance to the right margin where the sidebar goes
    "padding": "2rem 1rem"
}
global sid
seitentag = "_list"

sid = get_sidebar(seitentag)


#baseline truth of the users data
data = get_data()

#editable copy for filtering content
temp_data = data.copy(deep=True)




#filtering the given df for the characteristics in the filter_dict
def filter_content(df: pd.DataFrame, filter_dict: dict[str:str]):
    """
    df: Dataframe with user content to be filtered
    filter_dict: dictionary with all characteristics to be filtered for as keys, and either None or the given values as values

    returns: filtered dataframe by standards of filter_dict
    """
    #currently only filters for location and occupancy

    #if none then no location name was given the filter, so no filtering
    if filter_dict["location"] != None:
        df = filter_names(df, filter_dict["location"])
            
    #if none then no occupancy was given the filter, so no filtering
    if filter_dict["occupancy_traffic_light"] != None:
        df = filter_for_value(df, "occupancy_traffic_light", filter_dict["occupancy_traffic_light"])

    #filtered dataframe
    return df


#function to create a dictionary that can be passed to the filter_content() def
def create_filter_dict(text:str, radio:str):
    """
    text: location name
    radio: occupancy traffic light

    returns: dictionary of characteristics and values
    """
    #currently only filters for location and occupancy

    #init dict
    dic = {}

    #add location to dictionary
    if text != "":
        dic["location"] = text
    else:
        dic["location"] = None
    
    #add occupancy to dictionary
    if radio != "None":
        dic["occupancy_traffic_light"] = radio
    else:
        dic["occupancy_traffic_light"] = None


    return dic


#function to create the content of the tables(the content of the collapsibles)
#will be switched out by table through vuetify library and is not documented further -> soon to be DEPRECATED
def create_content(df: pd.DataFrame):
    cols = df.columns
    #print(cols)
    content = []
    names = []

    for i in range(len(df)):
        row = df.iloc[[i]]

        names.append(row["location"].values[0])

        inhalt = []
        for c in cols:
            mini = str(c) + ": " + str(row[c].values[0])
            inhalt.append(mini)
            inhalt.append(html.Br())

        content.append(inhalt)

    return names, content

#table for characteristics 

table = dbc.Table.from_dataframe(
    data, striped=True, bordered=True, hover=True, index=True
)

#function to dynamically create the dash components of the new layout, will always be used after filtering or refreshing
#----!!! Names and content is at the moment created through the create_content() def, will need new creation function after create_content() is DEPRECATED
def create_layout(names:list[str], content:list[str]):
    """
    names: list of headlines for the list of locations. typically the name of the location
    content: list of content to be given to the collapsibles

    returns: list of python dash and dash.html elements, will be the new layout
    """
    #currently content is list of strings, datatype will vary in the future
    global sid
    #init list of components
    html_list = []

    #iterate through names(names and content must have the same length)
    for i in range(len(names)):
        #append header of location
        html_list.append(dbc.CardHeader([dbc.Button(
                    names[i],
                    color="outline",
                    id={"type":"header", "index":i},
                    value=i
                ), dbc.Button([FA_icon_trash, ""], id={"type":"button_control", "index":i}, className = "pull-right",style = ARR_BUTTON_STYLE),
                   dbc.Button([FA_icon_pen, ""], id={"type":"pen_button", "index" :i}, className = "pull-right" ,style = ARR_BUTTON_STYLE),
                   dbc.Button([FA_icon_Arrow, ""], id={"type":"arrow_button", "index" :i}, className = "pull-right" ,style = ARR_BUTTON_STYLE)
                   ]))
                
                #append collapsible content
        html_list.append(dbc.Collapse(
            dbc.CardBody(table),
            #dbc.CardBody(content[i]),
            #html.Iframe(create_table()),
            id={"type":"content", "index":i}, 
            is_open=False
        ))

    #in case no name sare given(normally means filtering was unsuccessful)
    if len(names) == 0:
        html_list.append(html.H3("No results found!"))
        html_list.append(html.Hr())

    html_list.append(sid)

    return html_list

#create headers and content
names, content = create_content(data)
#create new layout
html_list_for_layout = create_layout(names, content)

layout = html.Div(children=html_list_for_layout, id="list_layout", style = CONTENT_STYLE)



#function to collapse and expand the list items
#takes all dash objects with id type content and header, and then outputs the result to the content type with matching id index
@callback(
    Output({"type": "content", "index": MATCH}, "is_open"),
    [Input({"type": "arrow_button","index": MATCH}, "n_clicks")],
    [State({"type": "content", "index": MATCH}, "is_open")],
)
def toggle_collapses(_butts, stats):
    ctxx = dash.callback_context
        
    if not ctxx.triggered:
        raise PreventUpdate
    else:
        #return opposite state of triggered button for either collapse or expand
        return not stats

#dunno if test or not lol
"""@callback(
    Output("test_side", "value"),
    [Input({"type": "button_control", "index": ALL}, "n_clicks")],
    prevent_initial_call=True,
)
def remove_location(_n):
    triggered_id = ctx.triggered_id

    return triggered_id["index"]"""


#---------testing------------

#modal filter handling
@callback(
    [Output("modal_window" + seitentag, "is_open"),
    Output("modal_name_filter" + seitentag, "value"),
    Output("modal_occupancy_filter" + seitentag, "value"),],
    [Input("advanced_filter_button" + seitentag, "n_clicks"),
    Input("modal_submit_button" + seitentag, "n_clicks"),
    Input("modal_cancel_button" + seitentag, "n_clicks"),
    Input("modal_name_filter" + seitentag, "value"),
    Input("modal_occupancy_filter" + seitentag, "value"),],
    [State("modal_window" + seitentag, "is_open")],
    prevent_initial_call=True
)
def advanced_filter_handling(_n1, _n2, _n3, modal_name_filter, modal_occupancy_filter, modal_open_state):
    global data

    triggered_id = ctx.triggered_id

    
    if triggered_id == "modal_cancel_button" + seitentag:
        return not modal_open_state, "", "None"
    elif triggered_id == "modal_submit_button" + seitentag:
        filter_dict = create_filter_dict(modal_name_filter, modal_occupancy_filter)
        filter_data(filter_dict)
        return not modal_open_state, modal_name_filter, modal_occupancy_filter
    elif triggered_id == "advanced_filter_button" + seitentag:
        return not modal_open_state, modal_name_filter, modal_occupancy_filter
    else:
        raise PreventUpdate

#------
#modal add handling

#switch add modal tabs
@callback(
    [Output("tab_add_url" + seitentag, "style"), Output("tab_add_manual" + seitentag, "style")],
    [Input("tabs_add_location" + seitentag, "active_tab")],
    prevent_initial_call=False
)
def switch_tabs(val):
    on = {'display': 'block'}
    off = {'display': 'none'}
    if val is not None:
        if val == "tab_add_manual":
            return off, on
        elif val == "tab_add_url":
            return on, off
    raise PreventUpdate



#open adding module, add location etc
@callback(
    Output("modal_add_location" + seitentag, "is_open"),
    [Input("modal_add_location_submit_button" + seitentag, "n_clicks"),
    Input("open_modal_add_location_button" + seitentag, "n_clicks"),
    Input("modal_add_location_cancel_button" + seitentag, "n_clicks"),
    Input("modal_add_location_url" + seitentag, "value"),
    Input("modal_add_location_manual_occupancy" + seitentag, "value"),
    Input("tabs_add_location" + seitentag, "active_tab"),],
    [State("modal_add_location" + seitentag, "is_open")],
    prevent_initial_call=True,
    suppress_callback_exceptions=True
)
def add_new_location(_1, _2, _3, URL_value, manual_occupancy, tab_value, modal_state):
    global data
    
    triggered_id = ctx.triggered_id

    if triggered_id == "modal_add_location_cancel_button" + seitentag:
        return not modal_state
    elif triggered_id == "open_modal_add_location_button" + seitentag:
        return not modal_state
    elif triggered_id == "modal_add_location_submit_button" + seitentag:
        #add new location
        if tab_value == "tab_add_url":
            #function to parse URL and update data/csv

            #maybe also check for security if this is also empty
            pass
        #add manually
        else:
            #function to take values from parameters and update data/csv
            pass

        return not modal_state
    else:
        raise PreventUpdate



#------
#sidebar handling
@callback(
    [Output("sideboard_name_filter" + seitentag, "value"),
    Output("sideboard_occupancy_filter" + seitentag, "value")],
    [Input("sideboard_name_filter" + seitentag, "value"),
    Input("sideboard_occupancy_filter" + seitentag, "value"),
    Input("clear_filter_button" + seitentag, "n_clicks"),],
    prevent_initial_call=True
)
def respond_to_sidebar(sideboard_name_filter, sideboard_occupancy_filter, _n1):
    global data

    triggered_id = ctx.triggered_id
    
    if triggered_id == "clear_filter_button" + seitentag:
        return "", "None"
        
    reset_data()
    filter_dict = create_filter_dict(sideboard_name_filter, sideboard_occupancy_filter)
    filter_data(filter_dict)

    return sideboard_name_filter, sideboard_occupancy_filter,

#-----
#layout refresh callback
@callback(
    Output("list_layout", "children"),
    [Input("modal_submit_button" + seitentag, "n_clicks"),
    Input("modal_cancel_button" + seitentag, "n_clicks"),
    Input("clear_filter_button" + seitentag, "n_clicks"),
    Input("modal_add_location_submit_button" + seitentag, "n_clicks"),
    Input("sideboard_name_filter" + seitentag, "value"),
    Input("sideboard_occupancy_filter" + seitentag, "value"),],
    prevent_initial_call=True
)
def update_layout(*args):

    triggered_id = ctx.triggered_id
    #print(triggered_id)

    if triggered_id == "clear_filter_button" + seitentag:
        reset_data()
        return refresh_layout()
    else:
        return refresh_layout()





def filter_data(filter_dict: dict[str:str]):
    global data

    data = filter_content(data, filter_dict)
    

def refresh_layout():
    names, content = create_content(data)

    layout = create_layout(names, content)

    return layout
    

def reset_data():
    global data
    data = get_data()
#---------------------------



"""
#function responsible for filtering and changing the layout
#callback inputs are all buttons and dash components used for either filtering or pop up/modal handeling
#callback outputs are interactive dash components for filtering and the pages layout
#state is the open/close state of the pop up/modal
@callback(
    [Output("list_layout", "children"), 
    Output("modal_window" + seitentag, "is_open"),
    Output("sideboard_name_filter" + seitentag, "value"),
    Output("modal_name_filter" + seitentag, "value"),
    Output("modal_occupancy_filter" + seitentag, "value"),
    Output("sideboard_occupancy_filter" + seitentag, "value")],
    [Input("clear_filter_button" + seitentag, "n_clicks"),
    Input("advanced_filter_button" + seitentag, "n_clicks"),
    Input("modal_submit_button" + seitentag, "n_clicks"),
    Input("modal_cancel_button" + seitentag, "n_clicks"),
    Input("modal_name_filter" + seitentag, "value"),
    Input("modal_occupancy_filter" + seitentag, "value"),
    Input("sideboard_name_filter" + seitentag, "value"),
    Input("sideboard_occupancy_filter" + seitentag, "value"),
    Input({"type": "button_control", "index": ALL}, "n_clicks")],
    [State("modal_window" + seitentag, "is_open")],
    prevent_initial_call=True
)
def filter_list(_n1, _n2, _n3, _n4, modal_name_text, modal_occupancy_radio, sideboard_name_text, sideboard_occupancy_radio, _delete_button, modal_state): #cancel_c_clicks,
    global data, temp_data

    triggered_id = ctx.triggered_id
    #print(type(triggered_id))
    #depending on the button pressed, act accordingly and return according values
    if isinstance(triggered_id, dash._utils.AttributeDict):
        filter_id = triggered_id["index"]
        # Call method for updating csv/deleting line with index from csv
        data = filter_for_index(data, filter_id)
        temp_data = filter_for_index(temp_data, filter_id)
        return keep_layout(), modal_state, sideboard_name_text, modal_name_text, modal_occupancy_radio, sideboard_occupancy_radio
    elif triggered_id == "clear_filter_button" + seitentag:
        return revert_filter_buttons(), modal_state, "", "", "None", "None"
    elif triggered_id == "advanced_filter_button" + seitentag:
        return keep_layout(), (not modal_state), "", modal_name_text, modal_occupancy_radio, "None"
    elif triggered_id == "modal_submit_button" + seitentag:
        filter_dict = create_filter_dict(modal_name_text, modal_occupancy_radio)
        return filter_buttons(filter_dict), (not modal_state), "", modal_name_text, modal_occupancy_radio, "None"
    elif triggered_id == "modal_cancel_button" + seitentag:
        return keep_layout(), (not modal_state), "", "", "None", "None"
    elif triggered_id == "sideboard_name_filter" + seitentag:
        filter_dict = create_filter_dict(sideboard_name_text, sideboard_occupancy_radio)
        return filter_buttons(filter_dict), False, sideboard_name_text, modal_name_text, modal_occupancy_radio, sideboard_occupancy_radio
    elif triggered_id == "sideboard_occupancy_filter" + seitentag:
        filter_dict = create_filter_dict(sideboard_name_text, sideboard_occupancy_radio)
        return filter_buttons(filter_dict), False, sideboard_name_text, modal_name_text, modal_occupancy_radio, sideboard_occupancy_radio
    else:
        raise PreventUpdate
 
        
#function to replace the filtered dataframe with the original
#returns layout of page
def revert_filter_buttons():
    global data, temp_data
    
    names2, content2 = create_content(data)
    layout2 = create_layout(names2, content2)
    temp_data = data.copy(deep=True)

    return layout2

#function to replace the filtered dataframe with itself, not changing anything
#returns layout of page
def keep_layout():
    global data, temp_data

    temp_data = filter_content(temp_data, {"location": None, "occupancy_traffic_light": None})
    names2, content2 = create_content(temp_data)
    layout2 = create_layout(names2, content2)
    
    return layout2

#function to replace the current dataframe with the filtered version of the original
#returns layout of page
def filter_buttons(filter_dict: dict[str:str]):

    global data, temp_data

    temp_data = data.copy(deep=True)

    temp_data = filter_content(temp_data, filter_dict)
    names2, content2 = create_content(temp_data)
    layout2 = create_layout(names2, content2)
    return layout2
"""
