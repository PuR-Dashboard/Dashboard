import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State, MATCH, ALL
import numpy as np
from dash.exceptions import PreventUpdate
from utility.util_functions import *
from utility.filter_funktion import filter_names, filter_for_value, filter_for_index, filter_for_list, filter_max_value
from components.sidebar import get_sidebar
import plotly.express as px
import pages.global_vars as glob_vars
from collections import defaultdict

import fontstyle



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
#data = get_data(name_of_csv="Characteristics.csv")
#print(data.columns, len(data.columns))
#list_row = ["Heidelberg", 1,  1, "None", "None", "None", "None", "None", "1-25", "None"]
#data.loc[len(data)] = list_row

#print("Data: ", data)
#editable copy for filtering content
#temp_data = data.copy(deep=True)



def create_edit_window(index:int):
    edit_popUp = dbc.Modal(  # Modal to display the advanced filter
        [
            dbc.ModalHeader("Edit"),# Header of the modal
            dbc.ModalBody(  # Body of the modal
                [
                    dbc.Label("address"),
                    dbc.Input(
                                    id={"type":"edit_address", "index":index},
                                    type="text",  # Set the type of the input field to text
                                    debounce=False,  # Set the debounce-attribute of the input field to True
                                    placeholder="edit adress",
                                    value=None  # Set the value of the input field to an empty string
                    ),
                    dbc.Label("Administration:",style = {"margin-top":"5%"}),
                    dbc.RadioItems(  # Radio buttons to select the occupancy
                        options=[  # Define the options of the radio buttons
                                    {'label': 'Yes', 'value': 'yes'},  # Option for high occupancy
                                    {'label': 'No', 'value': 'no'},  # Option for medium occupancy
                                    {'label': 'No specification', 'value': None}  # Option for no occupancy
                                ],
                        value=None,  # Set the value of the radio buttons to None
                        inline=True,  # Set the inline-attribute of the radio buttons to False
                        id={"type":"edit_administration", "index":index}  # Set the id of the radio buttons to modal_occupancy_filter
                    ),

                    dbc.Label("Parking type",style = {"margin-top":"5%", "weight":"bold"}),
                    dcc.Dropdown(
                                    options=[
                                        {'label': 'Parkhaus', 'value': 'Parkhaus'},
                                        {'label': 'Separate Fläche', 'value': 'Separate Fläche'},
                                        {'label': 'Am Fahrbahnrand / an der Straße', 'value': 'Am Fahrbahnrand / an der Straße'},
                                    ],
                                    placeholder="edit parking type",
                                    id={"type":"edit_parking_type", "index":index},
                                ),

                    dbc.Label("Number of carports",style = {"margin-top":"5%", "weight":"bold"}),
                    dcc.RangeSlider(min=1,max=6,step=None,id={"type":"edit_parking_lots", "index":index}, updatemode='drag',
                                    marks={
                                        1: '1',
                                        2: '25',
                                        3: '50',
                                        4: '100',
                                        5: '200',
                                        6: "1200",
                                    },
                                    value=[1, 6],
                    ),

                    dbc.Label("Max Preis(\u20ac):",style = {"margin-top":"5%"}),
                    dbc.Input(
                        id={"type":"edit_price", "index":index},
                        type="number",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to True
                        placeholder="edit price in \u20ac",
                        value=None  # Set the value of the input field to an empty string
                    ),

                    dbc.Label("ÖPNV accessibility",style = {"margin-top":"5%"}),
                    dbc.Input(
                                    id={"type":"edit_accessibility", "index":index},
                                    type="number",  # Set the type of the input field to text
                                    debounce=False,  # Set the debounce-attribute of the input field to True
                                    placeholder="edit ÖPNV accessibility",
                                    value=None  # Set the value of the input field to an empty string
                    ),

                    dbc.Label("Connection:",style = {"margin-top":"5%"}),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Übergeordnetes Netz innerorts (Bundesstraßen)', 'value': 'Übergeordnetes Netz innerorts (Bundesstraßen)'},
                            {'label': 'Übergeordnetes Netz außerorts (Bundesstraßen)', 'value': 'Übergeordnetes Netz außerorts (Bundesstraßen)'},
                            {'label': 'Nachgeordnetes Netz innerorts', 'value': 'Nachgeordnetes Netz innerorts'},
                            {'label': 'Nachgeordnetes Netz außerorts', 'value': 'Nachgeordnetes Netz außerorts'},
                        ],
                        placeholder="edit connection",
                        id={"type":"edit_connection", "index":index},
                    ),

                    dbc.Label("surrounding infrastructure",style = {"margin-top":"5%"}),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Grünflächen', 'value': 'Grünflächen'},
                            {'label': 'Wohnflächen', 'value': 'Wohnflächen'},
                            {'label': 'Industrieflächen', 'value': 'Industrieflächen'},
                            {'label': 'Gewerbegebieten', 'value': 'Gewerbegebieten'},
                            {'label': 'Mischflächen', 'value': 'Mischflächen'},
                        ],
                        placeholder="edit infrastructure",
                        id={"type":"edit_infrastructure", "index":index},
                    ),


                ]
            ),
            dbc.ModalFooter(  # Footer of the modal
                [
                    dbc.Button(  # Button to close the modal
                        "Apply",  # Text of the button
                        color="primary",  # Set the color of the button to primary
                        id={"type":"edit_submit_button", "index":index}  # Set the id of the button to modal_submit_button
                    ),

                ]
            ),
        ],
        id={"type":"edit_window", "index":index},  # Set the id of the modal to modal_window
        centered=True,  # Set the centered-attribute of the modal to True
    )
    return edit_popUp


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


