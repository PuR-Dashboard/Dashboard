# Import necessary libraries
from dash import html, dcc
from dash.dependencies import Input, Output

from App.components import sidebar
# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import map_page, list_page

# Connect the navbar to the index
from components import navbar


"""
This is the main index file to control the app layout. 
Further, it includes callback functions for the different pages of the application.
"""


nav = navbar.get_navbar()  # Create the navbar

sid = sidebar.get_sidebar()  # Create the sidebar

app.layout = html.Div([  # Create a Div containing the navbar and the content
    dcc.Location(id='url', refresh=False),  # Track current URL of the page
    nav,  # Add the navbar
    html.Div(id='page-content', children=[]),  # Add the page content
    sid  # Add the sidebar
])


@app.callback(  # Create a callback for the index page
    Output('page-content', 'children'),  # Output for the page content
    [Input('url', 'pathname')]  # Input for the current URL of the page
)
def display_page(pathname):
    """
    This function updates the content of the page based on the URL
    :param pathname:    The URL of the new page
    :return:    The new page content
    """
    if pathname == '/map_page':  # If the URL is map_page
        return map_page.layout  # Return the layout of the map page
    if pathname == '/list_page':  # If the URL is list_page
        return list_page.layout  # Return the layout of the list page
    else:  # If the URL is not map_page or list_page
        return map_page.layout  # Return the layout of the map page


# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
