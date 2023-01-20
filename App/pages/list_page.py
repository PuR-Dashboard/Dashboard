import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State, MATCH, ALL
import numpy as np
from dash.exceptions import PreventUpdate
from utility.util_functions import *
from utility.filter_funktion import *
from utility.data_functions import *
from components.sidebar import get_sidebar
import plotly.express as px
import pages.global_vars as glob_vars
from collections import defaultdict
import fontstyle

FA_icon_trash= html.I(className="fa fa-trash fa-lg")
FA_icon_pen= html.I(className="fa fa-pencil fa-lg")

ARR_BUTTON_STYLE = { #Define the style of the arrow button
    "color": "black", #set the arrow itself is black
    "background-color":"transparent", #set the background color to transparent
    "border": "transparent" #set the border color to transparent
}
FA_icon_Arrow = html.I(className="fa fa-chevron-down fa-lg") #arrow icon for the arrow button

CONTENT_STYLE = { #style the content of list_page so that it aligns with the sidebar
    "position": "fixed",
    "width": "calc(113vw - 250px)",
    "height": "calc(100vh - 50px)",
    "flex-grow": "1",
    "seamless":"True"
}
global sid
seitentag = "_list"

sid = get_sidebar(seitentag)

def create_security_window(location:str, index:int):
    return dbc.Modal([dbc.ModalHeader("Deleting Location {}. Are you sure?".format(location)),
                      dbc.ModalBody(
                        [dbc.Button(  # Button to close the modal
                        "Yes!",  # Text of the button
                        style = {"background-color":"#b3b3b3",
                                 "border": "black",
                                 "color": "black",
                                 "margin-right":"15px"
                                } ,
                        id={"type":"security_yes_button", "index":index}  # Set the id of the button to modal_submit_button
                        ),
                        dbc.Button(  # Button to close the modal
                        "No.",  # Text of the button
                        style = {"background-color":"#b3b3b3",
                                 "border": "black",
                                 "color": "black"} ,   # Set the color of the button to primary
                        id={"type":"security_no_button", "index":index}  # Set the id of the button to modal_submit_button
                        ),
                        ]
                      )],
                      id={"type":"security_window", "index":index},  # Set the id of the modal to modal_window
                        centered=True,  # Set the centered-attribute of the modal to True
                        )

