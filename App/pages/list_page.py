import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, ctx
from dash.dependencies import Input, Output, State, MATCH, ALL
import numpy as np
import pandas as pd
from dash.exceptions import PreventUpdate
from utility.filter_function import *
from utility.data_functions import *
from components.sidebar import get_sidebar
import plotly.express as px
import pages.global_vars as glob_vars
from collections import defaultdict
import fontstyle
from csv import reader


#----------generation of icons---------------

FA_icon_trash= html.I(className="fa fa-trash fa-lg") #icon of the deleting button
FA_icon_pen= html.I(className="fa fa-pencil fa-lg") # icon of the edditing button

#icon for button to expand list elements and arrow symbol for occupancy tendency in list view
FA_icon_Arrow = html.I(className="fa fa-chevron-down fa-lg")


#------------------------------------------



#----------generation of stylings---------------

ARR_BUTTON_STYLE = { #Define the style of the arrow button
    "color": "black", #set the arrow itself is black
    "background-color":"transparent", #set the background color to transparent
    "border": "transparent" #set the border color to transparent
}



CONTENT_STYLE = { #style the content of list_page so that it aligns with the sidebar
    "position": "fixed",
    "width": "calc(113vw - 250px)",
    "height": "calc(100vh - 50px)",
    "flex-grow": "1",
    "seamless":"True"
}

#---------------------------------------



#-----functions without a callback-----



