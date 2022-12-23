import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State, MATCH, ALL
import numpy as np
from dash.exceptions import PreventUpdate
from utility.util_functions import *
from utility.filter_funktion import filter_names, filter_for_value

#global so the filter functions can access the date
global data, temp_data

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
df = get_data()
table = dbc.Table.from_dataframe(
    df, striped=True, bordered=True, hover=True, index=True
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

    #init list of components
    html_list = []

    #iterate through names(names and content must have the same length)
    for i in range(len(names)):
        #append header of location
        html_list.append(dbc.CardHeader(dbc.Button(
                    names[i],
                    color="outline",
                    id={"type":"header", "index":i},
                    value=i
                )))
                #append collapsible content
        html_list.append(dbc.Collapse(
            dbc.CardBody(table),
           #dbc.CardBody(content[i]),
            id={"type":"content", "index":i}, 
            is_open=False
        ))

    #in case no name sare given(normally means filtering was unsuccessful)
    if len(names) == 0:
        html_list.append(html.H3("No results found!"))
        html_list.append(html.Hr())

    return html_list

#create headers and content
names, content = create_content(data)
#create new layout
html_list_for_layout = create_layout(names, content)

layout = html.Div(children=html_list_for_layout, id="page-layout")



#function to collapse and expand the list items
#takes all dash objects with id type content and header, and then outputs the result to the content type with matching id index
@callback(
    Output({"type": "content", "index": MATCH}, "is_open"),
    [Input({"type": "header", "index": MATCH}, "n_clicks")],
    [State({"type": "content", "index": MATCH}, "is_open")],
)
def toggle_collapses(_butts, stats):
    ctxx = dash.callback_context
        
    if not ctxx.triggered:
        raise PreventUpdate
    else:
        #return opposite state of triggered button for either collapse or expand
        return not stats



#function responsible for filtering and changing the layout
#callback inputs are all buttons and dash components used for either filtering or pop up/modal handeling
#callback outputs are interactive dash components for filtering and the pages layout
#state is the open/close state of the pop up/modal
@callback(
    [Output("page-layout", "children"), 
    Output("modal_window", "is_open"),
    Output("sideboard_name_filter", "value"),
    Output("modal_name_filter", "value"),
    Output("modal_occupancy_filter", "value")],
    [Input("clear_filter_button", "n_clicks"),
    Input("advanced_filter_button", "n_clicks"),
    Input("modal_submit_button", "n_clicks"),
    Input("modal_cancel_button", "n_clicks"),
    Input("modal_name_filter", "value"),
    Input("modal_occupancy_filter", "value"),
    Input("sideboard_name_filter", "value")],
    [State("modal_window", "is_open")],
    prevent_initial_call=True
)
def filter_list(_n1, _n2, _n3, _n4, modal_name_text, modal_occupancy_radio, sideboard_name_text, modal_state): #cancel_c_clicks,
    triggered_id = ctx.triggered_id

    #depending on the button pressed, act accordingly and return according values
    if triggered_id == "clear_filter_button":
        return revert_filter_buttons(), modal_state, "", "", "None"
    elif triggered_id == "advanced_filter_button":
        return keep_layout(), (not modal_state), "", modal_name_text, modal_occupancy_radio
    elif triggered_id == "modal_submit_button":
        filter_dict = create_filter_dict(modal_name_text, modal_occupancy_radio)
        return filter_buttons(filter_dict), (not modal_state), "", modal_name_text, modal_occupancy_radio
    elif triggered_id == "modal_cancel_button":
        return keep_layout(), (not modal_state), "", "", "None"
    elif triggered_id == "sideboard_name_filter":
        filter_dict = create_filter_dict(sideboard_name_text, modal_occupancy_radio)
        return filter_buttons(filter_dict), False, sideboard_name_text, modal_name_text, modal_occupancy_radio
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
    """
    filter_dict: dictionary to filter the dataframe by
    """

    global data, temp_data

    temp_data = data.copy(deep=True)

    temp_data = filter_content(temp_data, filter_dict)
    names2, content2 = create_content(temp_data)
    layout2 = create_layout(names2, content2)
    return layout2
