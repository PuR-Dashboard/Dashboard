import os
import dash_bootstrap_components as dbc
from dash import html, callback
from dash.dependencies import Input, Output
from utility.map_functions import *  # Needs to stay this way to run from command line
from folium import plugins


html_list = []  # Create an empty list to store the HTML elements

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
    Output(component_id='karte', component_property='karte'),  # Set the output of the callback
    [Input(component_id='Refresh', component_property='n_clicks')]  # Set the input of the callback
)
def update():
    """
    Update the map
    :return:
    """
    data = read_csv(  # Read the data from the csv file
        os.path.join(os.path.dirname(__file__), '../../Location_Data (1).csv'),  # Set the path to the csv file
        delimiter=','  # Set the delimiter of the csv file
    )

    screensize = get_screensize()  # Get the screensize

    markers = []  # Create an empty list to store the markers

    colors = []  # Create an empty list to store the colors of the markers

    tooltips = []  # Create an empty list to store the tooltips of the markers

    for i in range(len(data)):  # Iterate over the data
        colors.append(  # Append the color of the marker to the list
            "green" if data.iloc[i][6] == "wenige vorhanden"
            else "yellow" if data.iloc[i][6] == "ausreichend vorhanden"
            else "red"
        )
        tooltips.append(  # Append the tooltip of the marker to the list
            "mittlere Auslastung" if data.iloc[i][6] == "wenige vorhanden"
            else "geringe Auslastung" if data.iloc[i][6] == "ausreichend vorhanden"
            else "starke Auslastung"
        )

    # colors = ["orange"
    #           if (data.iloc[i][6] == "wenige vorhanden")
    #           else ("green"
    #                 if (data.iloc[i][6] == "ausreichend vorhanden")
    #                 else "red") for i in range(len(data))]
    #
    # tooltips = ["mittlere Auslastung"
    #             if (data.iloc[i][6] == "wenige vorhanden")
    #             else ("geringe Auslastung"
    #                   if (data.iloc[i][6] == "ausreichend vorhanden")
    #                   else "starke Auslastung") for i in range(len(data))]

    popup_html = create_popup_html(data, screensize)  # Create the HTML code for the map

    for i in range(len(data)):  # Iterate over the data
        markers.append(  # Append the marker to the list
            [
                data.iloc[i][2],  # Set the latitude of the marker
                data.iloc[i][1],  # Set the longitude of the marker
                popup_html[i],  # Set the HTML code of the marker
                colors[i],  # Set the color of the marker
                tooltips[i]  # Set the tooltip of the marker
            ]
        )

    add_markers(markers, html_list)  # Create the markers

    einzugsgebiete = MarkerCluster(  # Create the marker cluster for the "Einzugsgebiete"
        name='Einzugsgebiete',  # Set the name of the marker cluster
        show=False  # Set the default visibility of the marker cluster
    ).add_to(html_list)  # Add the marker cluster to the list

    gebiete = []  # Create an empty list to store the areas

    for i in range(len(data)):  # Iterate over the data
        gebiete.append(  # Append the area to the list
            [
                data.iloc[i][2],  # Set the latitude of the area
                data.iloc[i][1],  # Set the longitude of the area
                10000  # Set the radius of the area
            ]
        )

    create_einzugsgebiete(gebiete, einzugsgebiete)  # Create the "Einzugsgebiete"

    plugins.LocateControl().add_to(html_list)  # Add the locate-control to the list. Allows the user to locate himself
    # on the map

    plugins.Search(  # Add the search control to the list. Allows the user to search for a location on the map
        layer=einzugsgebiete,  # Set the layer to be searched
        position='topright'  # Set the position of the search control
    ).add_to(html_list)  # Add the search control to the list

    folium.LayerControl().add_to(html_list)  # Add the layer control to the list. Allows the user to show and hide the
    # marker clusters

    return html_list  # Return the list


layout = html.Div(html_list)  # Create the layout of the app
