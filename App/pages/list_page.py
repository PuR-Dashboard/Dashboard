import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State, MATCH, ALL
import numpy as np
from dash.exceptions import PreventUpdate
from ..utility.util_functions import *


data = get_data()  # Get DataFrame containing data stored in the Location Data csv


temp_content = data.copy(deep=True)  # Create deepcopy of data (for filtering operations)


def filter_content(df: pd.DataFrame, filter_dict: dict[str:str]):
    """
    Filter the content of the list page based on the filter
    :param df: The DataFrame containing the data
    :param filter_dict: The filter to apply
    :return: The filtered DataFrame
    """
    for f in filter_dict:  # Iterate over the filters
        df.drop(df.loc[df[f] != filter_dict[f]].index, inplace=True)  # Drop all rows which do not match the filter

    return df  # Return the filtered DataFrame


def create_content(df):
    """
    Create the content of the list page
    :param df: DataFrame containing the data of the locations
    :return: The names of the locations and the content of the list page as a tuple
    """

    cols = df.columns  # Get the columns of the DataFrame

    content = []  # Create an empty list to store the content

    names = []  # Create an empty list to store the names of the locations

    for i in range(len(df)):  # Iterate over the rows of the DataFrame

        row = df.iloc[[i]]  # Get the row

        names.append(row["location"].values[0])  # Append the name of the location to the list

        inhalt = []  # Create an empty list to store the content of the location

        for c in cols:  # Iterate over the columns of the DataFrame
            mini = str(c) + ": " + str(row[c].values[0])  # Create a string containing the column name and the value
            inhalt.append(mini)  # Append the string to the list
            inhalt.append(html.Br())  # Append a line break to the list

        content.append(inhalt)  # Append the content of the location to the list

    return names, content  # Return the names of the locations and the content of the list page as a tuple


def create_layout(names, content):
    """
    Create the layout of the list page
    :param names: The names of the locations
    :param content: The content associated with the locations
    :return: The layout of the list page
    """

    # Create dictionary which contains style information for the sidebar element
    SIDEBAR_STYLE = {
        "position": "fixed",  # Position the sidebar on the left side of the page
        "top": "4rem",  # Start the sidebar 4rem below the navbar
        "right": 0,  # Start the sidebar on the right side of the page
        "bottom": 0,  # End the sidebar at the bottom of the page
        "width": "16rem",  # Set the width of the sidebar to 16rem
        "padding": "2rem 1rem",  # Add some padding to the sidebar
        "background-color": "#f8f9fa",  # Set the background color of the sidebar to white
    }

    sidebar = html.Div(  # Create a div element for the sidebar
        [
            html.H2("Funcs", className="display-4"),  # Title of the sidebar
            html.Hr(),  # Horizontal line
            html.Button("Filter", id="filter_test", value="999"),  # Button for filtering
            html.Button("Revert", id="revert_filter_test", value="666"),  # Button for reverting the filter

            dbc.Nav(  # Group together a list of navigation links
                [
                    dbc.Button("Add", id="filter_test2", value=999),  # Button for adding a location TODO: ?
                    dbc.Button("Delete", id={"type": "test", "index": 111}),  # Button for deleting a location TODO: ?
                    html.Div(id={"type": "output", "index": 111}),  # Group content
                    dbc.Button("Delete2", id={"type": "test", "index": 222}),  # Button for deleting a location TODO: ?
                    html.Div(id={"type": "output", "index": 222}),  # Group content
                    dbc.Button("Test"),  # Button for testing TODO: ?
                ],
                vertical=True,  # Align the links vertically
                pills=True,  # Make the links look like pills
            ),
        ],
        style=SIDEBAR_STYLE,  # Apply the style information to the sidebar element
    )

    html_list = []  # Create an empty list to store the content of the list page

    for i in range(len(names)):  # Iterate over the names of the locations
        html_list.append(  # Append the card header
            dbc.CardHeader(  # Create a card header containing a button for the name of the location
                dbc.Button(  # Create a button for each location
                    names[i],  # Set the name of the location as the text of the button
                    color="outline",  # Set the color of the button to outline
                    id={"type": "header", "index": i},  # Set the id of the button to the index of the location
                    value=i  # Set the value of the button to the index of the location
                )
            )
        )
        html_list.append(  # Append the collapsible card body
            dbc.Collapse(  # Create a collapse element for the content of the location
                dbc.CardBody(content[i]),  # Create a card body containing the content of the location
                id={"type": "content", "index": i},  # Set the id of the card body to the index of the location
                is_open=False  # Set the card body to be closed by default
            )
        )

    html_list.append(sidebar)  # Append the sidebar to the list page

    return html_list  # Return the list page


def make_in_out_state(names):
    """
    Create callback inputs, outputs and states for the names of the locations
    :param names: The names of the locations
    :return: The inputs, outputs and states as a tuple
    """
    outs = [  # Create outputs for the names of the locations
        Output(  # Create an output for the content of the list page
            {"type": "content", "index": i},  # Dictionary containing metadata about the output
            "is_open"  # The name of the output
        ) for i in range(len(names))  # For each name
    ]

    ins = [  # Create inputs for the names of the locations
        Input(  # Create an input for the button of the name of the location
            {"type": "header", "index": i},  # Dictionary containing metadata about the input
            "n_clicks"  # The name of the input
        ) for i in range(len(names))  # For each name
    ]

    stats = [  # Create states for the names of the locations
        State(  # Create a state for the content of the list page
            {"type": "content", "index": i},  # Dictionary containing metadata about the state
            "is_open"  # The name of the state
        ) for i in range(len(names))  # For each name
    ]

    return outs, ins, stats  # Return the inputs, outputs and states as a tuple


names, content = create_content(data)  # Create the content of the list page


html_list_for_layout = create_layout(names, content)  # Create the layout of the list page


layout = html.Div(children=html_list_for_layout, id="page-layout")  # Create the layout using the html list and the id
# page-layout


@callback(  # Create a callback for the list page
    Output({"type": "content", "index": MATCH}, "is_open"),  # Output for the content of the list page
    [Input({"type": "header", "index": MATCH}, "n_clicks")],  # Input for the button of the name of the location
    [State({"type": "content", "index": MATCH}, "is_open")]  # State for the content of the list page
)
def toggle_collapses(butts, stats):
    """
    Toggle the collapse of the content of the list page
    :param butts: The input of the button of the name of the location
    :param stats: The state of the content of the list page
    :return: TODO
    """
    print("printing", butts, stats)  # Debugging

    ctx = dash.callback_context  # Get the callback context
        
    if not ctx.triggered:  # If the callback was not triggered
        print("Update prevented")  # Debugging
        raise PreventUpdate  # Prevent the update
    else:  # If the callback was triggered
        return not stats  # Return the opposite of the state of the content of the list page


@callback(  # Create a callback for the list page
    Output("page-layout", "children"), [Input("filter_test", "n_clicks")],  # Output for the content of the list page
    prevent_initial_call=True  # Prevent the initial call
)
def filter_buttons(n_clicks):
    """
    Filter the list page. This is temporary and will be replaced by a true implementation of filtering
    :param n_clicks: The input of the button for filtering. Currently unused
    :return: Update the layout of the list page
    """
    temp_content = filter_content(data, {"location": "Heidelberg"}) # Filter the content of the list page

    names2, content2 = create_content(temp_content)  # Create the content of the list page

    layout = create_layout(names2, content2)  # Create the layout of the list page

    return layout   # Return the layout of the list page
