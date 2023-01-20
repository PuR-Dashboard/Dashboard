import pyautogui
import os
import sys
import folium
from folium import plugins
from folium.plugins import MarkerCluster
import json
import requests
from folium_jsbutton import JsButton
import pandas as pd
from pandas import read_csv
import csv
import ctypes
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html


import branca

#Markerfunktion
#input: liste an Positionen für Marker, folium_map
def Marker(markers, folium_map, tooltips):

    for i in range (len(markers)):
        marker = markers[i]
        folium.Marker(
                    location=[marker[0], marker[1]], # coordinates for the marker (Earth Lab at CU Boulder)
                    popup=marker[2], # pop-up label for the marker
                    tooltip =tooltips[i],
                    icon=folium.Icon(color=marker[3])
                    ).add_to(folium_map)



# Bestimmung der Bildschirmgröße
def Bildschirmgroesse():

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize
    """
    Get the size of the primary monitor
    :return: width, height
    """
    #return pyautogui.size()  # Returns a tuple of (width, height)


# Popup kreiiren
# input: Name des Popup
# output: popup
def create_html(data,screensize,colors):
     result = []

     for i in range (len(data)):

         one_location_previous = data.iloc[i]
         one_location = ["not specified" if (one_location_previous[i] == None) else one_location_previous[i] for i in range (len(one_location_previous)) ]
         arrow = "&#x2B06;" if (one_location[3] == "increasing") else ("&#x2B07;" if (one_location[3] == "decreasing")else "&#x2B05;")
         html=f"""
            <!DOCTYPE html>
            <html>
            <head>
            <h1 style = "text-align: center"> {one_location[0]}</h1>
            </head>
            <body>
            <hr width="100%" size = "0.1">
             <p style = "font-size: 18px"><B><font face="Arial">Charkteristika:</font></B></p>
             <ul style="margin:0px;list-style:none ;">
                 <li style= "font-size: 15px"><B><font face="Arial">Adress:</font>     </B>&emsp;{one_location[3]}</li>
                 &thinsp;
                 <li style= "font-size: 15px"><B><font face="Arial">kind:</font> </B>&emsp;{one_location[5]}</li>
                 &thinsp;
                 <li style= "font-size: 15px"><B><font face="Arial">Number of parking lots:</font> </B>&emsp;{one_location[6]}</li>
                 &thinsp;
                 <li style= "font-size: 15px"><B><font face="Arial">price: </font></B>&emsp;{one_location[7]}</li>
                 &thinsp;
                 <li style= "font-size: 15px"><B><font face="Arial">Public transport:</font> </B>&emsp;{one_location[8]}</li>
             </ul>
            &thinsp;
             <hr width="100%" size = "0.1">

             <h2>Prognose:</h2>
             <ul style="margin:0px;list-style:none ;">
                 <li style= "font-size: 15px"> <B><font face="Arial">aktuelle Auslastung:</font></B> <font color = {colors[i]}>&emsp; high  </font>&emsp;{arrow}</li>&thinsp;

             </ul>
             </p>

            </body>
            </html>

             """

         iframe = folium.IFrame(html=html, width=screensize[0]/3, height=screensize[1]*2/4)
         popup = folium.Popup(iframe, max_width=7000)
         result.append(popup)

     return result





#Einzugsgebiete kreiiern und zum Cluster hinzufügen
# Input: liste an Positionen der Gebiete, Cluster
def create_Einzugsgebiete(gebiete,cluster):

    for gebiet in gebiete:
        circle = folium.vector_layers.Circle(location=[gebiet[0], gebiet[1]], radius=gebiet[2],color="#3186cc",
                                        fill=True,
                                        fill_color="#3186cc")
        circle.add_to(cluster)

#Knopf erstellen mit bestimmter Funktion
#Input: Funktion hinter Button
def create_Button( function):
    return JsButton(title='<i class="fas fa-crosshairs"></i>',function= function)


#Legender der Map hinzufügen
#Input: Map
def add_legend(folium_map):
    legend_html = '''
    {% macro html(this, kwargs) %}
    <div style="
        position: fixed;
        bottom: 50px;
        left: 10px;
        width: 260px;
        height: 110px;
        z-index:9999;
        font-size:14px;
        ">
        <p><a style="color: red;font-size:150%;margin-left:10px;">&diams;</a>&emsp;starke Auslastung</p>
        <p><a style="color:yellow;font-size:150%;margin-left:10px;">&diams;</a>&emsp;mittelere Auslastung</p>
        <p><a style="color:green;font-size:150%;margin-left:10px;">&diams;</a>&emsp;geringe Auslastung</p>
    </div>
    <div style="
        position: fixed;
        bottom: 50px;
        left: 10px;
        width: 175px;
        height: 110px;
        z-index:9998;
        font-size:14px;
        background-color: #ffffff;

        opacity: 0.7;
        ">
    </div>
    {% endmacro %}
    '''
    legend = branca.element.MacroElement()
    legend._template = branca.element.Template(legend_html)

    folium_map.get_root().add_child(legend)
    return folium_map



    #updaten der Map
def update(data,m):

    #data = read_csv("C:\\Users\\Marc\\Downloads\\Dashboard\\Dashboard\\Location_Data (1).csv",delimiter=',')

    screensize = Bildschirmgroesse()

    colors= ["orange" if (data.iloc[i][6] == "wenige vorhanden") else ("green" if (data.iloc[i][6] == "ausreichend vorhanden")else "red") for i in range (len(data))]
    tooltips= ["mittlere Auslastung" if (data.iloc[i][6] == "wenige vorhanden") else ("geringe Auslastung" if (data.iloc[i][6] == "ausreichend vorhanden")else "starke Auslastung") for i in range (len(data))]
    html = create_html(data, screensize,colors)
    markers = []
    for  i in range (len(data)):
        markers.append([data.iloc[i][2], data.iloc[i][1], html[i],colors[i]])

    Marker(markers,m, tooltips)

    # erstellen & visualisieren der Einzugsgebiete
    einzugsgebiete = MarkerCluster(name ='Einzugsgebiete', show = False).add_to(m)
    gebiete = []
    for i in range (len(data)):
        gebiete.append([data.iloc[i][2], data.iloc[i][1],10000])
    create_Einzugsgebiete(gebiete,einzugsgebiete)
    # Butto für die Angabe des Standortes
    folium.plugins.LocateControl().add_to(m)

    # Button für die Suche
    #folium.plugins.Search(layer = einzugsgebiete,position = 'topright').add_to(m)
    folium.LayerControl().add_to(m)
    m
    return m

def create_map(data):
    m = folium.Map(location=[51.5, 10.0], zoom_start=6.47)
    update(data,m)
    add_legend(m)
    m.save("P&R_Karte.html")

    return m



#es fehlt nur das letztendliche erstellen der Karte (s. Notebook)
