# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {  # Define the style of the sidebar
    "position": "fixed",  # Set the position of the sidebar to be fixed
    "top": "4rem",  # Position the sidebar below the navigation bar
    "right": 0,  # Position the sidebar on the right side of the page
    "bottom": 0,  # Position the sidebar at the bottom of the page
    "width": "16rem",  # Set the width of the sidebar to 16rem
    "padding": "2rem 1rem",  # Add some padding to the sidebar
    "background-color": "#f8f9fa",  # Set the background color of the sidebar to white
    "overflow": "scroll"  # Set the overflow of the sidebar to scroll
}

BUTTON_STYLE = {  # Define the style of the buttons
    "width": "8rem",  # Set the width of the buttons to 8rem
    "height": "2rem",  # Set the height of the buttons to 2rem
    "padding": "2rem 1rem",  # Add some padding to the buttons
    "text-align": "center",  # Align the text in the buttons to the center
}


def get_sidebar():
    """
    This function defines and returns a Dash layout for the sidebar of the application.
    :return: The layout of the sidebar of the application.
    """
    sidebar = html.Div(  # Create a div element for the sidebar
        [
            html.H2(  # Title of the sidebar
                "Funcs",  # Text of the title
                className="display-4"  # Set the class of the title to display-4
            ),
            html.Hr(),  # Horizontal line
            dbc.Nav(  # Group together a list of navigation links
                [
                    html.H4("Name"),  # Title of the navigation links
                    dbc.Input(  # Input field for the name
                        id="sideboard_name_filter",  # Set the id of the input field to sideboard_name_filter
                        type="text",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value="",  # Set the value of the input field to an empty string
                        placeholder="Location Name",  # Set the placeholder of the input field to Location Name
                        autofocus=True  # Set the autofocus-attribute of the input field to True
                    ),
                    dbc.Button(  # Button to filter the locations by name
                        "Advanced",  # Text of the button
                        id="advanced_filter_button",  # Set the id of the button to advanced_filter_button
                        value=999,  # Set the value of the button to 999
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break
                    dbc.Button(  # Button to clear the filter
                        "Clear Filter",  # Text of the button
                        id="clear_filter_button",  # Set the id of the button to clear_filter_button
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break
                ],
                vertical=True,  # Set the orientation of the navigation links to vertical
                pills=True,  # Set the pills-attribute of the navigation links to True
            ),
            dbc.Modal(  # Modal to display the advanced filter
                [
                    dbc.ModalHeader("Nach Kategorie filtern"),  # Header of the modal
                    dbc.ModalBody(  # Body of the modal
                        [
                            dbc.Label("Name:"),  # Label for the name input field
                            dbc.Input(
                                id="modal_name_filter",  # Set the id of the input field to modal_name_filter
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
                                id="modal_occupancy_filter"  # Set the id of the radio buttons to modal_occupancy_filter
                            ),
                        ]
                    ),
                    dbc.ModalFooter(  # Footer of the modal
                        [
                            dbc.Button(  # Button to close the modal
                                "Apply",  # Text of the button
                                color="primary",  # Set the color of the button to primary
                                id="modal_submit_button"  # Set the id of the button to modal_submit_button
                            ),
                            dbc.Button(  # Button to cancel the modal
                                "Discard",  # Text of the button
                                id="modal_cancel_button"  # Set the id of the button to modal_cancel_button
                            ),
                        ]
                    ),
                ],
                id="modal_window",  # Set the id of the modal to modal_window
                centered=True,  # Set the centered-attribute of the modal to True
            ),
        ],
        style=SIDEBAR_STYLE,  # Set the style of the sidebar to SIDEBAR_STYLE
    )

    return html.Div([sidebar])  # Return the sidebar as a div element
