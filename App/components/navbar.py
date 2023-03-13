import dash
import dash_bootstrap_components as dbc
#import dash_html_components as html
from dash import html, dcc
#from app import app
from dash.dependencies import Input, Output, State


#-------------generating icons for different buttons---------------------------
FA_icon = html.I(className="fa fa-refresh") #icon for the refresh button
FA_icon_Import = html.I(className="fa fa-upload", style={"display":"inline-block"})#icon for the upload button
FA_icon_Plus = html.I(className="fa fa-plus") #plus icon for adding a location

#-----------------------------------------------------------------------------


#-------------generating different buttons---------------------------
refr_button = (html.Div
                (dbc.Button([FA_icon, " Refresh"],
                    color="light", # color of the button
                    className="ms-2", #name of the class of the button
                    id = "refresh_page", #individuell id of the button
                    value = 0,
                    style={ # style of the button
                        "marginLeft":"10px",
                        "width": "80%",
                        "height": "40%",
                        "fontSize": "1.1em",
                        "color": "white",
                        "background-color":"transparent", #set the background color to transparent
                        "border": "transparent", #set the border color to transparent
                    },
                    )))

import_button = (html.Div
                    (dbc.Button([FA_icon_Import, " Import Location"],
                    color="light",
                    className="ms-2", #name of the class of the button
                    id = "import_button", #individuell id of the button
                    value = 0,
                      style={ # style of the button
                            "marginRight": "40px",
                            "width": "115%",
                            "height": "40%",
                            "fontSize": "1.1em",
                            "color": "white",
                            "background-color":"transparent", #set the background color to transparent
                            "border": "transparent", #set the border color to transparent
                    },
                    )))

add_location_button =  (html.Div
                         (dbc.Button([FA_icon_Plus, " Add Location"],
                         color="light",
                         className="ms-2",#name of the class of the button
                         id = "open_modal_add_location_button", #individuell id of the button
                         value = 0,
                            style={
                                    "marginRight": "40px",
                                    "width": "105%",
                                    "height": "40%",
                                    "fontSize": "1.1em",
                                    "color": "white",
                                    "background-color":"transparent", #set the background color to transparent
                                    "border": "transparent", #set the border color to transparent
                    },
                    )))

#--------------------------------------------------------------------------



# ---------------functions of the Navbar-----------------------------------
def get_navbar()-> dbc.Navbar:
    """
    This functions define a Dash layout for the navbar.

    Returns
    -------
    navbar:
        An object of the type dbc.Navbar which contains all components of the navbar.
    """
    navbar = dbc.Navbar( #defining the component is from the type Navbar
            dbc.Container(
                [ # the components are added as a container in Rows and columns
                    dbc.Row([ # concerned with the label of our Dashboard
                        dbc.Col([

                            dbc.NavbarBrand("Park&Ride Dashboard", style={"font-weight":"bold", "fontSize":"1.3em"}) # definine text which is visualized in the navbar
                        ],
                        width={"size":"auto"})
                    ],
                    align="center",
                    className="g-0"),

                    dbc.Row([ # concerned with visalizing the map page and list page button to allow a switch between those views
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink("Map View", href="/map_page",style={"color":"white","fontSize": "1.2em"})), # button for the map_page
                                dbc.NavItem(dbc.NavLink("List View", href="/list_page",style={"color":"white","fontSize": "1.2em"})), # button for the list_page
                            ],
                            navbar=True
                            )
                        ],
                        width={"size":"auto"})
                    ],
                    align="center"),
                    dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),
                     dbc.Col( # concerned with the visualization of error handeling
                           dbc.NavItem(make_import_modal(), style={"width":"10"}), # the add location through an import button
                        ),
                        dbc.Col(
                           dbc.NavItem(make_error_modal(), style={"width":"10"}),
                        ),
                        dbc.Col(
                           dbc.NavItem(html.Div(id="placeholder_error_message" , style={"display":"none","width":"10"})),
                        ),

                    dbc.Row([ # concerned with the visualization of different functionality buttons
                        dbc.Col(
                           dbc.NavItem(import_button), # import button
                        ),
                        dbc.Col(
                           dbc.NavItem(add_location_button), # add location button
                        ),
                         dbc.Col(
                           dbc.NavItem(refr_button), # the add location through an import button
                        ),
                    ],
                    align="right"),
                ],
            fluid=True
            ),
    color="#333333",
    dark=True

    )

    return navbar