#function to create a dictionary that can be passed to the filter_content() def
#hard coded, maybe change?? !!!!!
# filter dict entweder wert oder none, wenn None dann nix veränderun
# parameter order is important and corresponding to other parameter orders
def create_filter_dict(location:str = "", price:int = -1, parking_lots_range:list[int:int] = [1,6],
                        administration:str = "", road_network_connection:str = "",
                        parking_lot_marks:dict[str:str] = {'1': '1', '2': '25', '3': '50', '4': '100', '5': '200', '6': '1200'},
                        surrounding_infrastructure:str = "", kind:str = "", public_transport:int = -1):
    """
    location: location name
    price: price of the station
    parking_lots_range: list with min and max parking lot values
    parking_lot_marks: dictionary with principal parking lot values
    road_network_connection: kind of connection
    administration: yes, no, ""; if station is administrated
    surrounding_structure: <-, categories
    kind: what kind of station; categories
    public_transport: amount of public transport connections

    returns: dictionary of characteristics and values
    """
    #currently only filters for location and occupancy


    #string_parameters = [location, road_network_connection, administration, surrounding_infrastructure, kind]
    #int_parameters = [price, public_transport]

    filter_dict = {}


    if parking_lots_range[0] == 1 and parking_lots_range[1] == 6:
        filter_dict["number_parking_lots"] = None
    else:
        l = make_parking_lot_list(parking_lots_range[0], parking_lots_range[1], parking_lot_marks)
        if len(l) == 0:
            filter_dict["number_parking_lots"] = None
        else:
            filter_dict["number_parking_lots"] = l

    if location == "":
        filter_dict["location"] = None
    else:
        filter_dict["location"] = location

    if road_network_connection == "":
        filter_dict["road_network_connection"] = None
    else:
        filter_dict["road_network_connection"] = road_network_connection

    if administration == "":
        filter_dict["administration"] = None
    else:
        filter_dict["administration"] = administration

    if surrounding_infrastructure == "":
        filter_dict["surrounding_infrastructure"] = None
    else:
        filter_dict["surrounding_infrastructure"] = surrounding_infrastructure

    if kind == "":
        filter_dict["kind"] = None
    else:
        filter_dict["kind"] = kind

    if price == -1:
        filter_dict["price"] = None
    else:
        filter_dict["kind"] = price

    if public_transport == -1:
        filter_dict["public_transport"] = None
    else:
        filter_dict["public_transport"] = public_transport



    return filter_dict


#function to create the content of the tables(the content of the collapsibles)
#will be switched out by table through vuetify library and is not documented further -> soon to be DEPRECATED
def create_content(df: pd.DataFrame):
    #print("create data: ", df)
    cols = df.columns
    #print(cols)
    content = []
    names = []

    for i in range(len(df)):
        row = df.iloc[[i]]

        names.append(row["location"].values[0])

        inhalt = []
        for c in cols:
            mini = str(row[c].values[0])
            #mini = str(c) + ": " + str(row[c].values[0])
            inhalt.append(mini)
            inhalt.append(html.Br())

        content.append(inhalt)

    return names, content

