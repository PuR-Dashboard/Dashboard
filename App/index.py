# Import necessary libraries
from dash import html, dcc, ctx
from dash.dependencies import Input, Output
import dash
#from components import sidebar
# Connect to main app.py file
from app import app
import dash_bootstrap_components as dbc
# Connect to your app pages
from pages import map_page, list_page

# Connect the components to the index
from components import navbar
#from components import sidebar


"""
This is the main index file to control the app layout.
Further, it includes callback functions for the different pages of the application.
"""


nav = navbar.get_navbar()  # Create the navbar

# sid = sidebar.get_sidebar()  # Create the sidebar

app.layout = html.Div([  # Create a Div containing the navbar and the content
    dcc.Location(id='url', refresh=False),  # Track current URL of the page
    nav,  # Add the navbar
    dcc.Interval(
            id='auto_refresh_interval',
            interval=60/60 * 60/20 * 1000, #factor meaning left to right: minutes, seconds, miliseconds, current refresh rate every 60 minutes
            n_intervals=0
    ),
    html.Div(id="placeholder_interval_check", style={"display":"none"}),
    html.Div(id='page-content', children=[]),  # Add the page content
    #sid  # Add the sidebar
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


#callback to periodically refresh
@app.callback(
    Output("placeholder_interval_check", "n_clicks"),
    [Input('url', 'pathname'),
    Input("auto_refresh_interval", 'n_intervals')],
    prevent_initial_call=True
)
def testing_pls(path, a):
    ctxx = dash.callback_context
    triggered_id = ctx.triggered_id

    #parse/refresh urls/occupancy
    if triggered_id == "url":
        #dont update only because view is changed

        return a
    
    if path == "/list_page":
        #update list page layout

        pass
    elif path == "/map_page":
        #update map page layout

        pass

    #update layout

    #print(path, a)
    
    
    return a


# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