def create_edit_window(index:int):
    edit_popUp = dbc.Modal(  # Modal to display the advanced filter
        [
            dbc.ModalHeader("Edit"),# Header of the modal
            dbc.ModalBody(  # Body of the modal
                [
                    dbc.Label("Address"),
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

                    dbc.Label("Type of Facility",style = {"margin-top":"5%", "weight":"bold"}),
                    dcc.Dropdown(
                                    options=[
                                        {'label': 'Car Park', 'value': 'Car Park'},
                                        {'label': 'Separate Area', 'value': 'Separate Area'},
                                        {'label': 'At the edge of the road / on the road', 'value': 'At the edge of the road / on the road'},
                                    ],
                                    placeholder="edit type of facility",
                                    id={"type":"edit_parking_type", "index":index},
                                ),

                    dbc.Label("Number of Parking spots",style = {"margin-top":"5%", "weight":"bold"}),
                    dcc.Dropdown(
                        options=[
                            {'label': '1-25', 'value': '1-25'},
                            {'label': '25-50', 'value': '25-50'},
                            {'label': '50-100', 'value': '50-100'},
                            {'label': '100-200', 'value': '100-200'},
                            {'label': '200-1200', 'value': '200-1200'},
                        ],
                        placeholder="edit number of parking spots",
                        id={"type":"edit_parking_lots", "index":index}
                    ),

                    dbc.Label("Max Price(\u20ac):",style = {"margin-top":"5%"}),
                    dbc.Input(
                        id={"type":"edit_price", "index":index},
                        type="number",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to True
                        placeholder="edit price in \u20ac",
                        value=None  # Set the value of the input field to an empty string
                    ),

                    dbc.Label("Public Transport Accessibility",style = {"margin-top":"5%"}),
                    dbc.Input(
                                    id={"type":"edit_accessibility", "index":index},
                                    type="number",  # Set the type of the input field to text
                                    debounce=False,  # Set the debounce-attribute of the input field to True
                                    placeholder="edit public transport accessibility",
                                    value=None  # Set the value of the input field to an empty string
                    ),

                    dbc.Label("Transport Connection:",style = {"margin-top":"5%"}),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Superordinate network within the city (interstate)', 'value': 'Superordinate network within the city (interstate)'},
                            {'label': 'Superordinate network out of town (interstate)', 'value': 'Superordinate network out of town (interstate)'},
                            {'label': 'Subordinate network in the city', 'value': 'Subordinate network in the city'},
                            {'label': 'Subordinate network out of town', 'value': 'Subordinate network out of town'},
                        ],
                        placeholder="edit connection",
                        id={"type":"edit_connection", "index":index},
                    ),

                    dbc.Label("Surrounding Infrastructure",style = {"margin-top":"5%"}),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Green Spaces', 'value': 'Green Spaces'},
                            {'label': 'Living Spaces', 'value': 'Living Spaces'},
                            {'label': 'Industrial Areas', 'value': 'Industrial Areas'},
                            {'label': 'Industrial Parks', 'value': 'Industrial Parks'},
                            {'label': 'Mixed Areas', 'value': 'Mixed Areas'},
                        ],
                        placeholder="edit surrounding infrastructure",
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
                    #placeholder div for output of location edit
                    html.Div(id="placeholder_div_edit" + seitentag, style={"display":"none"}),

                ]
            ),
        ],
        id={"type":"edit_window", "index":index},  # Set the id of the modal to modal_window
        centered=True,  # Set the centered-attribute of the modal to True
    )
    return edit_popUp


#function to create the content of the tables(the content of the collapsibles)
#will be switched out by table through vuetify library and is not documented further -> soon to be DEPRECATED
def create_content(df: pd.DataFrame):
    #print("create data: ", df)
    cols = df.columns

    content = []
    names = []

    for i in range(len(df)):
        row = df.iloc[[i]]

        names.append(row["location"].values[0])

        inhalt = []
        for c in cols:
            mini = str(row[c].values[0])

            inhalt.append(mini)
            inhalt.append(html.Br())

        content.append(inhalt)

    return names, content

#table for characteristics

def create_table(content:list[str]):

    table_header = [
        html.Thead(html.Tr([html.Th("Charakeristiken"), html.Th("")]), style = {"marginTop":"5%"})
    ]
    charakter = ["address:","administration:" ,"Kind:","number of parking lots:","price:","public transport:","Road network connection:", "surrounding infrastructure" ]
    rows = [html.Tr([html.Td(charakter[i]), html.Td(content[(i+3)*2])]) for i in range (len(charakter))]

    table_body = [html.Tbody(rows)]

    table_1 = dbc.Table(table_header + table_body, borderless=False, hover=False)

    return table_1



#create plot for the distribution over the week
#!!!!Fehlen die Daten, um die Verteilung für die Orte individuell zu gestalten
def create_plot(content:list[str] = [1,2,3,4,5,6]):

    df = pd.DataFrame({
    "": ["Monday","Tuesday", "Wednesday", "Thursday","Friday", "WE"],
    "occupancy rate": [content[0],content[1],content[2],content[3],content[4],content[5]]
    })

    fig = px.bar(df, x="", y="occupancy rate")

    fig.update_layout(
        title = {
            'text' : "<b>Prediction over a week</b>",
        }
    )
    graph = dcc.Graph(
        figure =  fig,
        config={
            'displayModeBar': False
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


    #init list of components
    html_list = []



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
            [dbc.CardBody(create_table(content[i]), style ={"width": "60%", "marginLeft": "3%"}), dbc.CardBody(create_plot(),style ={"width": "50%", "color": "#F0F8FF"}) , create_edit_window(i), create_security_window(names[i], i), html.Div(id={"type":"security_id_transmitter", "index":i}, style={"display":"none"})],

            id={"type":"content", "index":i},
            style = {"width":"87%"},
            is_open=False
        ))
