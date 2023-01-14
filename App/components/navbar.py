# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def get_navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Map View", href="/map_page", style = {"color":"white"} )),
                dbc.NavItem(dbc.NavLink("List View", href="/list_page", style = {"color":"white"})),
            ] ,
            brand="Park&Ride Dashboard",
            brand_href="/map_page",
            color="black",
            dark=True,
        ), 
    ])

    return layout

 