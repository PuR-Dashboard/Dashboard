# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "4rem",
    "right": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

BUTTON_STYLE = {
    "width": "8rem",
    "height": "2rem",
    "padding": "2rem 1rem",
    "text-align":"center",
}


<<<<<<< Updated upstream
def Sidebar():
    sidebar = html.Div(
=======
def get_sidebar(distinction):
    """
    This function defines and returns a Dash layout for the sidebar of the application.
    :return: The layout of the sidebar of the application.
    """
    sidebar = html.Div(  # Create a div element for the sidebar
>>>>>>> Stashed changes
        [
            html.H2("Funcs", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
<<<<<<< Updated upstream
                    html.H4("Name"),
                    dbc.Input(id="sideboard_name_filter", type="text", debounce=False, value="", placeholder="Location Name", autofocus=True),
                    dbc.Button("Advanced", id="advanced_filter_button", value=999, style=BUTTON_STYLE),
                    html.Br(),
                    dbc.Button("Clear Filter", id="clear_filter_button",style=BUTTON_STYLE),
                    html.Br(),
=======
                    html.H4("Name"),  # Title of the navigation links
                    dbc.Input(  # Input field for the name
                        id="sideboard_name_filter" + distinction,  # Set the id of the input field to sideboard_name_filter
                        type="text",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value="",  # Set the value of the input field to an empty string
                        placeholder="Location Name",  # Set the placeholder of the input field to Location Name
                        autofocus=True  # Set the autofocus-attribute of the input field to True
                    ),
                    html.H4("Auslastung:"),  # Label for the occupancy input field
                    dbc.RadioItems(  # Radio buttons to select the occupancy
                        options=[  # Define the options of the radio buttons
                            {'label': 'Hoch', 'value': 'red'},  # Option for high occupancy
                            {'label': 'Mittel', 'value': 'yellow'},  # Option for medium occupancy
                            {'label': 'Niedrig', 'value': 'green'},  # Option for low occupancy
                            {'label': 'Keine Angabe', 'value': 'None'}  # Option for no occupancy
                        ],
                        value='None',  # Set the value of the radio buttons to None
                        inline=False,  # Set the inline-attribute of the radio buttons to False
                        id="sideboard_occupancy_filter" + distinction  # Set the id of the radio buttons to modal_occupancy_filter
                    ),
                    dbc.Button(  # Button to filter the locations by name
                        "Advanced",  # Text of the button
                        id="advanced_filter_button" + distinction,  # Set the id of the button to advanced_filter_button
                        value=999,  # Set the value of the button to 999
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break
                    dbc.Button(  # Button to clear the filter
                        "Clear Filter",  # Text of the button
                        id="clear_filter_button" + distinction,  # Set the id of the button to clear_filter_button
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break
>>>>>>> Stashed changes
                ],
                vertical=True,
                pills=True,
            ),
<<<<<<< Updated upstream
            dbc.Modal(
            [
                dbc.ModalHeader("Nach Kategorie filtern"),
                dbc.ModalBody(
                    [
                        dbc.Label("Name:"),
                        dbc.Input(id="modal_name_filter", type="text", debounce=True, value=""),
                        dbc.Label("Auslastung:"),
                        dbc.RadioItems(
                            options=[
                            {'label': 'Hoch', 'value': 'red'}, 
                            {'label': 'Mittel', 'value': 'yellow'}, 
                            {'label': 'Niedrig', 'value': 'green'}, 
                            {'label': 'Keine Angabe', 'value': 'None'}
                            ],
                            value='None',
                            inline=False,
                            id="modal_occupancy_filter"
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Apply", color="primary", id="modal_submit_button"),
                        dbc.Button("Discard", id="modal_cancel_button"),
                    ]
                ),
            ],
            id="modal_window",
            centered=True,
=======
            dbc.Modal(  # Modal to display the advanced filter
                [
                    dbc.ModalHeader("Nach Kategorie filtern"),  # Header of the modal
                    dbc.ModalBody(  # Body of the modal
                        [
                            dbc.Label("Name:"),  # Label for the name input field
                            dbc.Input(
                                id="modal_name_filter" + distinction,  # Set the id of the input field to modal_name_filter
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=""  # Set the value of the input field to an empty string
                            ),
                            dbc.Label("Auslastung:"),  # Label for the occupancy input field
                            dbc.RadioItems(  # Radio buttons to select the occupancy
                                options=[  # Define the options of the radio buttons
                                    {'label': 'Hoch', 'value': 'red'},  # Option for high occupancy
                                    {'label': 'Mittel', 'value': 'yellow'},  # Option for medium occupancy
                                    {'label': 'Niedrig', 'value': 'green'},  # Option for low occupancy
                                    {'label': 'Keine Angabe', 'value': 'None'}  # Option for no occupancy
                                ],
                                value='None',  # Set the value of the radio buttons to None
                                inline=False,  # Set the inline-attribute of the radio buttons to False
                                id="modal_occupancy_filter" + distinction  # Set the id of the radio buttons to modal_occupancy_filter
                            ),
                        ]
                    ),
                    dbc.ModalFooter(  # Footer of the modal
                        [
                            dbc.Button(  # Button to close the modal
                                "Apply",  # Text of the button
                                color="primary",  # Set the color of the button to primary
                                id="modal_submit_button" + distinction  # Set the id of the button to modal_submit_button
                            ),
                            dbc.Button(  # Button to cancel the modal
                                "Discard",  # Text of the button
                                id="modal_cancel_button" + distinction  # Set the id of the button to modal_cancel_button
                            ),
                        ]
                    ),
                ],
                id="modal_window" + distinction,  # Set the id of the modal to modal_window
                centered=True,  # Set the centered-attribute of the modal to True
>>>>>>> Stashed changes
            ),
        ],
        style=SIDEBAR_STYLE,
    )

<<<<<<< Updated upstream
    return html.Div([sidebar])
=======
    return sidebar  # Return the sidebar as a div element
>>>>>>> Stashed changes