"""
        [dbc.Row([ #getting the table and picture next to each other
        dbc.Col(dbc.CardBody(create_table(content[i]), style ={"width": "180%", "marginLeft": "0%"}), width = "auto"),
        dbc.Col(dbc.CardImg(src= "https://th.bing.com/th/id/OIP.mbBEbzuRMttCVk4AyTzIxwHaD8?pid=ImgDet&rs=1", style ={"width": "100%", "marginLeft": "90%", "marginTop": "10%"}), width = "auto"),
        ],
        style ={"width": "80%", "marginLeft": "1%"}),
        #plot directly under the table
        dbc.CardBody(create_plot(),style ={"width": "45%", "color": "#F0F8FF"}),
        ],
           #[dbc.CardBody(create_table(content[i]), style ={"width": "60%", "marginLeft": "3%"}), dbc.CardBody(create_plot(),style ={"width": "50%", "color": "#F0F8FF"}) , create_edit_window(i)],"""

    #in case no name sare given(normally means filtering was unsuccessful)
    if len(names) == 0:
        html_list.append(html.H3("No results found!"))
        html_list.append(html.Hr())

    html_list.append(sid)
    html_list.append(
                    #placeholder div for output of location delete
                    html.Div(id="placeholder_div_delete_list", style={"display":"none"}))

    return html_list

#create headers and content
names, content = create_content(glob_vars.data)
#create new layout
html_list_for_layout = create_layout(names, content)

layout = html.Div(children=html_list_for_layout, id="list_layout", style = CONTENT_STYLE)

#print(type(glob_vars.data["number_parking_lots"][0]))

#Callbacks:-----------------------------------------------

@callback(
    Output({"type":"security_window", "index":MATCH}, "is_open"),
    [Input({"type":"button_control", "index":MATCH}, "n_clicks")],
    prevent_initial_call=True
)
def security_observer(_n):
    if _n == 0:
        return False
    return True


@callback(
    Output("placeholder_div_delete_list", "n_clicks"),
    [Input({"type":"security_id_transmitter", "index":2}, "n_clicks")],
    prevent_initial_call=True
)
def delete_observer(_n):
    return 1



@callback(
    [Output({"type":"security_id_transmitter", "index":MATCH}, "n_clicks"),
    Output({"type":"button_control", "index":MATCH}, "n_clicks"),],
    [Input({"type":"security_yes_button", "index":MATCH}, "n_clicks"),
    Input({"type":"security_no_button", "index":MATCH}, "n_clicks")],
    prevent_initial_call=True,
)
def delete_location(yes, no):

    triggered_id = ctx.triggered_id["index"]

    if ctx.triggered_id["type"] == "security_no_button":
        return dash.no_update, 0

    row_to_delete = glob_vars.data.iloc[[triggered_id]]
    location_to_delete = row_to_delete["location"].values[0]


    path = get_path_to_csv(name_of_csv="Characteristics.csv")

    temp_data = get_data(name_of_csv="Characteristics.csv")
    temp_data = temp_data[temp_data["location"] != location_to_delete]

    temp_data.to_csv(path, index=False)
    #remove_location_from_json(location=location_to_delete)

    reset_data()
    filter_data()

    return 1, 0


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

    characteristics = ["address","administration","kind","number_parking_lots","price","public_transport","road_network_connection","surrounding_infrastructure"]

    location = glob_vars.data.iloc[index]["location"]

    temp_data = get_data("Characteristics.csv")

    for i in range (len(temp_data)):
        if temp_data.iloc[i]["location"] == location:
            position = i
            break

    dic = {}
    dic["location"] =  temp_data.iloc[position]["location"]

    for i  in range(len(characteristics)):

        if changed_data[i] == None:
            dic[characteristics[i]] = np.squeeze(temp_data.iloc[position][characteristics[i]])

        else:
            dic[characteristics[i]] = changed_data[i]


    update_characteristics_in_csv(dic)



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
def open_edit_window(n_clicks_edit,n_clicks_submit,adress, parking_lots, accessibility,price, infrastructure, administration,kind, connection, edit_state):

    triggered_id = ctx.triggered_id

    #+global data

    # if the edit button was pressed the edit window opens
    if triggered_id["type"] == "pen_button":
        return (not edit_state)

    # if the apply button was pressed the edit window closes and the data updates
    elif triggered_id["type"] == "edit_submit_button" :

        edit_data([adress, administration,kind, parking_lots,price,accessibility, connection,infrastructure],triggered_id.index)
        return(not edit_state)
    else:
        raise PreventUpdate

