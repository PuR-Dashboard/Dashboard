# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "3.5rem",
    "right": 0,
    "bottom": 0,
    "width": "auto",
    "padding": "2rem 1rem",
    "background-color": "#333333",
    "overflow": "scroll",


}

BUTTON_STYLE = {
    "width": "10rem",
    "height": "3.5rem",
    "text-align":"center",
    "background-color":"#b3b3b3",
    "border": "black",
    "color": "black"

}

FA_icon_Trash = html.I(className="fa fa-trash fa-lg")
FA_icon_Plus = html.I(className="fa fa-plus fa-lg")


def get_sidebar(distinction: str) -> html.Div:
    """
    This function defines and returns a Dash layout for the sidebar of the page given by the distinction.
    :return: The layout of the sidebar of the page.
    """

    sidebar = html.Div(  # Create a div element for the sidebar
        [
            #sidebar visible components
            dbc.Nav(
                [
                    html.H5("Location",style={'color': 'white'}),  # Label of the name search bar
                    dbc.Input(  # Input field for the name
                        id="sideboard_name_filter" + distinction,  # Set the id of the input field to sideboard_name_filter
                        type="text",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value=None,  # Set the value of the input field to an empty string
                        placeholder="Location Name",  # Set the placeholder of the input field to Location Name
                        autofocus=True  # Set the autofocus-attribute of the input field to True
                    ),
                    html.H5("Address",style={'color': 'white'}),  # Label of the name search bar
                    dbc.Input(  # Input field
                        id="sideboard_address_filter" + distinction,
                        type="text",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value=None,  # Set the value of the input field
                        placeholder="Address",  # Set the placeholder of the input field to Location Name
                        autofocus=False
                    ),
                    html.Hr(),
                       html.H5("Address",style={'color': 'white'}),  # Label of the name search bar
                    dbc.Input(  # Input field
                        id="sideboard_address_filter" + distinction,
                        type="text",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value=None,  # Set the value of the input field
                        placeholder="Address",  # Set the placeholder of the input field to Location Name
                        autofocus=False
                    ),
 html.Hr(),
                    html.H5("Occupancy:",style={'color': 'white'}),  # Label for the occupancy input field
                    dbc.RadioItems(  # Radio buttons to select the occupancy
                        options=[  # Define the options of the radio buttons
                                    {'label': 'High', 'value': 'high'},  # Option for high occupancy
                                    {'label': 'Medium', 'value': 'medium'},  # Option for medium occupancy
                                    {'label': 'Low', 'value': 'low'}, # Option for low occupancy
                                    {'label': 'No Filter', 'value': None}  # Option for no occupancy
                                ],
                        value=None,  # Set the value of the radio buttons to None
                        inline=False,  # Set the inline-attribute of the radio buttons to False
                        id="sideboard_occupancy_filter" + distinction,  # Set the id of the radio buttons to modal_occupancy_filter
                        style={'color': 'white'}
                    ),
                    html.Hr(),
                    html.H5("Price",style={'color': 'white'}),  # Label of the name search bar
                    dbc.Input(  # Input field
                        id="sideboard_price_filter" + distinction,
                        type="number",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value=None,  # Set the value of the input field
                        placeholder="Price",  # Set the placeholder of the input field to Location Name

                    ),
                    html.Hr(),
                    dbc.Button(  # Button to filter the locations With all filters
                        "Advanced",  # Text of the button
                        id="advanced_filter_button" + distinction,  # Set the id of the button to advanced_filter_button
                        value=999,
                        size= "md",
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break
                    dbc.Button(  # Button to clear all filters
                        [FA_icon_Trash, " Clear Filter"],  # Text of the button
                        id="clear_filter_button" + distinction,  # Set the id of the button to clear_filter_button
                        size= "md",
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break
                    dbc.Button(  # Button to add a new location
                        [FA_icon_Plus, " Add Location"],  # Text of the button
                        id="open_modal_add_location_button" + distinction,  # Set the id of the button to clear_filter_button
                        size= "md",
                        class_name= "outline-dark",
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                ],
                vertical=True, # allign elements vertically
                pills=True,
            ),
            dbc.Modal(  # Modal to display the advanced filter
                        # filters in advanced filter mostly drop down to allow multiple value filtering
                [
                    dbc.ModalHeader(dbc.ModalTitle("Filter all Categories")),  # Header of the modal
                    dbc.ModalBody(  # Body of the modal
                        [
                            dbc.Label("Name of Location:",style = {"margin-top":"2%"}), # name filter
                            dbc.Input(
                                id="modal_advanced_filter_name" + distinction, # name filter id
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                placeholder="Specify location name",
                                value=None  # Set the value of the input field to an empty string
                            ),
                           dbc.Label("Occupancy:",style = {"margin-top":"2%"}), # occupancy filter
                            dcc.Dropdown(
                                options=[ #options
                                    {'label': 'High', 'value': 'high'},
                                    {'label': 'Medium', 'value': 'medium'},
                                    {'label': 'Low', 'value': 'low'},
                                ],
                                placeholder="Specify occupancy",
                                id="modal_advanced_filter_occupancy" + distinction,
                                multi=True,
                            ),
                            dbc.Label("Address:",style = {"margin-top":"2%"}), # adress filter
                            dbc.Input(
                                id="modal_advanced_filter_address" + distinction,
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                placeholder="Specify address",
                                value=None  # Set default value
                            ),
                            dbc.Label("Administration:",style = {"margin-top":"2%"}),
                            dbc.RadioItems(  # Radio buttons to select the occupancy
                                options=[  # Define the options of the radio buttons
                                            {'label': 'Yes', 'value': 'yes'},  # Option for high occupancy
                                            {'label': 'No', 'value': 'no'},  # Option for medium occupancy
                                            {'label': 'Not Specified', 'value': None}  # Option for no occupancy
                                        ],
                                value=None,  # Set the value of the radio buttons to None
                                inline=True,  # Set the inline-attribute of the radio buttons
                                id="modal_advanced_filter_administration" + distinction  # Set the id
                            ),
                            dbc.Label("Type of Facility:",style = {"margin-top":"2%"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Car Park', 'value': 'Car Park'},
                                    {'label': 'Separate Area', 'value': 'Separate Area'},
                                    {'label': 'At the edge of the road / on the road', 'value': 'At the edge of the road / on the road'},
                                ],
                                placeholder="Specify the type of the facility",
                                id="modal_advanced_filter_kind" + distinction,
                                multi=True,
                            ),

                            dbc.Label("Number of Parking Lots:",style = {"margin-top":"2%"}), # parking lot filter(no slider like in sidebar above, this time dropdown)
                             dcc.Dropdown(
                                 options=[
                                     {'label': '1-25', 'value': '1-25'},
                                     {'label': '25-50', 'value': '25-50'},
                                     {'label': '50-100', 'value': '50-100'},
                                     {'label': '100-200', 'value': '100-200'},
                                     {'label': '200-1200', 'value': '200-1200'},
                                 ],
                                 placeholder="Specify number of parking slots",
                                 id='modal_advanced_filter_number_parking_lots' + distinction,
                                 multi=True,
                             ),
                             dbc.Label("Max. price(\u20ac):",style = {"margin-top":"2%"}),
                             dbc.Input(
                                 id="modal_advanced_filter_price" + distinction,
                                 type="number",  # Set the type of the input field to text
                                 debounce=False,  # Set the debounce-attribute of the input field to True
                                 placeholder="Price in \u20ac",
                                 value=None  # Set the value of the input field to an empty string
                             ),
                             dbc.Label("Public Transport Accessibility",style = {"margin-top":"2%"}),
                             dbc.Input(
                                 id="modal_advanced_filter_public_transport" + distinction,
                                 type="number",  # Set the type of the input field to text
                                 debounce=False,  # Set the debounce-attribute of the input field to True
                                 placeholder="Specify the public transport accessibility",
                                 value=None  # Set the value of the input field to an empty string
                             ),

                            dbc.Label("Transport Connection:",style = {"margin-top":"2%"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Superordinate network within the city (interstate)', 'value': 'Superordinate network within the city (interstate)'},
                                    {'label': 'Superordinate network out of town (interstate)', 'value': 'Superordinate network out of town (interstate)'},
                                    {'label': 'Subordinate network within the city', 'value': 'Subordinate network within the city'},
                                    {'label': 'Subordinate network out of town', 'value': 'Subordinate network out of town'},
                                ],
                                placeholder="Specify connection",
                                id="modal_advanced_filter_road_network_connection" + distinction,
                                multi=True,
                            ),


                            dbc.Label("Surrounding Infrastructure:",style = {"margin-top":"2%"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Green Spaces', 'value': 'Green Spaces'},
                                    {'label': 'Living Spaces', 'value': 'Living Spaces'},
                                    {'label': 'Industrial Areas', 'value': 'Industrial Areas'},
                                    {'label': 'Industrial Parks', 'value': 'Industrial Parks'},
                                    {'label': 'Mixed Areas', 'value': 'Mixed Areas'},
                                ],
                                placeholder="Specify surrounding infrastructure",
                                id="modal_advanced_filter_surrounding_infrastructure" + distinction,
                                multi=True,
                            ),




                        ]
                    ),
                    dbc.ModalFooter(  # Footer of the modal
                        [
                            dbc.Button(  # Button to apply the filter and close the modal
                                "Apply",  # Text of the button
                                color="primary",  # Set the color of the button to primary
                                id="modal_filter_submit_button" + distinction  # Set the id of the button to modal_submit_button
                            ),
                            dbc.Button(  # Button to discard the changes and close the the modal
                                "Discard",  # Text of the button
                                id="modal_filter_cancel_button" + distinction  # Set the id of the button to modal_cancel_button
                            ),
                        ]
                    ),
                ],
                id="modal_filter_window" + distinction,  # Set the id of the modal to modal_filter_window
                centered=True,  # Set the centered-attribute of the modal to True
            ),

            dbc.Modal(  # Modal to display the pop up for adding a location
                        # mostly uses single option dropdowns since only one value can be set per cahracteristic
                [
                    dbc.ModalHeader(dbc.ModalTitle("Add Location")),  # Header of the modal
                     dbc.ModalBody(  # Body of the modal
                        [
                            html.H4("Mandatory Fields:"), # url and location name are mandatory attributes
                            dbc.Label("URL:",style = {"margin-top":"2%"}), # url input field
                            dbc.Input(
                                placeholder="Specify the URL",
                                id="modal_add_location_url" + distinction,
                                type="text",  # Set the type of the input field
                                debounce=True,  # Set the debounce-attribute of the input field
                                value=None  # Set the value of the input field
                            ),
                            dbc.Label("Location Name:",style = {"margin-top":"2%"}), # name input field
                            dbc.Input(
                                placeholder="Specify the location name",
                                id="modal_add_location_name" + distinction,
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None  # Set the value of the input field
                            ),
                            html.H4("Optional Fields",style = {"margin-top":"5%"}), # nice to have aber none of these attributes are necessary to add location
                            dbc.Label("Address:",style = {"margin-top":"2%"}), # adress
                            dbc.Input(
                                placeholder="Specify the address",
                                id="modal_add_location_address" + distinction,
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None  # Set the value of the input field
                            ),
                            dbc.Label("Administration:",style = {"margin-top":"2%"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Yes', 'value': 'Yes'},
                                    {'label': 'No', 'value': 'No'},
                                ],
                                placeholder="Specify administration",
                                id="modal_add_location_administration" + distinction
                            ),
                            dbc.Label("Type of Facility:",style = {"margin-top":"2%"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Car Park', 'value': 'Car Park'},
                                    {'label': 'Separate Area', 'value': 'Separate Area'},
                                    {'label': 'At the edge of the road / on the road', 'value': 'At the edge of the road / on the road'},
                                ],
                                placeholder="Specify the type of the facility",
                                id="modal_add_location_kind" + distinction
                            ),

                            dbc.Label("Number of Parking Spots:",style = {"margin-top":"2%"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': '1-25', 'value': '1-25'},
                                    {'label': '25-50', 'value': '25-50'},
                                    {'label': '50-100', 'value': '50-100'},
                                    {'label': '100-200', 'value': '100-200'},
                                    {'label': '200-1200', 'value': '200-1200'},
                                ],
                                placeholder="Specify Number of parking spots",
                                id="modal_add_location_number_parking_lots" + distinction
                            ),
                            dbc.Label("Max Price:(\u20ac)",style = {"margin-top":"2%"}),
                            dbc.Input(
                                placeholder="Specify the max price in \u20ac",
                                id="modal_add_location_price" + distinction,
                                type="number",  # Set the type of the input field
                                debounce=True,  # Set the debounce-attribute of the input field
                                value=None  # Set the value of the input field
                            ),

                            dbc.Label("Public Transport Accessibility:",style = {"margin-top":"2%"}),
                            dbc.Input(
                                placeholder="Specify the public transport accessibility",
                                id="modal_add_location_public_transport" + distinction,
                                type="number",  # Set the type
                                debounce=True,  # Set the debounce-attribute
                                value=None  # Set the default value
                            ),

                            dbc.Label("Transport Connection:",style = {"margin-top":"2%"}), #connection input
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Superordinate network within the city (interstate)', 'value': 'Superordinate network within the city (interstate)'},
                                    {'label': 'Superordinate network out of town (interstate)', 'value': 'Superordinate network out of town (interstate)'},
                                    {'label': 'Subordinate network in the city', 'value': 'Subordinate network in the city'},
                                    {'label': 'Subordinate network out of town', 'value': 'Subordinate network out of town'},
                                ],
                                placeholder="Specify the transport connection",
                                id="modal_add_location_road_network_connection" + distinction
                            ),


                            dbc.Label("Surrounding Infrastructure:",style = {"margin-top":"2%"}),
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Green Spaces', 'value': 'Green Spaces'},
                                    {'label': 'Living Spaces', 'value': 'Living Spaces'},
                                    {'label': 'Industrial Areas', 'value': 'Industrial Areas'},
                                    {'label': 'Industrial Parks', 'value': 'Industrial Parks'},
                                    {'label': 'Mixed Areas', 'value': 'Mixed Areas'},
                                ],
                                placeholder="Specify the surrounding infrastructure",
                                id="modal_add_location_surrounding_infrastructure" + distinction
                            ),



                        ]
                    ),
                     dbc.ModalFooter(  # Footer of the modal
                        [
                            # warning if one of the mandatory fields is not filled out
                            dbc.Label("Fill out all mandatory fields!", id="modal_field_warning" + distinction, style={"display":"none", "color":"red"}),
                            dbc.Button(  # Button to add location and close the modal
                                "Add",  # Text of the button
                                color="primary",  # Set the color of the button to primary
                                id="modal_add_location_submit_button" + distinction  # Set the id of the button
                            ),
                            dbc.Button(  # Button to close the modal
                                "Discard",  # Text of the button
                                id="modal_add_location_cancel_button" + distinction  # Set the id of the button
                            ),
                        ]
                    ),
                ],
                id="modal_add_location" + distinction,  # Set the id of the modal
                size="lg",
                #scrollable=True,
                centered=True,  # Set the centered-attribute of the modal to True
            ),
            #placeholder div for output of advanced filter
            html.Div(id="placeholder_div_filter" + distinction, style={"display":"none"}),
            #placeholder div for output of location addition
            html.Div(id="placeholder_div_adding" + distinction, style={"display":"none"}),

        ],
        style=SIDEBAR_STYLE,
    )

    return sidebar  # Return the sidebar as a div element
