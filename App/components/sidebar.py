# Import necessary libraries
from dash import html, dcc
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


def get_sidebar(distinction):
    """
    This function defines and returns a Dash layout for the sidebar of the application.
    :return: The layout of the sidebar of the application.
    """
    sidebar = html.Div(  # Create a div element for the sidebar
        [
            html.H2("Funcs", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
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
                                    {'label': 'Ja', 'value': 'yes'},  # Option for high occupancy
                                    {'label': 'Nein', 'value': 'no'},  # Option for medium occupancy
                                    {'label': 'Keine Angabe', 'value': None}  # Option for no occupancy
                                ],
                        value=None,  # Set the value of the radio buttons to None
                        inline=False,  # Set the inline-attribute of the radio buttons to False
                        id="sideboard_administration_filter" + distinction  # Set the id of the radio buttons to modal_occupancy_filter
                    ),
                    html.H4("Anzahl Stellplätze:"),
                    dcc.RangeSlider(min=1,max=6,step=None,id='sideboard_parking_lots_slider' + distinction, updatemode='drag',
                        marks={
                            1: '1',
                            2: '25',
                            3: '50',
                            4: '100',
                            5: '200',
                            6: "1200",
                        },
                        value=[1, 6]
                    ),
                    dbc.Input(  # Input field for the name
                        id="sideboard_slider_test" + distinction,  # Set the id of the input field to sideboard_name_filter
                        type="text",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value="",  # Set the value of the input field to an empty string
                        placeholder="Values",  # Set the placeholder of the input field to Location Name
                        autofocus=True  # Set the autofocus-attribute of the input field to True
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
                    dbc.Button(  # Button to clear the filter
                        "Add Location",  # Text of the button
                        id="open_modal_add_location_button" + distinction,  # Set the id of the button to clear_filter_button
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                ],
                vertical=True,
                pills=True,
            ),
            dbc.Modal(  # Modal to display the advanced filter
                [
                    dbc.ModalHeader("Nach Kategorie filtern"),  # Header of the modal
                    dbc.ModalBody(  # Body of the modal
                        [
                            dbc.Label("Name des Standortes:"),
                            dbc.Input(
                                id="modal_advanced_filter_name" + distinction,
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                placeholder="Stationsname",
                                value=None  # Set the value of the input field to an empty string
                            ),
                            dbc.Label("Netzanbindung:"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Übergeordnetes Netz innerorts (Bundesstraßen)', 'value': 'Übergeordnetes Netz innerorts (Bundesstraßen)'},
                                    {'label': 'Übergeordnetes Netz außerorts (Bundesstraßen)', 'value': 'Übergeordnetes Netz außerorts (Bundesstraßen)'},
                                    {'label': 'Nachgeordnetes Netz innerorts', 'value': 'Nachgeordnetes Netz innerorts'},
                                    {'label': 'Nachgeordnetes Netz außerorts', 'value': 'Nachgeordnetes Netz außerorts'},
                                ],
                                placeholder="Anbindung angeben",
                                id="modal_advanced_filter_connection" + distinction,
                                multi=True,
                            ),
                            dbc.Label("Anzahl Stellplätze:"),
                            dcc.RangeSlider(min=1,max=6,step=None,id='modal_advanced_filter_parking_lots' + distinction, updatemode='drag',
                                marks={
                                    1: '1',
                                    2: '25',
                                    3: '50',
                                    4: '100',
                                    5: '200',
                                    6: "1200",
                                },
                                value=[1, 6]
                            ),
                            dbc.Label("Bewirtschaftung:"),
                            dbc.RadioItems(  # Radio buttons to select the occupancy
                                options=[  # Define the options of the radio buttons
                                            {'label': 'Ja', 'value': 'yes'},  # Option for high occupancy
                                            {'label': 'Nein', 'value': 'no'},  # Option for medium occupancy
                                            {'label': 'Keine Angabe', 'value': None}  # Option for no occupancy
                                        ],
                                value=None,  # Set the value of the radio buttons to None
                                inline=True,  # Set the inline-attribute of the radio buttons to False
                                id="modal_advanced_filter_administration" + distinction  # Set the id of the radio buttons to modal_occupancy_filter
                            ),
                            dbc.Label("Umliegende Bebauung:"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Grünflächen', 'value': 'Grünflächen'},
                                    {'label': 'Wohnflächen', 'value': 'Wohnflächen'},
                                    {'label': 'Industrieflächen', 'value': 'Industrieflächen'},
                                    {'label': 'Gewerbegebieten', 'value': 'Gewerbegebieten'},
                                    {'label': 'Mischflächen', 'value': 'Mischflächen'},
                                ],
                                placeholder="Bebauung angeben",
                                id="modal_advanced_filter_infrastructure" + distinction,
                                multi=True,
                            ),
                            dbc.Label("Art der Parkgelegenheit:"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Parkhaus', 'value': 'Parkhaus'},
                                    {'label': 'Separate Fläche', 'value': 'Separate Fläche'},
                                    {'label': 'Am Fahrbahnrand / an der Straße', 'value': 'Am Fahrbahnrand / an der Straße'},
                                ],
                                placeholder="Bewirtschaftung angeben",
                                id="modal_advanced_filter_kind" + distinction,
                                multi=True,
                            ),
                            dbc.Label("Max Preis(\u20ac):"),
                            dbc.Input(
                                id="modal_advanced_filter_price" + distinction,
                                type="number",  # Set the type of the input field to text
                                debounce=False,  # Set the debounce-attribute of the input field to True
                                placeholder="Preis in \u20ac",
                                value=None  # Set the value of the input field to an empty string
                            ),
                            dbc.Label("Max Anzahl ÖPNV-Anbindungen:"),
                            dbc.Input(
                                id="modal_advanced_filter_num_connections" + distinction,
                                type="number",  # Set the type of the input field to text
                                debounce=False,  # Set the debounce-attribute of the input field to True
                                placeholder="Anzahl",
                                value=None  # Set the value of the input field to an empty string
                            ),
                        ]
                    ),
                    dbc.ModalFooter(  # Footer of the modal
                        [
                            dbc.Button(  # Button to close the modal
                                "Apply",  # Text of the button
                                color="primary",  # Set the color of the button to primary
                                id="modal_filter_submit_button" + distinction  # Set the id of the button to modal_submit_button
                            ),
                            dbc.Button(  # Button to cancel the modal
                                "Discard",  # Text of the button
                                id="modal_filter_cancel_button" + distinction  # Set the id of the button to modal_cancel_button
                            ),
                        ]
                    ),
                ],
                id="modal_filter_window" + distinction,  # Set the id of the modal to modal_window
                centered=True,  # Set the centered-attribute of the modal to True
            ),

            dbc.Modal(  # Modal to display the advanced filter
                [
                    dbc.ModalHeader(dbc.ModalTitle("Hinzufügen")),  # Header of the modal
                    dbc.ModalBody(  # Body of the modal
                        [
                            html.H4("Pflichtangaben"),
                            dbc.Label("URL:"),
                            dbc.Input(
                                id="modal_add_location_url" + distinction,
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None  # Set the value of the input field to an empty string
                            ),
                            dbc.Label("Name des Standortes:"),
                            dbc.Input(
                                id="modal_add_location_name" + distinction,
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None  # Set the value of the input field to an empty string
                            ),
                            html.H4("Optionale Angaben"),
                            dbc.Label("Netzanbindung:"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Übergeordnetes Netz innerorts (Bundesstraßen)', 'value': 'Übergeordnetes Netz innerorts (Bundesstraßen)'},
                                    {'label': 'Übergeordnetes Netz außerorts (Bundesstraßen)', 'value': 'Übergeordnetes Netz außerorts (Bundesstraßen)'},
                                    {'label': 'Nachgeordnetes Netz innerorts', 'value': 'Nachgeordnetes Netz innerorts'},
                                    {'label': 'Nachgeordnetes Netz außerorts', 'value': 'Nachgeordnetes Netz außerorts'},
                                ],
                                placeholder="Anbindung angeben",
                                id="modal_add_location_connection" + distinction
                            ),
                            dbc.Label("Anzahl Stellplätze:"),
                            dcc.Dropdown(
                                options=[
                                    {'label': '1-25', 'value': '1-25'},
                                    {'label': '25-50', 'value': '25-50'},
                                    {'label': '50-100', 'value': '50-100'},
                                    {'label': '100-200', 'value': '100-200'},
                                    {'label': '200-1200', 'value': '200-1200'},
                                ],
                                placeholder="Anzahl Stellplätze angeben",
                                id="modal_add_location_parking_lots" + distinction
                            ),
                            dbc.Label("Bewirtschaftung:"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Ja', 'value': 'Ja'},
                                    {'label': 'Nein', 'value': 'Nein'},
                                ],
                                placeholder="Bewirtschaftung angeben",
                                id="modal_add_location_administration" + distinction
                            ),
                            dbc.Label("Umliegende Bebauung:"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Grünflächen', 'value': 'Grünflächen'},
                                    {'label': 'Wohnflächen', 'value': 'Wohnflächen'},
                                    {'label': 'Industrieflächen', 'value': 'Industrieflächen'},
                                    {'label': 'Gewerbegebieten', 'value': 'Gewerbegebieten'},
                                    {'label': 'Mischflächen', 'value': 'Mischflächen'},
                                ],
                                placeholder="Bebauung angeben",
                                id="modal_add_location_infrastructure" + distinction
                            ),
                            dbc.Label("Art der Parkgelegenheit:"),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Parkhaus', 'value': 'Parkhaus'},
                                    {'label': 'Separate Fläche', 'value': 'Separate Fläche'},
                                    {'label': 'Am Fahrbahnrand / an der Straße', 'value': 'Am Fahrbahnrand / an der Straße'},
                                ],
                                placeholder="Bewirtschaftung angeben",
                                id="modal_add_location_kind" + distinction
                            ),
                            dbc.Label("Preis:"),
                            dbc.Input(
                                id="modal_add_location_price" + distinction,
                                type="number",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None  # Set the value of the input field to an empty string
                            ),
                            dbc.Label("Anzahl ÖPNV-Anbindungen:"),
                            dbc.Input(
                                id="modal_add_location_num_connections" + distinction,
                                type="number",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None  # Set the value of the input field to an empty string
                            ),
                        ]
                    ),
                    dbc.ModalFooter(  # Footer of the modal
                        [
                            dbc.Label("Alle Pflichtfelder Ausfüllen!", id="modal_field_warning" + distinction, style={"display":"none", "color":"red"}),
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
                size="lg",
                #scrollable=True,
                centered=True,  # Set the centered-attribute of the modal to True
            ),
            #placeholder div for output
            html.Div(id="placeholder_div" + distinction, style={"display":"none"})

        ],
        style=SIDEBAR_STYLE,
    )

    return sidebar  # Return the sidebar as a div element


