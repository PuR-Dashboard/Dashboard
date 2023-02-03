import dash
import dash_bootstrap_components as dbc

import pages.global_vars as glob_vars
"""
This is the main app object. It is used to create the dash app and to run the app.
Further, it defines some external stylesheets and scripts that are used in the app.
"""
#initialise data, etc; gloabl variables
glob_vars.init()

external_stylesheets_list = [  # Define list of external stylesheets to style the Dash application
    dbc.themes.BOOTSTRAP,  # Toolkit for building responsive, mobile-first sites
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
    # Provides scalable vector icons
]
app = dash.Dash(  # Create instance of the Dash application
    __name__,  # Name of the current module. Used by Flask to find resources on the filesystem
    external_stylesheets=external_stylesheets_list,  # List of external stylesheets that are applied to the application
    meta_tags=[
        {"name": "viewport", "content": "width=device-width"}  # Set the width of the page to the width of the device
    ],
    suppress_callback_exceptions=True  # Suppress exceptions thrown in callbacks, so that the app can continue running
)



