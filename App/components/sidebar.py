# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "3.5rem",
    "right": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "black",
    "overflow": "scroll"
}

BUTTON_STYLE = {
    "width": "10rem",
    "height": "3.5rem",
   # "padding": "1.5rem 1rem",
    "text-align":"center",
    "background-color":"grey",
    "border": "grey",
    # "margin-top": "0.5rem",
    # "margin-bottom": "0.5rem",
    "color": "black"
    
}

FA_icon_Trash = html.I(className="fa fa-trash fa-lg")
FA_icon_Plus = html.I(className="fa fa-plus fa-lg")

def get_sidebar(distinction):
    """
    This function defines and returns a Dash layout for the sidebar of the application.
    :return: The layout of the sidebar of the application.
    """
    sidebar = html.Div(  # Create a div element for the sidebar
        [
           #html.H2("Funcs", className="display-4"),
            #html.Hr(),
            dbc.Nav(
                
                [
                    html.H5("Location",style={'color': 'white'}),  # Title of the navigation links
                    dbc.Input(  # Input field for the name
                        id="sideboard_name_filter" + distinction,  # Set the id of the input field to sideboard_name_filter
                        type="text",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value="",  # Set the value of the input field to an empty string
                        placeholder="Location Name",  # Set the placeholder of the input field to Location Name
                        autofocus=True,  # Set the autofocus-attribute of the input field to True
                        
                    ),
                    html.Hr(),
                    html.H5("Occupancy:",style={'color': 'white'}),  # Label for the occupancy input field
                    dbc.RadioItems(  # Radio buttons to select the occupancy
                        options=[  # Define the options of the radio buttons
                            {'label': 'High', 'value': 'red'},  # Option for high occupancy
                            {'label': 'Moderate', 'value': 'yellow'},  # Option for medium occupancy
                            {'label': 'Low', 'value': 'green'},  # Option for low occupancy
                            {'label': 'Not Specified', 'value': 'None'}  # Option for no occupancy
                        ],
                        value='None',  # Set the value of the radio buttons to None
                        inline=False,  # Set the inline-attribute of the radio buttons to False
                        id="sideboard_occupancy_filter" + distinction,  # Set the id of the radio buttons to modal_occupancy_filter
                        style={'color': 'white'}
                        
                    ),
                    html.Hr(),
                    
                    dbc.Button(  # Button to filter the locations by name
                        "Advanced",  # Text of the button
                        id="advanced_filter_button" + distinction,  # Set the id of the button to advanced_filter_button
                        value=999,  # Set the value of the button to 
                        size= "md",   
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break
                    dbc.Button(  # Button to clear the filter
                        [FA_icon_Trash, " Clear Filter"],  # Text of the button
                        id="clear_filter_button" + distinction,  # Set the id of the button to clear_filter_button
                        size= "md", 
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break
                    dbc.Button(  # Button to clear the filter
                        [FA_icon_Plus, " Add Location"],  # Text of the button
                        id="open_modal_add_location_button" + distinction,  # Set the id of the button to clear_filter_button
                        size= "md", 
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                ],
                
                vertical=True,
                pills=True,
            ),
            dbc.Modal(  # Modal to display the advanced filter
                [
                    dbc.ModalHeader("Sort by Category"),  # Header of the modal
                    dbc.ModalBody(  # Body of the modal
                        [
                            dbc.Label("Location:"),  # Label for the name input field
                            dbc.Input(
                                id="modal_name_filter" + distinction,  # Set the id of the input field to modal_name_filter
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=""  # Set the value of the input field to an empty string
                            ),
                            dbc.Label("Occupancy:"),  # Label for the occupancy input field
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
            ),
            
            dbc.Modal(  # Modal to display the advanced filter
                [
                    dbc.ModalHeader("Add Location"),  # Header of the modal
                    dbc.ModalBody(  # Body of the modal
                        [
                            dbc.Tabs(id="tabs_add_location" + distinction, active_tab="tab_add_url", children=[
                                dbc.Tab(label='Add with URL', tab_id='tab_add_url'),
                                dbc.Tab(label='Add Manually', tab_id='tab_add_manual'),
                            ]),
                            html.Div(id='tab_add_url' + distinction, children=make_url_tab(distinction), style={'display': 'block'}),
                            html.Div(id="tab_add_manual" + distinction, children=make_manual_tab(distinction), style = {'display': 'none'})
                        ]
                    ),
                    dbc.ModalFooter(  # Footer of the modal
                        [
                            dbc.Button(  # Button to close the modal
                                "Add",  # Text of the button
                                color="primary",  # Set the color of the button to primary
                                id="modal_add_location_submit_button" + distinction  # Set the id of the button to modal_submit_button
                            ),
                            dbc.Button(  # Button to cancel the modal
                                "Discard",  # Text of the button
                                id="modal_add_location_cancel_button" + distinction  # Set the id of the button to modal_cancel_button
                            ),
                        ]
                    ),
                ],
                id="modal_add_location" + distinction,  # Set the id of the modal to modal_window
                centered=True,  # Set the centered-attribute of the modal to True
            ),
        ],
       
        style=SIDEBAR_STYLE,
    )

    return sidebar  # Return the sidebar as a div element



def make_url_tab(distinction):
    html_list = []
    html_list.append(dbc.Label("URL:"))  # Label for the name input field
    html_list.append(dbc.Input(
                id="modal_add_location_url" + distinction,
                type="text",  # Set the type of the input field to text
                debounce=True,  # Set the debounce-attribute of the input field to True
                value=""  # Set the value of the input field to an empty string
            ))

    return html.Div(html_list)


def make_manual_tab(distinction):
    html_list = []
    html_list.append(dbc.Label("Location:"))  # Label for the name input field
    html_list.append(dbc.Input(
                id="modal_add_location_manual_name" + distinction,
                type="text",  # Set the type of the input field to text
                debounce=True,  # Set the debounce-attribute of the input field to True
                value=""  # Set the value of the input field to an empty string
            ))
    html_list.append(dbc.Label("Occupancy:"))
    html_list.append(dbc.RadioItems(  # Radio buttons to select the occupancy
                                options=[  # Define the options of the radio buttons
                                    {'label': 'Hoch', 'value': 'red'},  # Option for high occupancy
                                    {'label': 'Mittel', 'value': 'yellow'},  # Option for medium occupancy
                                    {'label': 'Niedrig', 'value': 'green'},  # Option for low occupancy
                                    {'label': 'Keine Angabe', 'value': 'None'}  # Option for no occupancy
                                ],
                                value='None',  # Set the value of the radio buttons to None
                                inline=False,  # Set the inline-attribute of the radio buttons to False
                                id="modal_add_location_manual_occupancy" + distinction  # Set the id of the radio buttons to modal_occupancy_filter
                            ))
                            

    return html.Div(html_list)