#---------testing------------

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
    characteristics = list(glob_vars.data.columns.values)
    #latitude and longitude not given by pop up
    non_changeable = ["lat", "lon"]

    for n in non_changeable:
        if n in characteristics:
            characteristics.remove(n)

    #modal state
    modal_state = params[-1]

    characs = params[:-1]

    assert len(characs) == len(characteristics)



    empty_ret_list = [None]

    for c in characteristics:
        empty_ret_list.append(None)


    if triggered_id == "modal_filter_cancel_button" + seitentag:
        return (0, not modal_state,) + tuple(empty_ret_list)
    elif triggered_id == "modal_filter_submit_button" + seitentag:
        reset_data()

        glob_vars.current_filter["occupancy"] = occupancy_vals

        for c, chara in zip(characs, characteristics):
            if c == None:
                glob_vars.current_filter.pop(chara, None)
                continue

            glob_vars.current_filter[chara] = c


        filter_data()
        return (1, not modal_state, occupancy_vals) + tuple(characs)
    elif triggered_id == "advanced_filter_button" + seitentag:
        characs = list(characs)

        for i in range(len(characteristics)):
            key = characteristics[i]

            characs[i] = glob_vars.current_filter[key]

        return (dash.no_update, not modal_state, glob_vars.current_filter["occupancy"]) + tuple(characs)
    else:
        raise PreventUpdate

#------
#modal add handling


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



#-----
#layout refresh callback and sidebar handling
#ANMERKUNGEN: Maybe braucht man hier keine args liste sondern kann einfach feste parameter machen? kommt drauf an wie viele parameter am ende
@callback(
    [Output("list_layout", "children"),
    Output("sideboard_name_filter" + seitentag, "value"),
    Output("sideboard_address_filter" + seitentag, "value"),
    Output("sideboard_occupancy_filter" + seitentag, "value"),
    Output("sideboard_price_filter" + seitentag, "value"),],
    [Input("placeholder_div_delete_list", "n_clicks"),
    Input("placeholder_div_filter" + seitentag, "n_clicks"),
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

    #manually write characteristics of quick filters
    sidebar_characs = ["location", "address", "occupancy", "price"]

    #num is amount of sidebar elements that are quickfilter, i.e. the last num inputs of this callback
    num = 4
    sidebar_values = args[-num:]
    # index of callback input for

    if triggered_id == "clear_filter_button" + seitentag:
        reset_data()
        reset_global_filter()
        sidebar_values = [None for x in sidebar_values]
        return (refresh_layout(),) + tuple(sidebar_values)
    elif triggered_id == "refresh_list":
        return (refresh_layout(),) + tuple(sidebar_values)
    elif triggered_id == "placeholder_div_filter" + seitentag or triggered_id == "placeholder_div_adding" + seitentag or triggered_id == "placeholder_div_delete_list":
        return (refresh_layout(),) + tuple(sidebar_values)
    else:
        #print("im in")
        reset_data()
        assert len(sidebar_characs) == len(sidebar_values)

        for s, val in zip(sidebar_characs, sidebar_values):

            if val == "":
                val = None

            glob_vars.current_filter[s] = val

        #print(glob_vars.current_filter)
        filter_data()#glob_vars.current_filter)



        return (refresh_layout(),) + tuple(sidebar_values)


def refresh_layout():
    reset_data()
    filter_data()
    names, content = create_content(glob_vars.data)

    layout = create_layout(names, content)

    return layout
