from gc import callbacks
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate
import os
from utility import map_functions
from utility.map_functions import *
from pandas import read_csv


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "4rem",
    "right": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

BUTTON_STYLE = {
    "width": "8rem",
    "height": "2rem",
    "padding": "2rem 1rem",
    "text-align":"center",
}



html_list = []

#html_list.append(html.H3("Interaktive Karte Test"))

#button for refreshing the map
FA_icon = html.I(className="fa fa-refresh")
button = (html.Div(dbc.Button([FA_icon, " Refresh"], color="light", className="me-1",
style={
                        "marginLeft": "93%",
                        "width": "7%",
                        "height": "60%",
                        "fontSize": "1em",
                       # "background-color": "grey",
                        "color": "black",
                       # "border-radius": "4px",
                       # "border": "2px solid black",
                    },
                    )))

html_list.append(button)
#----------!!!!!!!!!
# pfad zur karte manchmal weird muss vorm testen angepasst werden(also wenn was falsch läuft kann gut hier dran liegen)
m = map_functions.create_map()

#----------!!!!!!!!!
# pfad zur karte manchmal weird muss vorm testen angepasst werden(also wenn was falsch läuft kann gut hier dran liegen)
html_list.append(html.Iframe(id="karte", srcDoc=open(os.path.join(os.path.dirname(__file__), '../P&R_Karte.html'), "r").read(), width="87%", height="800"))

#html.P(id='placeholder')
@callback(Output(component_id='karte', component_property='karte'),
   [Input(component_id='Refresh', component_property='n_clicks')])

def update(nr_clicks):
   #os.path.join(os.path.dirname(__file__), '../P&R_Karte.html')
    data = read_csv(os.path.join(os.path.dirname(__file__),'../../Location_Data (1).csv'),delimiter=',')
    screensize = Bildschirmgroesse()

    markers = []
    colors= ["orange" if (data.iloc[i][6] == "wenige vorhanden") else ("green" if (data.iloc[i][6] == "ausreichend vorhanden")else "red") for i in range (len(data))]
    tooltips= ["mittlere Auslastung" if (data.iloc[i][6] == "wenige vorhanden") else ("geringe Auslastung" if (data.iloc[i][6] == "ausreichend vorhanden")else "starke Auslastung") for i in range (len(data))]
    html = create_html(data, screensize,colors)

    for  i in range (len(data)):
        markers.append([data.iloc[i][2], data.iloc[i][1], html[i],colors[i], tooltips[i]])

    Marker(markers, html_list)

    # erstellen & visualisieren der Einzugsgebiete
    einzugsgebiete = MarkerCluster(name ='Einzugsgebiete', show = False).add_to(html_list)
    gebiete = []
    for i in range (len(data)):
        gebiete.append([data.iloc[i][2], data.iloc[i][1],10000])
    create_Einzugsgebiete(gebiete,einzugsgebiete)
    # Butto für die Angabe des Standortes
    folium.plugins.LocateControl().add_to(html_list)

    # Button für die Suche
    folium.plugins.Search(layer = einzugsgebiete,position = 'topright').add_to(html_list)
    folium.LayerControl().add_to(html_list)

    return html_list




layout = html.Div(html_list)