#table for characteristics

def create_table(content:list[str]):

    table_header = [
        html.Thead(html.Tr([html.Th("Charakeristiken"), html.Th("")]))
    ]
    charakter = ["location:","lat:" ,"lon:","occupancy_tendency:","occupancy_tendency:","occupancy_traffic_light:","occupancy_label:" ]
    rows = [html.Tr([html.Td(charakter[i]), html.Td(content[i*2])]) for i in range (len(charakter))]

    table_body = [html.Tbody(rows)]

    table_1 = dbc.Table(table_header + table_body, borderless=True, hover=False)

    return table_1


#create plot for the distribution over the week
#!!!!Fehlen die Daten, um die Verteilung für die Orte individuell zu gestalten
def create_plot(content:list[str] = [1,2,3,4,5,6]):


    graph = dcc.Graph(
        figure={
            'data': [
                {'x': ["Montag","Dienstag", "Mittwoch", "Donnerstag","Freitag", "WE"], 'y': [content[0],content[1],content[2],content[3],content[4],content[5], ],
                'type': 'bar','name': 'Auslastung',
                "marker": {"color": "lightskyblue"}}
            ],
            'layout': {
                'title': 'Prognose über die Woche'
            }
        }
    )
    return graph


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
    FA_icon = html.I(className="fa fa-refresh")
    button_refresh = (html.Div(dbc.Button([FA_icon, " Refresh"], color="light", className="me-1",id = "refresh_list", value = 0,
                    style={
                        "marginLeft": "0%",
                        "width": "7%",
                        "height": "60%",
                        "fontSize": "1em",
                       # "background-color": "grey",
                        "color": "black",
                       # "border-radius": "4px",
                       # "border": "2px solid black",
                    },
                    )))
    #init list of components
    html_list = []
    html_list.append(button_refresh)
    #html_list.append(dbc.Input(  # Input field for the name
    #                    id="test_side",  # Set the id of the input field to sideboard_name_filter
    #                    type="text",  # Set the type of the input field to text
    #                    debounce=False,  # Set the debounce-attribute of the input field to False
    #                    value="",  # Set the value of the input field to an empty string
    #                    placeholder="Location Name",  # Set the placeholder of the input field to Location Name
    #                    autofocus=True  # Set the autofocus-attribute of the input field to True
    #                ),)


    #iterate through names(names and content must have the same length)
    for i in range(len(names)):
        #append header of location
        html_list.append(dbc.CardHeader([dbc.Button(
                    names[i],
                    color="outline",
                    id={"type":"header", "index":i},
                    value=i,
                    
                ), dbc.Button([FA_icon_trash, ""], id={"type":"button_control", "index":i}, className = "pull-right",style = ARR_BUTTON_STYLE),
                   dbc.Button([FA_icon_pen, ""], id={"type":"pen_button", "index" :i}, className = "pull-right" ,style = ARR_BUTTON_STYLE),
                   dbc.Button([FA_icon_Arrow, ""], id={"type":"arrow_button", "index" :i}, className = "pull-right" ,style = ARR_BUTTON_STYLE)
                   ], style = {"width":"87%"}))

                #append collapsible content
        html_list.append(dbc.Collapse(
            [dbc.CardBody(create_table(content[i]), style ={"width": "60%", "marginLeft": "3%"}), dbc.CardBody(create_plot(),style ={"width": "50%", "color": "#F0F8FF"}) , create_edit_window(i)],
            #dbc.CardBody(content[i]),
            #html.Iframe(create_table()),
            id={"type":"content", "index":i},
            style = {"width":"87%"},
            is_open=False
        ))

    #in case no name sare given(normally means filtering was unsuccessful)
    if len(names) == 0:
        html_list.append(html.H3("No results found!"))
        html_list.append(html.Hr())

    html_list.append(sid)

    return html_list

#create headers and content
names, content = create_content(glob_vars.data)
#create new layout
html_list_for_layout = create_layout(names, content)

layout = html.Div(children=html_list_for_layout, id="list_layout")

#print(type(glob_vars.data["number_parking_lots"][0]))