def define_chracteristics()->list:
    """
    This functions creates a list with all current characteristics.

    Returns
    -------
    characteristics2: list
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
        characteristics2.append(row[0])

    return characteristics2


def create_security_window(location:str, index:int)-> dbc.Modal:
    """
    This function creates a pop up for the deleting function.

    Parameters
    ----------
    location:
        The name of the location which should be deleted.

    index:
        The index of the deleted location.

    Returns
    -------
    popup:
        A layout for the popup to ensure the action of deleting.
    """
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


def create_edit_window(index:int)-> dbc.Modal:
    """
    This function creates a pop up to add the data for a certain location.

    Parameters
    ----------
    index:
        The index of the edited location.

    Returns
    -------
    edit_popUp:
        A layout for the popup to edit the data of the location.
    """

    edit_popUp = dbc.Modal(  # Modal to display the advanced filter
        [
            dbc.ModalHeader("Edit",style = {"font-weight":"bold"}),# Header of the modal
            dbc.ModalBody(  # Body of the modal
                [
                    dbc.Label("Address:"),
                    dbc.Input(
                                    id={"type":"edit_address", "index":index},
                                    type="text",  # Set the type of the input field to text
                                    debounce=False,  # Set the debounce-attribute of the input field to True
                                    placeholder="edit address",
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

                    dbc.Label("Type of Facility:",style = {"margin-top":"5%", "weight":"bold"}),
                    dcc.Dropdown(
                                    options=[
                                        {'label': 'Car Park', 'value': 'Car Park'},
                                        {'label': 'Separate Area', 'value': 'Separate Area'},
                                        {'label': 'At the edge of the road / on the road', 'value': 'At the edge of the road / on the road'},
                                    ],
                                    placeholder="edit type of facility",
                                    id={"type":"edit_kind", "index":index},
                                ),

                    dbc.Label("Number of Parking spots (class):",style = {"margin-top":"5%", "weight":"bold"}),
                    dcc.Dropdown(
                        options=[
                            {'label': '1-25', 'value': '1-25'},
                            {'label': '25-50', 'value': '25-50'},
                            {'label': '50-100', 'value': '50-100'},
                            {'label': '100-200', 'value': '100-200'},
                            {'label': '200-1200', 'value': '200-1200'},
                        ],
                        placeholder="edit number of parking spots",
                        id={"type":"edit_number_parking_lots", "index":index}
                    ),

                    dbc.Label("Max. Price per Day (\u20ac):",style = {"margin-top":"5%"}),
                    dbc.Input(
                        id={"type":"edit_price", "index":index},
                        type="number",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to True
                        placeholder="edit price in \u20ac",
                        value=None  # Set the value of the input field to an empty string
                    ),

                    dbc.Label("Public Transport Accessibility:",style = {"margin-top":"5%"}),
                    dbc.Input(
                                    id={"type":"edit_public_transport", "index":index},
                                    type="text",  # Set the type of the input field to text
                                    debounce=False,  # Set the debounce-attribute of the input field to True
                                    placeholder="edit public transport accessibility",
                                    value=None  # Set the value of the input field to an empty string
                    ),

                    dbc.Label("Road Network Connection:",style = {"margin-top":"5%"}),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Superordinate network within the city (interstate)', 'value': 'Superordinate network within the city (interstate)'},
                            {'label': 'Superordinate network out of town (interstate)', 'value': 'Superordinate network out of town (interstate)'},
                            {'label': 'Subordinate network in the city', 'value': 'Subordinate network in the city'},
                            {'label': 'Subordinate network out of town', 'value': 'Subordinate network out of town'},
                        ],
                        placeholder="edit connection",
                        id={"type":"edit_road_network_connection", "index":index},
                    ),

                    dbc.Label("Surrounding Infrastructure:",style = {"margin-top":"5%"}),
                    dcc.Dropdown(
                        options=[
                            {'label': 'Green Spaces', 'value': 'Green Spaces'},
                            {'label': 'Living Spaces', 'value': 'Living Spaces'},
                            {'label': 'Industrial Areas', 'value': 'Industrial Areas'},
                            {'label': 'Industrial Parks', 'value': 'Industrial Parks'},
                            {'label': 'Mixed Areas', 'value': 'Mixed Areas'},
                        ],
                        placeholder="edit surrounding infrastructure",
                        id={"type":"edit_surrounding_infrastructure", "index":index},
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
                    #html.Div(id="placeholder_div_edit", style={"display":"none"}),

                ]
            ),
        ],
        id={"type":"edit_window", "index":index},  # Set the id of the modal to modal_window
        centered=True,  # Set the centered-attribute of the modal to True
    )
    return edit_popUp



def create_content(df: pd.DataFrame)-> tuple[list[str], list[str]]:
    """
    This function creates the names and information of the location.
    --> content of the tables

    Parameters
    ----------
    df:
        The Dataframe storring the data of the location.

    Returns
    -------
    names:
        Names of the location.

    content:
        Given Information of the location.
    """

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


def create_table(data:pd.DataFrame,content:list)->dbc.Table :
    """
    This function creates the tables for the given data.

    Parameters
    ----------
    content:
        A list of the information which should be storred in the table.

    Returns
    -------
    table_1:
        A tables which represents all the given data.
    """

    #defining the header
    table_header = [
        html.Thead(html.Tr([html.Th("Characteristics"), html.Th("Values")]), style = {"marginTop":"5%"})
    ]

    rows = [] #storing all the rows which should be visualized


    occupancy = glob_vars.occupancy # global variable saving the data of the occupancy
    one = occupancy.iloc[len(occupancy)-1] # getting the last row of the dataframe which is representing the currenct occupancys

    #adding the occupancy and the tendencyto the table
    for i in range (len(data)):

        one_location_previous = data.iloc[i] # data of one location
        one_occupancy = one[one_location_previous[0]].split(",") # the occupancy information of the locations
        this_occupancy = one_occupancy[1][:-1].replace("'", "")
        if this_occupancy == " wenige vorhanden":
            this_occupancy = "medium occupancy"
        if this_occupancy == " keine vorhanden":
            this_occupancy = "high occupancy"
        if this_occupancy == " ausreichend vorhanden":
            this_occupancy = "low occupancy"

        tendency = "increasing" if (one_occupancy[0][1:] == "'zunehmend'") else ("decreasing" if (one_occupancy[0][1:] == "'abnehmend'")else "constant")
        if content[0] == one_location_previous[0]:
            rows.append(html.Tr([html.Td("occupancy"), html.Td(this_occupancy)]))
            rows.append(html.Tr([html.Td("occupancy tendency"), html.Td(tendency)]))


    #adding the characteristics to the table
    underscored_charakter = define_chracteristics()

    #remove the underscores
    charakter = []
    for c in underscored_charakter:
        splitted_c = c.split("_")
        new_c = " ".join(splitted_c)

        if(new_c == "price"):
            new_c = "max. price per day (€)"

        if(new_c == "number parking lots"):
            new_c = "number of parking lots (class)"



        charakter.append(new_c)


    for i in range (len(charakter)):
        rows.append(html.Tr([html.Td(charakter[i], style={'font_size': '10px',}), html.Td(content[(i+3)*2], style={'font_size': '7px',})]))



    #add icons

    table_body = [html.Tbody(rows)]

    table_1 = dbc.Table(table_header + table_body, borderless=False, hover=False, style = {"width":"100%"})

    return table_1



def create_plot(content:list[str] = [1,2,3,4,5,6])-> dcc.Graph:
    """
    This function creates a plot to visualize the prediction over the week.

    Parameters
    ----------
    content:
        A list of the average occupancy for a certain day in the week.

    Returns
    -------
    graph:
        A graph which visualize the occupancy prediction for the whole week.
    """

    df = pd.DataFrame({
    "": ["Monday","Tuesday", "Wednesday", "Thursday","Friday", "WE"],
    "occupancy rate": [content[0],content[1],content[2],content[3],content[4],content[5]]
    })

    fig = px.bar(df, x="", y="occupancy rate")
    fig.add_hline(y=1,line_color="lightblue",  annotation_text="<b>high occupancy</b>")
    fig.add_hline(y=0.5,line_color="lightblue", annotation_text="<b>medium occupancy</b>")
    fig.add_hline(y=0,line_color="lightblue", annotation_text="<b>low occupancy</b>")

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



def create_history(name:str)-> list:

    """
    This method creates the average occupancy of one location over a week.

    Parameters
    -----------
    name:
        Name of the location

    Returns
    -----------
    averages:
        list of the average occupancy of each day in a week
        -> Index 0: monday
        -> Index 1: tuesday
        -> Index 2: wednesday
        -> Index 3: thursday
        -> Index 4: friday
        -> Index 5: weekend

        if there are no occupancy values, it returns a list of -1

    """

    occupancy = glob_vars.occupancy # global variable saving the data of the occupancy
    #create an array for each day of the week
    monday = []
    tuesday = []
    wednesday = []
    thursday = []
    friday =[]
    weekend = []

    #catch the case, if there are no occupancy values
    if (len(occupancy)==0):
        return [-1,-1,-1,-1,-1,-1]

    # iterate through the data
    #!!!!!!!!!!!!!!!!!!!!!! ab 21, weil da erst die neuen Occupancy daten anfangen
    for i in range (21,len(occupancy)):

        #getting the occupancy values for each row
        one = occupancy.iloc[i]

        #catch the case if the location is no given
        if one[name] == 'None':
            continue

        # split the given data format ("keine vorhanden, abnehmend") into the different single values
        splitted_one = one[name].split(",")

        #give the different string values a fitting int value to calculate the average
        value = 0 if (splitted_one[1][:-1] == " 'keine vorhanden'") else (0.5 if (splitted_one[1][:-1] == " 'wenige vorhanden'")else 1)

        #get the date
        timestamp = one["timestamp"].split(" ")
        #form it to a day of a week
        temp = pd.Timestamp(timestamp[0])
        day_of_the_week = temp.day_name()

        #sort the different values according to the weekday
        if day_of_the_week == "Saturday" or  day_of_the_week == "Sunday":
            weekend.append(value)

        elif  day_of_the_week == "Monday":
            monday.append(value)

        elif  day_of_the_week == "Tuesday":
            tuesday.append(value)

        elif  day_of_the_week == "Wednesday":
            wednesday.append(value)

        elif  day_of_the_week == "Thursday":
            thursday.append(value)

        elif  day_of_the_week == "Friday":
            friday.append(value)


        all = [monday,tuesday,wednesday,thursday,friday,weekend]
        averages = []

        #calculate the averages
        for i in range(6):


            if len(all[i]) == 0:
                averages.append(0)

            elif i == 5:
                averages.append(sum(all[i])/len(all[i]))

            else:
                averages.append(sum(all[i])/len(all[i]))




    return averages

def occupancy_function (data:pd.DataFrame, location_name) -> html.Div:
    """
    This Function returns the occupancy for one location.
    Parameters
    ----------
    data: The Dataframe storring the data of the location.
    location_name: The name of the location for which the occupancy is returned
    Returns
    -----------
    The occupancy of the location as a html.Div
    """
    result = "test"
    for i in range (len(data)):
        occupancy = glob_vars.occupancy # global variable saving the data of the occupancy
        one = occupancy.iloc[len(occupancy)-1] # getting the last row of the dataframe which is representing the currenct occupancys
        one_location_previous = data.iloc[i] # data of one location
        if location_name == one_location_previous[0]:            
            one_occupancy = one[one_location_previous[0]].split(",") # the occupancy information of the locations
            result = one_occupancy[1][:-1].replace("'", "")
            if result == " wenige vorhanden":
                result = html.Div("medium occupancy", style = {"color":"orange"})
            if result == " keine vorhanden":
                result = html.Div("high occupancy", style = {"color":"red"})
            if result == " ausreichend vorhanden":
                result = html.Div("low occupancy", style = {"color":"green"})
    return result

def create_layout(data:pd.DataFrame, names:list[str], content:list[str]) -> list:
    """
    This function dynamically creates the layout for the list_page.

    Parameters
    ----------
    names:
        A list of all names of the locations for the headlines.

    content:
        A list of the content to be represented in the collapsibles.

    Returns
    -------
    html_list:
        A list of python dash and dash.html elements representing the layout of the list_page.
    """
    #currently content is list of strings, datatype will vary in the future
    #global sid


    #init list of components
    html_list = []


    if (content == [-1,-1,-1,-1,-1,-1]):
        return None


    #iterate through names(names and content must have the same length)
    for i in range(len(names)):
        #append header of location
        html_list.append(dbc.CardHeader([dbc.Button(
                   [html.Div([ html.B(names[i]), occupancy_function(data, names[i])], style={ "text-align" : "left"})],
                    color="outline",
                    id={"type":"header", "index":i},
                    value=i,

                ), dbc.Button([FA_icon_trash, ""], id={"type":"button_control", "index":i}, className = "pull-right",style = ARR_BUTTON_STYLE),
                   dbc.Button([FA_icon_pen, ""], id={"type":"pen_button", "index" :i}, className = "pull-right" ,style = ARR_BUTTON_STYLE),
                   dbc.Button([FA_icon_Arrow, ""], id={"type":"arrow_button", "index" :i}, className = "pull-right" ,style = ARR_BUTTON_STYLE)
                   ], style = {"width":"87%"}))

                #append collapsible content
        html_list.append(dbc.Collapse(
            [
                html.Div(
                    children=[
                        dbc.Row([ #getting the table and picture next to each other
                        dbc.Col(dbc.CardBody(create_table(data, content[i]), style ={"marginRight":"auto"})),
                        dbc.Col(dbc.CardImg(src= get_image(names[i]+".jpg"), #if you want to present a picture on the listpage, just add a path to the picture by extracting it out of the excel-file
                        style ={"height":"auto", "width":"auto","marginRight":"1%", "marginLeft": "auto", "marginTop": "6%","horizontalAlign": "right"})),
                    ],
                    style ={"width": "auto", "marginLeft": "1%"}),
                    #plot directly under the table
                    dbc.CardBody(create_plot(create_history(names[i])),style ={"width": "auto","height":"auto", "color": "#F0F8FF"}),

                    ],
                style={"width":"calc(100vw - 260px)","overflow": "scroll", "height": "calc(100vh - 120px)"}
                ),
            create_edit_window(i), create_security_window(names[i], i), html.Div(id={"type":"edit_controller", "index":i}, style={"display":"none"}),
            html.Div(id={"type":"security_id_transmitter", "index":i}, style={"display":"none"}),


            ],
            id={"type":"content", "index":i},
            is_open=False,
            style={"background-color":"#e6e6e6"},

        ))
    #in case no name sare given(normally means filtering was unsuccessful)
    if len(names) == 0:
        html_list.append(html.H3("No results found!"))
        html_list.append(html.Hr())

    #html_list.append(sid)
    html_list.append(
                #placeholder div for output of location delete
                html.Div(id="placeholder_div_delete_list", style={"display":"none"}))
    html_list.append(#placeholder div for output of location edit
                    html.Div(id="placeholder_div_edit", style={"display":"none"}))
    return html_list

#create headers and content
names, content = create_content(glob_vars.data)
#create new layout
html_list_for_layout = create_layout(glob_vars.data, names, content)

layout = html.Div(children=html_list_for_layout, id="list_layout", style = CONTENT_STYLE)



def edit_data(changed_data:list[str],index:int)-> None:
    """
    This function edits the data according to the changes in the edit_window and displays the changes.

    Parameters
    ----------
    changed_data:
        A list of the values for the different chracteristics(if nothing was changed to one charachteritsics is is the old value).

    index:
        The index of the location.

    """

    temp_data = get_data("Characteristics.csv")

    characteristics = define_chracteristics()

    location = glob_vars.data.iloc[index]["location"]

    for i in range (len(temp_data)):
        if temp_data.iloc[i]["location"] == location:
            position = i
            break

    dic = {}
    array = []
    array.append(temp_data.iloc[position]["location"])
    dic["location"] =  temp_data.iloc[position]["location"]

    for i  in range(len(characteristics)):

        if changed_data[i] == None:
            array.append(np.squeeze(temp_data.iloc[position][characteristics[i]]))
            dic[characteristics[i]] = np.squeeze(temp_data.iloc[position][characteristics[i]])

        else:
            dic[characteristics[i]] = changed_data[i]
            array.append(changed_data[i])

    update_characteristics_in_csv(array)


def define_inputs_edit(special_ones:list)->list:
    """
    This function creates a list of all inputs for the callback to edit the data for a location.

    Parameters
    ----------
    special_ones:
        A list of inputs which are final.

    Returns
    -------
    inputs :
        A list of all inputs to edit the data of a location.

    """


    inputs = []

    for one in special_ones:
        inputs.append(one)

    characteristics= define_chracteristics()

    for characs in characteristics:

        inputs.append(Input({"type": "edit_"+characs, "index": MATCH}, 'value'))

    return inputs


def define_outputs_edit(special_ones:list)->list:
    """
    This function creates a list of all inputs for the callback to edit the data for a location.

    Parameters
    ----------
    special_ones:
        A list of inputs which are final.

    Returns
    -------
    outputs :
        A list of all inputs to edit the data of a location.

    """

    outputs = []

    for one in special_ones:
        outputs.append(one)

    characteristics= define_chracteristics()

    for characs in characteristics:

        outputs.append(Output({"type": "edit_"+characs, "index": MATCH}, 'value'))

    return outputs


def refresh_layout() -> list:
    """
    This function refreshed the layout by reseting the data and reapply the filters.

    Returns
    -------
    layout :
        A list with all components for the new reseted layout to display.

    """

    #filter on renewed data
    glob_vars.reset_data()
    filter_data()
    #create names and content of collapsibles
    names, content = create_content(glob_vars.data)
    #make new layout
    layout = create_layout(glob_vars.data,names, content)

    return layout

#-------------------------------------------------------

#-----------functions with Callbacks:-------------------

#callback to observe if the delete button has been pressed
#open security question window as response
@callback(
    Output({"type":"security_window", "index":MATCH}, "is_open"),
    [Input({"type":"button_control", "index":MATCH}, "n_clicks")],
    prevent_initial_call=True
)
def security_observer(_n):
    """
    This helper function opens the secruity window if the yes button for the Deleting was pressed.

    Inputs
    ----------
    _n:
        The number of clicks on the button controller.

    Outputs
    -------
    security_window:
        A boolean whether the security should be opended.
    """
    #if n_clicks is set to 0 close window
    if _n == 0:
        return False
    return True


#is necessary because in the delete_location() callback placeholder_div_delete_list cant be called due to no wildcard id(no MATCH index)
@callback(
    Output("placeholder_div_delete_list", "n_clicks"),
    [Input({"type":"security_id_transmitter", "index":ALL}, "n_clicks")],
    prevent_initial_call=True
)
def delete_observer(_n):
    """
    This helper function for the delete location function.
    It should trigger the placeholder for deleting a row.

    Inputs
    ----------
    _n:
        The number of clicks on the security id transmitter.

    Outputs
    -------
    n_clicks:
        returns 1 to trigger the trigger the update function and update the layout of the list page.

    """
    return 1


#callback to delete row from csv and give deletion confirmation to placeholder div
#checks if yes or no was pressed on security question
@callback(
    [Output({"type":"security_id_transmitter", "index":MATCH}, "n_clicks"),
    Output({"type":"button_control", "index":MATCH}, "n_clicks"),],
    [Input({"type":"security_yes_button", "index":MATCH}, "n_clicks"),
    Input({"type":"security_no_button", "index":MATCH}, "n_clicks")],
    prevent_initial_call=True,
)
def delete_location(yes, no):
    """
    This function deletes a row from csv and give deletion confirmation to placeholder div.
    Furthermore it checks if yes or no was pressed on security question and acts according to this.

    Inputs
    ----------
    yes:
        Number of clicks on the yes Button(if it was pressed)

    no:
        Number of clicks on the no Button(if it was pressed)

    Outputs
    -------
    n_clicks on the security_id_transmitter:
        Returns a number instead of dash.no_update if yes was pressed to trigger  delete obsver to update the layout.

    n_clicks on the button_control:
        always 0 to trigger the function security_observer.

    """
    #id of row to be deleted => only in currently displayed data, not necessarily global row id!!!
    triggered_id = ctx.triggered_id["index"]

    #abort if no was pressed on security button
    if ctx.triggered_id["type"] == "security_no_button":
        #dont update confirmation and 0 for closing security window
        return dash.no_update, 0

    #get location of row to delete -> to figure out position of row in global data
    row_to_delete = glob_vars.data.iloc[[triggered_id]]
    location_to_delete = row_to_delete["location"].values[0]

    remove_location(location_to_delete)

    #renew global data
    glob_vars.reset_data()
    filter_data()

    #return confirmation of deletion and second return 0 to close security window
    return 1, 0


#function to collapse and expand the list items/collapsibles
#takes all dash objects with id type content and header, and then outputs the result to the content type with matching id index
@callback(
    Output({"type": "content", "index": MATCH}, "is_open"),
    [Input({"type": "arrow_button","index": MATCH}, "n_clicks"),
     Input({"type": "header","index": MATCH}, "n_clicks")],
    [State({"type": "content", "index": MATCH}, "is_open")],
)
def toggle_collapses(_arros, _butts, stats):
    """
    This function collapses and expands the list items/collapsibles.

    Inputs
    ----------
    _arros:
        The number of clicks on the arrow button.

    _butts:
        The number of clicks on the location button.

    State
    ----------
     content:
        The current state of the collapsibles(visble or invisible).

    Outputs
    -------
    content:
        The changed state of the collapsibles(visble or invisible).
    """

    ctxx = dash.callback_context

    #if callback is not triggered by inputs dont expand
    if not ctxx.triggered:
        raise PreventUpdate
    else:
        #return opposite state of triggered button for either collapse or expand
        return not stats


#method which edits the data according to the changes in the edit_window
@callback(
    Output("placeholder_div_edit" , "n_clicks"),
    [Input({"type": "edit_controller", "index": ALL}, "is_open")]
)
def edit_window_observer(_n)-> int:
    """
    This helper function for the edit function.
    It should trigger the placeholder for refreshingthe page after editing the data.

    Inputs
    ----------
    _n:
        Whether the state of zhe edit controller changed.

    Outputs
    -------
    n_clicks:
        returns 1 to trigger the trigger the update function and update the layout of the list page.

    """

    return 1



#method to open the edit window and to close it after pressing the apply button
@callback(
    define_outputs_edit([Output({"type": "edit_window", "index": MATCH}, "is_open"),Output({"type": "edit_controller", "index": MATCH}, "is_open")]),
     define_inputs_edit([Input({"type": "pen_button", "index": MATCH}, 'n_clicks'),Input({"type": "edit_submit_button", "index": MATCH}, 'n_clicks')]),
    [State({"type": "edit_window", "index": MATCH}, "is_open")],
    prevent_initial_call=True,
)
def open_edit_window(n_clicks_edit,n_clicks_submit,*params):
#address, parking_lots, accessibility,price, infrastructure, administration,kind, connection, edit_state):

    """
    This function handels editing the data and open/close the edit window.

    Inputs
    ----------
    n_clicks_edit:
        The number of clicks on the pen-button(to open the eddit window).

    n_clicks_submit:
        The number of clicks on the submit button to change the data according to the inputs.

    address, parking_lots, accessibility,price, infrastructure, administration,kind, connection, edit_state:
        The values of the charachteritsics which should be added.

    State
    ----------
     stateedit_window:
        The current state of the edit window(visble or invisible).

    Outputs
    -------
    edit_window_is_open:
        Whether the edit window should be open/visibe.

    edit_controller_is_open:
        Whether the edit window should be open/visibe.

    """

    triggered_id = ctx.triggered_id

    #+global data
    characs = define_chracteristics()

    # if the edit button was pressed the edit window opens
    if triggered_id["type"] == "pen_button":
        row = glob_vars.data.iloc[triggered_id.index]

        display_list = []

        for c in characs:
            display_list.append(row[c])

        return (not params[-1], dash.no_update) + tuple(display_list)

    # if the apply button was pressed the edit window closes and the data updates
    elif triggered_id["type"] == "edit_submit_button" :
        none_list = [None for x in characs]
        edit_data(params[:-1],triggered_id.index)
        return (not params[-1],1) + tuple(none_list)
    else:
        raise PreventUpdate




#gets confirmation of deletion, update filter etc through placeholder, also inputs from sidebar
@callback(
    Output("list_layout", "children"),
    [Input("placeholder_div_delete_list", "n_clicks"),
    Input("placeholder_div_edit", "n_clicks"),
    Input("update_list_div", "n_clicks")],
    prevent_initial_call=True
)
def update_layout(*args):
    """
    This function updates the layout of the list page by confirmation of deletion, update filter, update edit and other placeholders.

    Inputs
    ----------
    placeholder_div_delete_list:
        A placeholder as an integer value to indicate that a location was deleted from the list and the layout should be refreshed.

    placeholder_div_edit:
        A placeholder as an integer value to indicate that a location was edit and the layout should be refreshed.

    update_list_div:
        A placeholder as an integer value to indicate that the layout should be refreshed.

    Outputs
    -------
    list_layout:
        A list of all components which will represent the new layout of page.
    """
    triggered_id = ctx.triggered_id

    return refresh_layout()

#---------------------------------------------
