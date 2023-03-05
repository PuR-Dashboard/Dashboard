# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

#style options of the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "3.5rem",
    "right": 0,
    "bottom": 0,
    "width": "auto",
    "height": "93%",
    "padding": "2rem 1rem", #spaces between the content
    "background-color": "#333333",
    "overflow": "scroll",
}

#style of the buttons in the sidebar
BUTTON_STYLE = {
    "width": "10rem",
    "height": "3.5rem",
    "text-align":"center",
    "background-color":"#b3b3b3",
    "border": "black",
    "color": "black"
}

#trash icon for clearing all filters
FA_icon_Trash = html.I(className="fa fa-trash fa-lg")



def get_sidebar() -> html.Div:
    """
    This function defines and returns a Dash layout for the sidebar.

    Returns
    -------
    sidebar:
        The layout of the sidebar of the page including the add_location popup and the advanced filter pop up.
    """


    #documentation for the attributes of single components gets lesser the further down, since its always the same pattern
    sidebar = html.Div(  # Create a div element for the sidebar
        [
            #sidebar visible components
            dbc.Nav(
                [
                    html.H4("Filter Options",style={'color': 'white'}),
                    html.Div(html.Hr(),style={"color": "#b3b3b3"}),
                    html.H5("Location",style={'color': 'white'}),  # Label of the name search bar
                    dbc.Input(  # Input field for the name
                        id="sideboard_name_filter"  ,  # Set the id of the input field to sideboard_name_filter
                        type="text",  # Set the type of the input field to text
                        debounce=False,  # Set the debounce-attribute of the input field to False
                        value=None,  # Set the value of the input field to an empty string
                        placeholder="Location Name",  # Set the placeholder of the input field to Location Name
                        autofocus=True  # Set the autofocus-attribute of the input field to True
                    ),
                    html.Hr(), #method to leave space between elements
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
                        id="sideboard_occupancy_filter" ,  # Set the id of the radio buttons to sideboard_occupancy_filter
                        style={'color': 'white'} #style of the buttons
                    ),
                    html.Hr(),
                    html.H5("Max. Price per Day (\u20ac)",style={'color': 'white'}),  # Label of the price filter
                    dbc.Input(  # Input field
                        id="sideboard_price_filter" , #ID
                        type="number",  # Set the type of the input field to number
                        debounce=False,  # Set the debounce-attribute of the input field
                        value=None,  # Set the value of the input field
                        placeholder="Price",  # Set the placeholder of the input field

                    ),
                    html.Hr(),
                    dbc.Button(  # Button to filter the locations With all filters / open the advanced filter pop up
                        "Advanced Filter",  # Text of the button
                        id="advanced_filter_button" ,  # Set the id of the button to advanced_filter_button
                        value=999,
                        size= "md",
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Hr(),
                    dbc.Button(  # Button to clear all filters
                        [FA_icon_Trash, " Clear Filter"],  # Icon + Text of the button
                        id="clear_filter_button" ,  # Set the id of the button to clear_filter_button
                        size= "md",
                        style=BUTTON_STYLE  # Set the style of the button to BUTTON_STYLE
                    ),
                    html.Br(),  # Line break

                ],
                vertical=True, # allign elements vertically
                pills=True, # "pill" style for components
            ),
            dbc.Modal(  # Modal to display the advanced filter
                        # filters in advanced filter mostly drop down to allow multiple value filtering
                [
                    dbc.ModalHeader(dbc.ModalTitle("Filter all Categories")),  # Header of the modal
                    dbc.ModalBody(  # Body of the modal
                        [
                            dbc.Label("Name of Location:",style = {"margin-top":"2%"}), # name of the characteristic of the filter
                            dbc.Input(
                                id="modal_advanced_filter_name" , # name filter id
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                placeholder="Specify location name",
                                value=None  # Set the value of the input field
                            ),
                           dbc.Label("Occupancy:",style = {"margin-top":"2%"}), # name of the characteristic of the filter
                            dcc.Dropdown(
                                options=[ #options visalized as a dropdown
                                    {'label': 'High', 'value': 'high'},
                                    {'label': 'Medium', 'value': 'medium'},
                                    {'label': 'Low', 'value': 'low'},
                                ],
                                placeholder="Specify occupancy",  #the text which is vialized as long as nothing is choosen
                                id="modal_advanced_filter_occupancy" , # individuell id of this component
                                multi=True,#multiple values can be selected
                            ),
                            dbc.Label("Address:",style = {"margin-top":"2%"}), # adress filter
                            dbc.Input(
                                id="modal_advanced_filter_address" , # individuell id of this component
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                placeholder="Specify address", #the text which is vialized as long as nothing is choosen
                                value=None  # Set default value
                            ),
                            dbc.Label("Administration:",style = {"margin-top":"2%"}), #administration filter, no dropdown since only two options
                            dbc.RadioItems(  # Radio buttons
                                options=[  # Define the options of the radio buttons
                                            {'label': 'Yes', 'value': 'yes'},  # administration
                                            {'label': 'No', 'value': 'no'},  # no administration
                                            {'label': 'Not Specified', 'value': None}  # not specified
                                        ],
                                value=None,  # Set the value of the radio buttons to None
                                inline=True,  # Set the inline-attribute of the radio buttons
                                id="modal_advanced_filter_administration"   # Set the id
                            ),
                            dbc.Label("Type of Facility:",style = {"margin-top":"2%"}), # name of the characteristic of the filter
                            dcc.Dropdown(
                                options=[ # options of this charakteristic visalized as a dropdown
                                    {'label': 'Car Park', 'value': 'Car Park'},
                                    {'label': 'Separate Area', 'value': 'Separate Area'},
                                    {'label': 'At the edge of the road / on the road', 'value': 'At the edge of the road / on the road'},
                                ],
                                placeholder="Specify the type of the facility",#the text which is vialized as long as nothing is choosen
                                id="modal_advanced_filter_kind" , # individuell id of this component
                                multi=True, #multiple inputs are possible
                            ),

                            dbc.Label("Number of Parking Lots:",style = {"margin-top":"2%"}), # parking lot filter(no slider like in sidebar above, this time dropdown)
                             dcc.Dropdown(
                                 options=[ # options of this charakteristic visalized as a dropdown
                                     {'label': '1-25', 'value': '1-25'},
                                     {'label': '25-50', 'value': '25-50'},
                                     {'label': '50-100', 'value': '50-100'},
                                     {'label': '100-200', 'value': '100-200'},
                                     {'label': '200-1200', 'value': '200-1200'},
                                 ],
                                 placeholder="Specify number of parking slots", #the text which is vialized as long as nothing is choosen
                                 id='modal_advanced_filter_number_parking_lots' , # individuell id of this component
                                 multi=True, #multiple inputs are possible
                             ),
                             dbc.Label("Max. Price per Day (\u20ac):",style = {"margin-top":"2%"}),# name of the characteristic of the filter
                             dbc.Input(
                                 id="modal_advanced_filter_price" , # individuell id of this component
                                 type="number",  # Set the type of the input field to text
                                 debounce=False,  # Set the debounce-attribute of the input field to True
                                 placeholder="Price in \u20ac", #the text which is vialized as long as nothing is choosen
                                 value=None  # Set the value of the input field to an empty string
                             ),
                             dbc.Label("Public Transport Accessibility",style = {"margin-top":"2%"}), # name of the characteristic of the filter
                             dbc.Input(
                                 id="modal_advanced_filter_public_transport" , # individuell id of this component
                                 type="number",  # Set the type of the input field to text
                                 debounce=False,  # Set the debounce-attribute of the input field to True
                                 placeholder="Specify the public transport accessibility", #the text which is vialized as long as nothing is choosen
                                 value=None  # Set the value of the input field to an empty string
                             ),

                            dbc.Label("Transport Connection:",style = {"margin-top":"2%"}), # name of the characteristic of the filter
                            dcc.Dropdown(
                                options=[ # options of this charakteristic visalized as a dropdown
                                    {'label': 'Superordinate network within the city (interstate)', 'value': 'Superordinate network within the city (interstate)'},
                                    {'label': 'Superordinate network out of town (interstate)', 'value': 'Superordinate network out of town (interstate)'},
                                    {'label': 'Subordinate network within the city', 'value': 'Subordinate network within the city'},
                                    {'label': 'Subordinate network out of town', 'value': 'Subordinate network out of town'},
                                ],
                                placeholder="Specify connection", #the text which is visualized as long as long as nothing is choosen
                                id="modal_advanced_filter_road_network_connection" , # individuell id of this component
                                multi=True, #multiple inputs are possible
                            ),


                            dbc.Label("Surrounding Infrastructure:",style = {"margin-top":"2%"}), # name of the characteristic of the filter
                            dcc.Dropdown(
                                options=[# options of this charakteristic visalized as a dropdown
                                    {'label': 'Green Spaces', 'value': 'Green Spaces'},
                                    {'label': 'Living Spaces', 'value': 'Living Spaces'},
                                    {'label': 'Industrial Areas', 'value': 'Industrial Areas'},
                                    {'label': 'Industrial Parks', 'value': 'Industrial Parks'},
                                    {'label': 'Mixed Areas', 'value': 'Mixed Areas'},
                                ],
                                placeholder="Specify surrounding infrastructure", #the text which is visualized as long as long as nothing is choosen
                                id="modal_advanced_filter_surrounding_infrastructure" , # individuell id of this component
                                multi=True, #multiple inputs are possible
                            ),




                        ]
                    ),
                    dbc.ModalFooter(  # Footer of the modal
                        [
                            dbc.Button(  # Button to apply the filter and close the modal, will keep/save the selected filters
                                "Apply",  # Text of the button
                                color="primary",  # Set the color of the button to primary
                                id="modal_filter_submit_button"   # Set the id of the button to modal_submit_button
                            ),
                            dbc.Button(  # Button to discard the changes and close the the modal, will delete the filters
                                "Discard",  # Text of the button
                                id="modal_filter_cancel_button"   # Set the id of the button to modal_cancel_button
                            ),
                        ]
                    ),
                ],
                id="modal_filter_window" ,  # Set the id of the modal to modal_filter_window
                centered=True,  # Set the centered-attribute of the modal to True
            ),

            dbc.Modal(  # Modal to display the pop up for adding a location
                        # uses single option dropdowns since only one value can be set per cahracteristic
                [
                    dbc.ModalHeader(dbc.ModalTitle("Add Location")),  # Header of the modal
                     dbc.ModalBody(  # Body of the modal
                        [
                            html.H4("Mandatory Fields:"), # url and location name are mandatory attributes
                            dbc.Label("URL:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dbc.Input(
                                placeholder="Specify the URL", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_url" , # individuell id of this component
                                type="text",  # Set the type of the input field
                                debounce=True,  # Set the debounce-attribute of the input field
                                value=None  # Set the value of the input field
                            ),
                            dbc.Label("Location Name:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dbc.Input(
                                placeholder="Specify the location name", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_name" , # individuell id of this component
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None  # Set the value of the input field
                            ),
                            html.H4("Optional Fields",style = {"margin-top":"5%"}), # nice to have but none of these attributes are necessary to add location
                            dbc.Label("Address:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dbc.Input(
                                placeholder="Specify the address", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_address" , # individuell id of this component
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None  # Set the value of the input field
                            ),
                            dbc.Label("Administration:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dcc.Dropdown(
                                options=[ # options of this charakteristic visalized as a dropdown
                                    {'label': 'Yes', 'value': 'Yes'},
                                    {'label': 'No', 'value': 'No'},
                                ],
                                placeholder="Specify administration", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_administration" # individuell id of this component
                            ),
                            dbc.Label("Type of Facility:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dcc.Dropdown(
                                options=[ # options of this charakteristic visalized as a dropdown
                                    {'label': 'Car Park', 'value': 'Car Park'},
                                    {'label': 'Separate Area', 'value': 'Separate Area'},
                                    {'label': 'At the edge of the road / on the road', 'value': 'At the edge of the road / on the road'},
                                ],
                                placeholder="Specify the type of the facility", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_kind" # individuell id of this component
                            ),

                            dbc.Label("Number of Parking Spots:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dcc.Dropdown(
                                options=[ # options of this charakteristic visalized as a dropdown
                                    {'label': '1-25', 'value': '1-25'},
                                    {'label': '25-50', 'value': '25-50'},
                                    {'label': '50-100', 'value': '50-100'},
                                    {'label': '100-200', 'value': '100-200'},
                                    {'label': '200-1200', 'value': '200-1200'},
                                ],
                                placeholder="Specify Number of parking spots", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_number_parking_lots"
                            ),
                            dbc.Label("Max Price per Day (\u20ac):",style = {"margin-top":"2%"}),# name of the characteristic as a label
                            dbc.Input(
                                placeholder="Specify the max price in \u20ac", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_price" , # individuell id of this component
                                type="number",  # Set the type of the input field
                                debounce=True,  # Set the debounce-attribute of the input field
                                value=None  # Set the value of the input field
                            ),

                            dbc.Label("Public Transport Accessibility:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dbc.Input(
                                placeholder="Specify the public transport accessibility", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_public_transport" , # individuell id of this component
                                type="number",  # Set the type
                                debounce=True,  # Set the debounce-attribute
                                value=None  # Set the default value
                            ),

                            dbc.Label("Transport Connection:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dcc.Dropdown(
                                options=[ # options of this charakteristic visalized as a dropdown
                                    {'label': 'Superordinate network within the city (interstate)', 'value': 'Superordinate network within the city (interstate)'},
                                    {'label': 'Superordinate network out of town (interstate)', 'value': 'Superordinate network out of town (interstate)'},
                                    {'label': 'Subordinate network in the city', 'value': 'Subordinate network in the city'},
                                    {'label': 'Subordinate network out of town', 'value': 'Subordinate network out of town'},
                                ],
                                placeholder="Specify the transport connection", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_road_network_connection" # individuell id of this component
                            ),


                            dbc.Label("Surrounding Infrastructure:",style = {"margin-top":"2%"}), # name of the characteristic as a label
                            dcc.Dropdown(
                                options=[ # options of this charakteristic visalized as a dropdown
                                    {'label': 'Green Spaces', 'value': 'Green Spaces'},
                                    {'label': 'Living Spaces', 'value': 'Living Spaces'},
                                    {'label': 'Industrial Areas', 'value': 'Industrial Areas'},
                                    {'label': 'Industrial Parks', 'value': 'Industrial Parks'},
                                    {'label': 'Mixed Areas', 'value': 'Mixed Areas'},
                                ],
                                placeholder="Specify the surrounding infrastructure", #the text which is visualized as long as long as nothing is choosen
                                id="modal_add_location_surrounding_infrastructure" # individuell id of this component
                            ),



                        ]
                    ),
                     dbc.ModalFooter(  # Footer of the modal
                        [
                            # warning if one of the mandatory fields is not filled out
                            dbc.Label("Fill out all mandatory fields!", id="modal_field_warning" , style={"display":"none", "color":"red"}),
                            dbc.Button(  # Button to add location and close the modal
                                "Add",  # Text of the button
                                color="primary",  # Set the color of the button to primary
                                id="modal_add_location_submit_button"   # Set the id of the button
                            ),
                            dbc.Button(  # Button to close the modal, changes will be discarded
                                "Discard",  # Text of the button
                                id="modal_add_location_cancel_button"   # Set the id of the button
                            ),
                        ]
                    ),
                ],
                id="modal_add_location" ,  # Set the id of the modal
                size="lg",
                #scrollable=True,
                centered=True,  # Set the centered-attribute of the modal to True
            ),
            #placeholder div for signal of advanced filter
            html.Div(id="placeholder_div_filter" , style={"display":"none"}),
            #placeholder div for signal of location addition
            html.Div(id="placeholder_div_adding" , style={"display":"none"}),

        ],
        #set the style of the sidebar
        style=SIDEBAR_STYLE,
    )

    return sidebar  # Return the sidebar as a div element