#Callbacks:-----------------------------------------------

@callback(
    Output("modal_testing_indication" + seitentag, "value"),
    [Input("second_modal_testing_indication" + seitentag, "value")]
)
def testing_indi(val):
    return val



@callback(
    Output({"type": "button_control", "index": MATCH}, "n_clicks"),
    [Input({"type": "button_control", "index": MATCH}, "n_clicks")],
    prevent_initial_call=True,
)
def delete_location(del_button):
    triggered_id = ctx.triggered_id["index"]

    row_to_delete = glob_vars.data.iloc[[triggered_id]]
    location_to_delete = row_to_delete["location"].values[0]
    #print(row_to_delete, location_to_delete)

    path = get_path_to_csv(name_of_csv="Characteristics_testing.csv")

    temp_data = get_data(name_of_csv="Characteristics_testing.csv")
    temp_data = temp_data[temp_data["location"] != location_to_delete]
    
    temp_data.to_csv(path, index=False)

    reset_data()
    filter_data()

    #print(triggered_id)

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


#method which edits the data according to the changes in the edit_window
def edit_data(changed_data:list[str],index):
    #global data, temp_data

    charakteristics = ["price","road_network_connection","number_parking_lots","administration","surrounding_infrastructure","kind","public_transport"]

    for i in range(len(changed_data)):
        glob_vars.data.iloc[index][charakteristics[i]] = changed_data[i]



#method to open the edit window and to close it after pressing the apply button
@callback(
    Output({"type": "edit_window", "index": MATCH}, "is_open"),
    [Input({"type": "pen_button", "index": MATCH}, 'n_clicks'),
     Input({"type": "edit_submit_button", "index": MATCH}, 'n_clicks'),
     Input({"type": "edit_address", "index": MATCH}, 'value'),
     Input({"type": "edit_parking_lots", "index": MATCH}, 'value'),
     Input({"type": "edit_accessibility", "index": MATCH}, 'value'),
     Input({"type": "edit_price", "index": MATCH}, 'value'),
     Input({"type": "edit_infrastructure", "index": MATCH}, 'value'),
     Input({"type": "edit_administration", "index": MATCH}, 'value'),
     Input({"type": "edit_parking_type", "index": MATCH}, 'value'),
     Input({"type": "edit_connection", "index": MATCH}, 'value'), ],
    [State({"type": "edit_window", "index": MATCH}, "is_open")],
    prevent_initial_call=True,
)
def open_edit_window(n_clicks_edit,n_clicks_submit,adress, parking_lots, accessibility,price, infrastructure, administration,parking_type, connection, edit_state):

    triggered_id = ctx.triggered_id

    #+global data

    # if the edit button was pressed the edit window opens
    if triggered_id["type"] == "pen_button":
        return (not edit_state)

    # if the apply button was pressed the edit window closes and the data updates
    elif triggered_id["type"] == "edit_submit_button" :

        #edit_data([price,connection,parking_lots, administration, infrastructure, parking_type, accessibility],index)
        return(not edit_state)
    else:
        raise PreventUpdate

#---------testing------------

