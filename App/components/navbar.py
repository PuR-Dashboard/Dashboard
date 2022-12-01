# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Kartenansicht", href="/map_page")),
                dbc.NavItem(dbc.NavLink("Listenansicht", href="/list_page")),
            ] ,
            brand="Park&Ride Dashboard",
            brand_href="/map_page",
            color="dark",
            dark=True,
        ), 
    ])

    return layout

 