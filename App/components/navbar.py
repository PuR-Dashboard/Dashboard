import dash_bootstrap_components as dbc
#import dash_html_components as html
from dash import html
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
                        )
                    ],
                    align="center")
                ],
            fluid=True
            ),
    color="#333333",
    dark=True
    
    )

    return navbar