#modal filter handling
@callback(
    [Output("modal_filter_window" + seitentag, "is_open"),
    Output("modal_advanced_filter_name" + seitentag, "value"),
    Output("modal_advanced_filter_price" + seitentag, "value"),
    Output("modal_advanced_filter_connection" + seitentag, "value"),
    Output("modal_advanced_filter_parking_lots" + seitentag, "value"),
    Output("modal_advanced_filter_administration" + seitentag, "value"),
    Output("modal_advanced_filter_infrastructure" + seitentag, "value"),
    Output("modal_advanced_filter_kind" + seitentag, "value"),
    Output("modal_advanced_filter_num_connections" + seitentag, "value"),],
    [Input("advanced_filter_button" + seitentag, "n_clicks"),
    Input("modal_filter_submit_button" + seitentag, "n_clicks"),
    Input("modal_filter_cancel_button" + seitentag, "n_clicks"),
    Input("modal_advanced_filter_parking_lots" + seitentag, "marks"),
    Input("modal_advanced_filter_name" + seitentag, "value"),
    Input("modal_advanced_filter_price" + seitentag, "value"),
    Input("modal_advanced_filter_connection" + seitentag, "value"),
    Input("modal_advanced_filter_parking_lots" + seitentag, "value"),
    Input("modal_advanced_filter_administration" + seitentag, "value"),
    Input("modal_advanced_filter_infrastructure" + seitentag, "value"),
    Input("modal_advanced_filter_kind" + seitentag, "value"),
    Input("modal_advanced_filter_num_connections" + seitentag, "value"),],
    [State("modal_filter_window" + seitentag, "is_open")],
    prevent_initial_call=True
)
def advanced_filter_handling(_n1, _n2, _n3, parking_lot_marks, *params):
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
    charac_with_none = ["location", "road_network_connection", "administration", "surrounding_infrastructure", "kind", "price", "public_transport"]
    two_value_slider = ["number_parking_lots"]


    empty_ret_list = []

    for c in characteristics:
        if c in charac_with_none:
            empty_ret_list.append(None)
        elif c in two_value_slider:
            if c == "number_parking_lots":
                empty_ret_list.append([1,6])



    if triggered_id == "modal_filter_cancel_button" + seitentag:
        return (not modal_state,) + tuple(empty_ret_list)
    elif triggered_id == "modal_filter_submit_button" + seitentag:
        reset_data()
        #filter_dict = {}


        for c, chara in zip(characs, characteristics):
            if c == None:
                continue
            if chara == "number_parking_lots":
                if c[0] == 1 and c[1] == 6:
                    c = None
                else:
                    c = make_parking_lot_list(c[0], c[1], parking_lot_marks)

            glob_vars.current_filter[chara] = c

        print(glob_vars.current_filter)

        #filter_dict = create_filter_dict(*characs)
        filter_data(glob_vars.current_filter)
        return (not modal_state,) + tuple(characs)
    elif triggered_id == "advanced_filter_button" + seitentag:
        characs = list(characs)
        for i in range(len(characteristics)):
            key = characteristics[i]
            #print(key)
            if glob_vars.current_filter[key] == None:
                continue
            else:
                characs[i] = glob_vars.current_filter[key]


        return (not modal_state,) + tuple(characs)
    else:
        raise PreventUpdate

#------
#modal add handling