def make_error_modal() -> dbc.Modal:
    """
    This functions defines a Dash Modal to show when an error occcures.

    Returns
    -------
    modal:
        A modal which contains the error warning
    """

    return dbc.Modal(  # Modal to display
                [
                    dbc.ModalHeader(dbc.ModalTitle("An Error has occured!")),  # Header of the modal
                     dbc.ModalBody(  # Body of the modal
                        [
                            dbc.Label("An error has occured while using the dashboard. Your current data is secured and you should be able to continue as usual. More information might be shown in the terminal. The origin of error is shown below:", id="error_steady_text" , style={"display":"block", "color":"black"}),
                            dbc.Label("Unidentified Error", id="modal_dynamic_error" , style={"display":"block", "color":"red"}),
                        ]
                    ),
                     dbc.ModalFooter(  # Footer of the modal
                        [
                            dbc.Button(  # Button to close the modal, changes will be discarded
                                "Okay",
                                 style = {"background-color":"#b3b3b3",
                                         "border": "black",
                                         "color": "black" # Set the color of the button to black
                                         },   # Text of the button
                                id="modal_error_ok_button"  # Set the id of the button
                            ),
                        ]
                    ),
                ],
                id="modal_error",  # Set the id of the modal
                size="lg",
                centered=True,  # Set the centered-attribute of the modal to True
            ),

def make_import_modal()-> dbc.Modal:
    """
    This functions defines a Dash layout to create new locations by importing a csv file.

    Returns
    -------
    pop_up:
        A Modal which contains all components of the visualisation of the pop up to import a csv file..
    """
    return dbc.Modal(  # Modal to display the import file option
                [
                    dbc.ModalHeader(dbc.ModalTitle("Import Files")),  # Header of the modal
                     dbc.ModalBody(  # Body of the modal
                        [
                            dcc.Upload( # style of the upload button
                                id='upload_import_files',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                multiple=True # Allow multiple files to be uploaded
                            ),
                            dbc.Label("Uploaded CSV File:",style = {"margin-top":"2%"}), # tool to upload a csv file
                            dbc.Input( # an input field where one can drop in the csv files
                                placeholder="",
                                id="modal_uploaded_csv",
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None,  # Set the value of the input field
                                disabled=True,
                                style={"background":"white"}
                            ),
                            dbc.Label("Uploaded JSON File:",style = {"margin-top":"2%"}), # tool to upload a json file
                            dbc.Input( # an input field where one can drop in the csv files
                                placeholder="",
                                id="modal_uploaded_json",
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None,  # Set the value of the input field
                                disabled=True,
                                style={"background":"white"}
                            ),
                        ]
                    ),
                     dbc.ModalFooter(  # Footer of the modal
                        [
                            # warning if error
                            html.Label("", id="modal_import_warning", style={"display":"block", "color":"red"}),
                            dbc.Button(  # Button to import and close the modal
                                "Upload",  # Text of the button
                                style = {"background-color":"#b3b3b3",
                                         "border": "black",
                                         "color": "black" # Set the color of the button to black
                                         },
                                id="modal_import_file_upload_button"# Set the id of the button
                            ),
                            dbc.Button(  # Button to close the modal, changes will be discarded
                                "Cancel",
                                 style = {"background-color":"#b3b3b3",
                                         "border": "black",
                                         "color": "black" # Set the color of the button to black
                                         },
                                id="modal_import_file_cancel_button"  # Set the id of the button
                            ),
                        ]
                    ),
                ],
                id="modal_import_file",  # Set the id of the modal
                size="lg",
                centered=True,  # Set the centered-attribute of the modal to True
            ),

#----------------------------------------------------------------------------------------
