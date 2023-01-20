# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def get_navbar():
    """
    This function defines and returns a Dash layout for the navigation bar of the application.
    :return: A Dash layout for the navigation bar of the application.
    """
    layout = html.Div(  # Create a Div element
        [
            dbc.NavbarSimple(  # Bootstrap component which creates a simple navigation bar
                children=[  # Define the links in the navigation bar
                    dbc.NavItem(dbc.NavLink("Kartenansicht", href="/map_page")),  # Link to the map page
                    dbc.NavItem(dbc.NavLink("Listenansicht", href="/list_page")),  # Link to the table page
                ],
                brand="Park&Ride Dashboard",  # The text displayed as the brand name in the navigation bar
                brand_href="/map_page",  # The link to which the brand name redirects
                color="dark",  # The color of the navigation bar
                dark=True,  # Use the dark theme of the navigation bar
            ),
        ]
    )

    return layout  # Return the layout

 