#open adding module, add location etc
@callback(
    [Output("modal_add_location" + seitentag, "is_open"),
    Output("modal_field_warning" + seitentag, "style"),
    Output("modal_add_location_url" + seitentag, "value"),
    Output("modal_add_location_name" + seitentag, "value"),
    Output("modal_add_location_price" + seitentag, "value"),
    Output("modal_add_location_connection" + seitentag, "value"),
    Output("modal_add_location_parking_lots" + seitentag, "value"),
    Output("modal_add_location_administration" + seitentag, "value"),
    Output("modal_add_location_infrastructure" + seitentag, "value"),
    Output("modal_add_location_kind" + seitentag, "value"),
    Output("modal_add_location_num_connections" + seitentag, "value"),],
    [Input("modal_add_location_submit_button" + seitentag, "n_clicks"),
    Input("open_modal_add_location_button" + seitentag, "n_clicks"),
    Input("modal_add_location_cancel_button" + seitentag, "n_clicks"),
    Input("modal_add_location_url" + seitentag, "value"),
    Input("modal_add_location_name" + seitentag, "value"),
    Input("modal_add_location_price" + seitentag, "value"),
    Input("modal_add_location_connection" + seitentag, "value"),
    Input("modal_add_location_parking_lots" + seitentag, "value"),
    Input("modal_add_location_administration" + seitentag, "value"),
    Input("modal_add_location_infrastructure" + seitentag, "value"),
    Input("modal_add_location_kind" + seitentag, "value"),
    Input("modal_add_location_num_connections" + seitentag, "value"),],
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
        return (not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    elif triggered_id == "open_modal_add_location_button" + seitentag:
        return (not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    elif triggered_id == "modal_add_location_submit_button" + seitentag:
        #check if URL and name are given
        error_made = [False, False]
        #url must be given
        if URL_value == None or URL_value == "":

            return (modal_state, {"display":"block", "color":"red"}, URL_value) + tuple(characs)

        #location name must be given
        if characs[0] == None or characs[0] == "":

            return (modal_state, {"display":"block", "color":"red"}, URL_value) + tuple(characs)


        #make dictionary for function
        add_dictionary = {}
        #print("worked anyways lol")
        for c, charac in zip(characs, characteristics):
            add_dictionary[charac] = c

        # NOW FUNCTION TO ADD LOCATION TO CSV


        return (not modal_state, {"display":"none", "color":"red"}, None, None) + tuple([None for x in characs[1:]])
    else:
        raise PreventUpdate



#-----
#layout refresh callback and sidebar handling
#ANMERKUNGEN: Maybe braucht man hier keine args liste sondern kann einfach feste parameter machen? kommt drauf an wie viele parameter am ende
@callback(
    [Output("list_layout", "children"),
    Output("sideboard_name_filter" + seitentag, "value"),
    Output("sideboard_administration_filter" + seitentag, "value"),
    Output("sideboard_parking_lots_slider" + seitentag, "value"),],
    [Input("modal_filter_submit_button" + seitentag, "n_clicks"),
    #Input("modal_filter_cancel_button" + seitentag, "n_clicks"),
    Input("clear_filter_button" + seitentag, "n_clicks"),
    Input("refresh_list", "n_clicks"),
    #Input("modal_add_location_cancel_button" + seitentag, "n_clicks"),
    Input("sideboard_parking_lots_slider" + seitentag, "marks"),
    #Input("placeholder_div" + seitentag, "n_clicks"),
    Input("sideboard_name_filter" + seitentag, "value"),
    Input("sideboard_administration_filter" + seitentag, "value"),
    Input("sideboard_parking_lots_slider" + seitentag, "value"),],
    prevent_initial_call=True
)
def update_layout(*args):

    triggered_id = ctx.triggered_id
    #print(triggered_id)

    #manually write characteristics of quick filters
    sidebar_characs = ["location", "administration", "number_parking_lots"]

    #num is amount of sidebar elements that are quickfilter, i.e. the last num inputs of this callback
    num = 3
    sidebar_values = args[-num:]
    print("VALS: ", sidebar_values)
    # index of callback input for 
    marks = args[-4]

    if triggered_id == "clear_filter_button" + seitentag:
        reset_data()
        reset_global_filter()
        return refresh_layout(), "", "", [1,6]
    #elif triggered_id == "sideboard_name_filter" + seitentag or triggered_id == "sideboard_occupancy_filter" + seitentag:
    elif triggered_id == "refresh_list":
        return refresh_layout(), args[-3], args[-2], args[-1]
    else:
        #print(triggered_id, glob_vars.current_filter, marks, args[-1])
        reset_data()
        assert len(sidebar_characs) == len(sidebar_values)

        for s, val in zip(sidebar_characs, sidebar_values):
            if s == "number_parking_lots":
                if val[0] == 1 and val[1] == 6:
                    glob_vars.current_filter.pop(s, None)
                    continue
                else: 
                    #print("conversion: ", make_parking_lot_list(val[0], val[1], marks))
                    glob_vars.current_filter[s] = make_parking_lot_list(val[0], val[1], marks)
            elif val == None or val == "":
                glob_vars.current_filter.pop(s, None)
                continue
            else:
                glob_vars.current_filter[s] = val
        #filter_dict = create_filter_dict(administration=args[-2], parking_lots_range=args[-1])
        print(glob_vars.current_filter)
        filter_data()#glob_vars.current_filter)
        
        #print(glob_vars.data)

        return refresh_layout(), args[-3], args[-2], args[-1]




def make_parking_lot_list(mini, maxi, values):
    value_list = []

    for i in range(mini, maxi):
        i_range = values[str(i)] + "-" + values[str(i+1)]
        value_list.append(i_range)

    return value_list


def reset_global_filter():
    glob_vars.current_filter = defaultdict(lambda: None)


def filter_data():#filter_dict: dict[str:str]):
    #global data

    glob_vars.data = filter_content(glob_vars.data, glob_vars.current_filter)


def refresh_layout():
    names, content = create_content(glob_vars.data)

    layout = create_layout(names, content)

    return layout


def reset_data(name="Characteristics.csv"):
    #global data
    glob_vars.data = get_data("Characteristics_testing.csv")
    #list_row = ["Heidelberg", 1,  1, "None", "None", "None", "None", "None", "1-25", "None"]
    #glob_vars.data.loc[len(glob_vars.data)] = list_row
#---------------------------

