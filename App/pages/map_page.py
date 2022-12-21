import os
import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output
from utility.map_functions import *  # Needs to stay this way to run from command line
from dash.exceptions import PreventUpdate # to avoid Update if Button is not clicked
from folium import plugins


html_list = []  # Create an empty list to store the HTML elements
print("hallo")
FA_icon = html.I(className="fa fa-refresh")  # Create an icon for the refresh button

button = (  # Create a button to refresh the list
    html.Div(  # Create a Div element
        dbc.Button(  # Create a Bootstrap button
            [FA_icon, " Refresh"],   # Create a button with the icon and the text "Refresh"
            color="light",  # Set the color of the button
            className="me-1",  # Set the class name of the button
            style={  # Set the style of the button
                "marginLeft": "93%",  # Set the left margin of the button
                "width": "7%",  # Set the width of the button
                "height": "60%",  # Set the height of the button
                "fontSize": "1em",  # Set the font size of the button
                # "background-color": "grey",  # Set the background color of the button
                "color": "black",  # Set the color of the text of the button
                # "border-radius": "4px",  # Set the border radius of the button
                # "border": "2px solid black",  # Set the border of the button
            },
        )
    )
)

html_list.append(button)  # Append the button to the list
karte = html.Div(id="karte")
html_list.append(karte)

m = create_map()  # Create the map

html_list.append(   # Append the map to the list
    html.Iframe(  # Create an Iframe element for the map
        id="karte",  # Set the id of the Iframe element
        srcDoc=open(os.path.join(os.path.dirname(__file__), '../P&R_Karte.html'), "r").read(),  # Set the source of the
        # Iframe element to be the previously created map
        width="100%",  # Set the width of the map
        height="800"  # Set the height of the map
    )
)

@callback(  # Create a callback
    Output(component_id='karte', component_property='children'),  # Set the output of the callback
    [Input(component_id='Refresh', component_property='n_clicks')]  # Set the input of the callback
)
# method to update map if refresh button is clicked
def update(nr_clicks):
    if nr_clicks == None:
        raise PreventUpdate
    m = create_map()
    return m

layout = html.Div(html_list)  # Create the layout of the app
