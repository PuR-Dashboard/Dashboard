import dash_bootstrap_components as dbc
#import dash_html_components as html
from dash import html, dcc
#from app import app
from dash.dependencies import Input, Output, State
import dash

FA_icon = html.I(className="fa fa-refresh")
refr_button = (html.Div(dbc.Button([FA_icon, " Refresh"], color="light", className="ms-2",id = "refresh_page", value = 0,
                    style={
                        "marginRight": "0%",
                        "width": "auto",
                        "height": "40%",
                        "fontSize": "1em",
                        "color": "white",
                        "background-color":"transparent", #set the background color to transparent
                        "border": "transparent", #set the border color to transparent
                    },
                    )))


import_button = (html.Div(dbc.Button("Import Locations", color="light", className="ms-2",id = "import_button", value = 0,
                    style={
                        "marginRight": "20%",
                        "width": "auto",
                        "height": "40%",
                        "fontSize": "1em",
                        "color": "white",
                        "background-color":"transparent", #set the background color to transparent
                        "border": "transparent", #set the border color to transparent
                    },
                    )))

def get_navbar():
    navbar = dbc.Navbar(
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col([

                            dbc.NavbarBrand("Park&Ride Dashboard", className="font-weight-bold")
                        ],
                        width={"size":"auto"})
                    ],
                    align="center",
                    className="g-0"),

                    dbc.Row([
                        dbc.Col([
                            dbc.Nav([
                                dbc.NavItem(dbc.NavLink("Map View", href="/map_page",style={"color":"white"})),
                                dbc.NavItem(dbc.NavLink("List View", href="/list_page",style={"color":"white"})),
                            ],
                            navbar=True
                            )
                        ],
                        width={"size":"auto"})
                    ],
                    align="center"),
                    dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),

                    dbc.Row([
                        dbc.Col(
                           dbc.NavItem(refr_button),
                        ),
                        dbc.Col(
                           dbc.NavItem(import_button),
                        ),
                        dbc.Col(
                           dbc.NavItem(make_import_modal()),
                        )
                    ],
                    align="center"),
                ],
            fluid=True
            ),
    color="#333333",
    dark=True

    )

    return navbar



def make_import_modal():
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
                                # Allow multiple files to be uploaded
                                multiple=True
                            ),
                            dbc.Label("Uploaded CSV File:",style = {"margin-top":"2%"}),
                            dbc.Input(
                                placeholder="",
                                id="modal_uploaded_csv",
                                type="text",  # Set the type of the input field to text
                                debounce=True,  # Set the debounce-attribute of the input field to True
                                value=None,  # Set the value of the input field
                                disabled=True,
                                style={"background":"white"}
                            ),
                            dbc.Label("Uploaded JSON File:",style = {"margin-top":"2%"}),
                            dbc.Input(
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
                                color="primary",  # Set the color of the button to primary
                                id="modal_import_file_upload_button"# Set the id of the button
                            ),
                            dbc.Button(  # Button to close the modal, changes will be discarded
                                "Cancel",  # Text of the button
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