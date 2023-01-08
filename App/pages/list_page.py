import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State, MATCH, ALL
import numpy as np
from dash.exceptions import PreventUpdate
from utility.util_functions import *
from utility.filter_funktion import filter_names, filter_for_value, filter_for_index
from components.sidebar import get_sidebar

#global so the filter functions can access the date
global data, temp_data


DEL_BUTTON_STYLE = {  # Define the style of the buttons
    #"width": "8rem",  # Set the width of the buttons to 8rem
    #"height": "2rem",  # Set the height of the buttons to 2rem
    "padding": "2rem 1rem",  # Add some padding to the buttons
    "marginRight": "0%",  # Align the text in the buttons to the right
}
# creating the refresh Button on the list_page
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
            mini = str(row[c].values[0])
            #mini = str(c) + ": " + str(row[c].values[0])
            inhalt.append(mini)
            inhalt.append(html.Br())

        content.append(inhalt)

    return names, content

#table for characteristics

def create_table(content:list[str]):

    table_header = [
        html.Thead(html.Tr([html.Th("Charakeristik"), html.Th("Wert")]))
    ]
    charakter = ["location","lat" ,"lon","occupancy_tendency","occupancy_tendency:de","occupancy_traffic_light","occupancy_label:de" ]
    rows = [html.Tr([html.Td(charakter[i]), html.Td(content[i*2])]) for i in range (len(charakter))]

    table_body = [html.Tbody(rows)]

    table_1 = dbc.Table(table_header + table_body, bordered=True, hover=True)

    return table_1



def create_edit_button(index:int):
    edit_button = html.Button("edit", id = {"type":"button_eddit", "index":index}, style ={"width": "6rem",
                                "height": "3rem","text-align":"center", "marginLeft": "77%"})
    return edit_button


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
                    style = {"width" :"80%"}
                ), html.Button("Löschen", id={"type":"button_control", "index":i})]))
                #append collapsible content
        html_list.append(dbc.Collapse(
            [dbc.CardBody(create_table(content[i]), style ={"width": "80%"}), create_edit_button(i),create_edit_window(i) ],
            #dbc.CardBody(content[i]),
            #html.Iframe(create_table()),
            id={"type":"content", "index":i},
            is_open=False,
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

layout = html.Div(children=html_list_for_layout, id="list_layout")



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


@callback(
    Output("test_side", "value"),
    [Input({"type": "button_control", "index": ALL}, "n_clicks")],
    prevent_initial_call=True,
)
def remove_location(_n):
    triggered_id = ctx.triggered_id

    return triggered_id["index"]


#method which edits the data according to the changes in the edit_window
def edit_data(changed_data:list[str],index):
    global data, temp_data

    charakeristics = ["price","road_network_connection","number_parking_lots","administration","surrounding_infrastructure","kind","public_transport"]

    for i in range(len(changed_data)):
        data.iloc[index][charakeristics[i]] = changed_data[i]

    temp_data = data


#method to open the edit window and to close it after pressing the apply button
@callback(
    Output({"type": "edit_window", "index": MATCH}, "is_open"),
    [Input({"type": "button_eddit", "index": MATCH}, 'n_clicks'),
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

    global data, temp_data


    # if the edit button was pressed the edit window opens
    if triggered_id["type"] == "button_eddit":
        return (not edit_state)

    # if the apply button was pressed the edit window closes and the data updates
    elif triggered_id["type"] == "edit_submit_button" :

        #edit_data([price,connection,parking_lots, administration, infrastructure, parking_type, accessibility],index)
        return(not edit_state)
    else:
        raise PreventUpdate

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
    Input("refresh_list", 'n_clicks'),
    Input({"type": "edit_submit_button", "index": ALL}, 'n_clicks'),
    Input("modal_name_filter" + seitentag, "value"),
    Input("modal_occupancy_filter" + seitentag, "value"),
    Input("sideboard_name_filter" + seitentag, "value"),
    Input("sideboard_occupancy_filter" + seitentag, "value"),
    Input({"type": "button_control", "index": ALL}, "n_clicks")],
    [State("modal_window" + seitentag, "is_open")],
    prevent_initial_call=True
)
def filter_list(_n1, _n2, _n3, _n4, _n5, _n6, modal_name_text, modal_occupancy_radio, sideboard_name_text, sideboard_occupancy_radio, _delete_button, modal_state): #cancel_c_clicks,
    global data, temp_data

    triggered_id = ctx.triggered_id
    #print(type(triggered_id))
    #depending on the button pressed, act accordingly and return according values
    if isinstance(triggered_id, dash._utils.AttributeDict):
        filter_id = triggered_id["index"]
        # Call method for updating csv/deleting line with index from csv
        if(triggered_id["type"] == "edit_submit_button"):
            data.drop(data.loc[data['location'] == "Heidelberg"].index, inplace = True )
            return update_list(_n6),modal_state, sideboard_name_text, modal_name_text, modal_occupancy_radio, sideboard_occupancy_radio

        else:
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
    elif triggered_id == "refresh_list":
        return update_list(_n5), False, sideboard_name_text, modal_name_text, modal_occupancy_radio,sideboard_occupancy_radio
    elif triggered_id == "button_eddit":
        print("hello")
        return keep_layout(), False, sideboard_name_text, modal_name_text, modal_occupancy_radio,sideboard_occupancy_radio

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

#function to update the dataframe according to the data (checking for potentiell changes in the data)
# returns the updated layou of the page
def update_list(nr_clicks):
    global data, temp_data

    if nr_clicks == None:
        raise PreventUpdate

    data = get_data()
    temp_data = data.copy(deep=True)
    # only for the tetsing
    #temp_data.drop(temp_data.loc[temp_data['location'] == "Heidelberg"].index, inplace = True )


    names2, content2 = create_content(temp_data)
    layout2 = create_layout(names2, content2)
    return layout2
