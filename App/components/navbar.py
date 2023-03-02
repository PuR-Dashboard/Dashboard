import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash

FA_icon = html.I(className="fa fa-refresh") #icon for the refresh button
FA_icon_Import = html.I(className="fa fa-upload", style={"display":"inline-block"})#icon for the upload button


FA_icon_Plus = html.I(className="fa fa-plus")#plus icon for adding a location

#creating the refresh button
refr_button = (html.Div
                (dbc.Button([FA_icon, " Refresh"],
                    color="light", # color of the button
                    className="ms-2", #name of the class of the button
                    id = "refresh_page", #individuell id of the button
                    value = 0,
                    style={ # style of the button
                        "margin-left":"800%",
                        "width": "100%",
                        "height": "40%",
                        "fontSize": "1em",
                        "color": "white",
                        "background-color":"transparent", #set the background color to transparent
                        "border": "transparent", #set the border color to transparent
                    },
                    )))

#creating the import button
import_button = (html.Div
                    (dbc.Button([FA_icon_Import," Import Location"],
                    color="light",  # color of the button
                    className="ms-2", #name of the class of the button
                    id = "import_button",  #individuell id of the button
                    value = 0,
                      style={ # style of the button
                            "marginRight": "40px",
                            "width": "125%",
                            "height": "40%",
                            "fontSize": "1em",
                            "color": "white",
                            "background-color":"transparent", #set the background color to transparent
                            "border": "transparent", #set the border color to transparent
                    },
                    )))

#creating the import button
add_location_button =  (html.Div
                         (dbc.Button([FA_icon_Plus, " Add Location"],
                         color="light",  # color of the button
                         className="ms-2", #name of the class of the button
                         id = "open_modal_add_location_button", #individuell id of the button
                         value = 0,
                            style={ # style of the button
                                    "marginRight": "40px",
                                    "width": "105%",
                                    "height": "40%",
                                    "fontSize": "1em",
                                    "color": "white",
                                    "background-color":"transparent", #set the background color to transparent
                                    "border": "transparent", #set the border color to transparent
                    },
                    )))




def get_navbar()-> dbc.Navbar:
    """
    This functions define a Dash layout for the navbar.

    Returns
    -------
    navbar:
        An object of the type dbc.Navbar which contains all components of the navbar.
    """
    navbar = dbc.Navbar( #the cpmponent is from the type Navbar
            dbc.Container(
                [# the components are added in a container as Rows and columns
                    dbc.Row([ # this row is concerned with the label of our Dashboard
                        dbc.Col([

                            dbc.NavbarBrand("Park&Ride Dashboard", className="font-weight-bold") # defining some text which is visualized in the navbar
                        ],
                        width={"size":"auto"})
                    ],
                    align="center",
                    className="g-0"),

                    dbc.Row([ # this row is concerned with visalizing the map page and list page button to allow a switch between those views
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink("Map View", href="/map_page",style={"color":"white"})), # button for the map_page
                                dbc.NavItem(dbc.NavLink("List View", href="/list_page",style={"color":"white"})), # button for the list_page
                            ],
                            navbar=True
                            )
                        ],
                        width={"size":"auto"})
                    ],
                    align="center"),
                    dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),

                    dbc.Row([ # this row is concerned with the visualization of different functionality buttons
                        dbc.Col(
                           dbc.NavItem(import_button), # import button
                        ),
                        dbc.Col(
                           dbc.NavItem(add_location_button), # add location button
                        ),
                         dbc.Col(
                           dbc.NavItem(refr_button), # the fresh button
                        ),
                        dbc.Col(
                           dbc.NavItem(make_import_modal()), # the add location through an import button
                        )
                    ],
                    align="right"),
                ],
            fluid=True
            ),
    color="#333333",
    dark=True

    )

    return navbar



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
                            dcc.Upload(
                                id='upload_import_files',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={ # style of the upload button
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

                            dbc.Label("Uploaded CSV File:",style = {"margin-top":"2%"}), # upload of the tool to upload a csv file
                            dbc.Input( # an input field where one can drop in the csv files
                                placeholder="",
                                id="modal_uploaded_csv",
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None,  # Set the value of the input field
                                disabled=True,
                                style={"background":"white"}
                            ),
                            dbc.Label("Uploaded JSON File:",style = {"margin-top":"2%"}),# upload of the tool to upload a csv file
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
                                         },   # Text of the button
                                id="modal_import_file_cancel_button"  # Set the id of the button
                            ),
                        ]
                    ),
                ],
                id="modal_import_file",  # Set the id of the modal
                size="lg",
                #scrollable=True,
                centered=True,  # Set the centered-attribute of the modal to True
            ),
