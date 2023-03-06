import os
import sys
import folium
from folium import plugins
from folium.plugins import MarkerCluster
import json
import requests
import pandas as pd
from pandas import read_csv
import csv
import ctypes
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import branca
from utility.data_functions import *
import pages.global_vars as glob_vars



def marker(markers:list, folium_map:folium.Map, tooltips)-> None:
    """
    This function visualises the given markers on the given map.

    Parameters
    ----------
    markers : list of markers
        The list of markers which should be visualized.

    folium_map:
        The map on which the marrkers should be presented.

    tooltips: list of tooltips:
        Contains a tooltip for each marker.
    """

    #adding all marker which should be visualized
    for i in range (len(markers)):
        marker = markers[i]
        folium.Marker(
                    location=[marker[0], marker[1]], # coordinates for the marker (Earth Lab at CU Boulder)
                    popup=marker[2], # pop-up label for the marker
                    tooltip =tooltips[i],# tool tip of each marker
                    icon=folium.Icon(color=marker[3])# defining the color of the marker according to the occupancy of the location
                    ).add_to(folium_map)# adding the designed marker to the folium map




def screensize()-> list:
    """
    Get the size of the primary monitor
    Returns
    -------
    width and height of the screen
    """
    return (1920, 1080)  # Returns a tuple of (width, height)


def create_html(data:pd.DataFrame,screensize:list ,colors:list)->list :
    """
    This function creates the pop-up for all markers/locations.

    Parameters
    ----------
    data : csv
        The data which should be visualized

    screensize: list of Integer
        The size to which the pop up window should be adjusted.

    colors: list of strings
        Contains the occupancy as a color representation.

    Returns
    -------
    result: list of folium.Popup
        Contains all Pop ups for all markers.
    """

    result = []
    occupancy = glob_vars.occupancy # global variable saving the data of the occupancy


    one = occupancy.iloc[len(occupancy)-1] # getting the last row of the dataframe which is representing the currenct occupancys
    


    # creating for each marker the pop up according to the saved information about this location
    for i in range (len(data)):

        one_location_previous = data.iloc[i] # data about one location
        one_occupancy = one[one_location_previous[0]].split(",") # the occupancy information of the locations

        # all charakteristics which are not specified yet(a corresponding visuell description)
        one_location = ["not specified" if (one_location_previous[i] == None) else one_location_previous[i] for i in range (len(one_location_previous)) ]

        # choosing the right arrow according to the tendency of the occupancy
        arrow = "&#x2B06;" if (one_occupancy[0][1:] == "zunehmend") else ("&#x2B07;" if (one_occupancy[0][1:] == "abnehmend")else "&#x2B05;")

        # creating the HTML for one certain location
        html=f"""
            <!DOCTYPE html>
            <html>
                   <head>
                   <h1 style = "text-align: center"><font face="Arial"> {data.iloc[i]["location"]}</font></h1>
                   </head>
                   <body>

                    <p style = "font-size: 18px"><B><u><font face="Arial">Characteristics:</font></u></B></p>
                   <ul>
                       <li style= "font-size: 15px"><B><font face="Arial">Address:</B></font></B></font><font face="Arial">&emsp; {data.iloc[i]["address"]}</font></li>&thinsp;
                       <li style= "font-size: 15px"> <B><font face="Arial">Number of Parking Lots: </font></B></font><font face="Arial">&emsp;{data.iloc[i]["number_parking_lots"]}</font></li>&thinsp;
                       <li style= "font-size: 15px"> <B><font face="Arial">Type of Facility:</font></B></font><font face="Arial">&emsp;{data.iloc[i]["kind"]}</font></li>&thinsp;
                       <li style= "font-size: 15px"> <B><font face="Arial">Public Transport Connections: </font></B></font><font face="Arial">&emsp;{data.iloc[i]["public_transport"]}</font></li>&thinsp;
                       <li style= "font-size: 15px"> <B><font face="Arial">Current Occupancy:</font></B> <font color = {colors[i]}>&emsp; {one_occupancy[1][:-1]}  </font>&emsp;{arrow}</li>&thinsp;
                   </ul>

                       <table style= "border:1px solid black; background-color:#E3EFFA; text-align:center; font-size: 14px; width:100%; height:100%">
                       <caption style= "text-align:center"> <B style= "font-size: 18px"><font face="Arial">Occupancy History Of The Week</font></B> </caption>
                        &thinsp;
                       <tr>
                           <th height=30 style=" border-bottom: 1px solid black; border-right: 1px solid black;"><font face="Arial">Monday</font></th>
                           <th  style=" border-bottom: 1px solid black;border-right: 1px solid black;"><font face="Arial">Tuesday</font></th>
                           <th  style=" border-bottom: 1px solid black;border-right: 1px solid black;"><font face="Arial">Wednesday</font></th>
                           <th  style=" border-bottom: 1px solid black;border-right: 1px solid black;"><font face="Arial">Thursday</font></th>
                           <th  style=" border-bottom: 1px solid black;border-right: 1px solid black;"><font face="Arial">Friday</font></th>
                           <th  style=" border-bottom: 1px solid black;border-right: 1px solid black;"><font face="Arial">Saturday</font></th>
                           <th  style=" border-bottom: 1px solid black;"><font face="Arial">Sunday</font></th>
                       </tr>
                       &thinsp;
                       <tr>
                       <td style = "border-right: 1px solid black;"><font face="Arial"> <font color = {colors[i]}>&emsp; {one_location[6]}  </font>&emsp;{arrow}</li></font></td>
                       <td style = "border-right: 1px solid black;"><font face="Arial"> <font color = {colors[i]}>&emsp; {one_location[6]}  </font>&emsp;{arrow}</li></font></td>
                       <td style = "border-right: 1px solid black;"><font face="Arial"> <font color = {colors[i]}>&emsp; {one_location[6]}  </font>&emsp;{arrow}</li></font></td>
                       <td style = "border-right: 1px solid black;"><font face="Arial"> <font color = {colors[i]}>&emsp; {one_location[6]}  </font>&emsp;{arrow}</li></font></td>
                       <td style = "border-right: 1px solid black;"><font face="Arial"> <font color = {colors[i]}>&emsp; {one_location[6]}  </font>&emsp;{arrow}</li></font></td>
                       <td style = "border-right: 1px solid black;"><font face="Arial"> <font color = {colors[i]}>&emsp; {one_location[6]}  </font>&emsp;{arrow}</li></font></td>
                       <td><font face="Arial"> <font color = {colors[i]}>&emsp; {one_occupancy[1]}  </font>&emsp;{arrow}</li></font></td>
                       </tr>
                       </table>


                   </p>
                   </body>
           </html>
             """

        iframe = folium.IFrame(html=html, width=screensize[0]/3, height=screensize[1]/2)# trandforming the html file in a IFrame dynamic to the size of the screen
        popup = folium.Popup(iframe, max_width=7000)# creating the pop up based on the iframe
        result.append(popup)

    return result



def define_radius(radius= 0)-> int:
    """
    This function returns the radius of the draw area.

    Parameters
    ----------
    radius : int
        The size of the radius.
        (If none is given, the radius is zero)

    Returns
    -------
    radius: int
    """

    return radius



def create_drawarea(regions: list,cluster: MarkerCluster)-> None:
    """
    This function creates the draw areas for all markers.

    Parameters
    ----------
    regions : list of locations

    cluster:
        Component to cluster the draw areas in the visualization.
    """

    for r in regions:
        circle = folium.vector_layers.Circle(# creating a circle for each location representing the drawing area
                                        location=[r[0], r[1]], radius=r[2],
                                        color="#3186cc",
                                        fill=True,
                                        fill_color="#3186cc")
        circle.add_to(cluster)# adding the circle to the cluster which saves al the draw areas for all locations



def add_legend(folium_map:folium.Map)-> folium.Map:
    """
    This function adds a legend to the given map.

    Parameters
    ----------
    folium_map :
        The map which will be visualized.

    Returns
    -------
    folium_map:
        The map with the added legend.
    """

    # creating the legend as a HTML
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
        <p><a style="color: red;font-size:150%;margin-left:10px;">&diams;</a>&emsp;high occupancy</p>
        <p><a style="color:gold;font-size:150%;margin-left:10px;">&diams;</a>&emsp;medium occupancy</p>
        <p><a style="color:green;font-size:150%;margin-left:10px;">&diams;</a>&emsp;low occupancy</p>
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

    legend = branca.element.MacroElement() # creating a MacroElement
    legend._template = branca.element.Template(legend_html) # adding the legend_html to the MacroElement

    folium_map.get_root().add_child(legend) # adding the MacroElement to the folium map

    return folium_map



def update(data:pd.DataFrame,m:folium.Map)-> folium.Map:
    """
    This function updates the given map according to potential changes in the data.
    Creates all the components of the map.

    Parameters
    ----------
    data: Panda DataFrame
        The data which should be visualized.

    m: Folium.map
        The map which should be updated.

    Returns
    -------
    folium_map:
        The updated map.
    """

    #calculating the screensize of the current screen
    ss = screensize()

    occupancy = glob_vars.occupancy # getting the occupancies

    one = occupancy.iloc[len(occupancy)-1]# only the last row is interesting for us because it stores the current occupancy

    # defining the colors of the markers according to the current occupancy
    colors= ["orange" if (one[data.iloc[i][0]].split(",")[1][:-1] == " 'wenige vorhanden'") else ("green" if (one[data.iloc[i][0]].split(",")[1][:-1] == " 'ausreichend vorhanden'")else "red") for i in range (len(data))]

    # defining the tooltips of the markers according to the current occupancy
    tooltips= ["medium occupancy" if (one[data.iloc[i][0]].split(",")[1][:-1]== " 'wenige vorhanden'") else ("low occupancy" if (one[data.iloc[i][0]].split(",")[1][:-1] == " 'ausreichend vorhanden'")else "high occupancy") for i in range (len(data))]

    #creating the pop ups for all the markers
    html = create_html(data, ss,colors)

    #appending the markers on the map
    markers = []
    for  i in range (len(data)):
        markers.append([data.iloc[i][2], data.iloc[i][1], html[i],colors[i]])
    marker(markers,m, tooltips)

    # creating and adding the draw areas of the locations
    drawAreas = MarkerCluster(name ='Einzugsgebiete', show = False).add_to(m) # cluster to safe all the draw areas
    areas = []
    for i in range (len(data)):
        areas.append([data.iloc[i][2], data.iloc[i][1],define_radius()])
    create_drawarea(areas,drawAreas)

    #adding the layer Controler for the draw areas to the map
    folium.LayerControl().add_to(m)

    # button for the current location of the user
    folium.plugins.LocateControl(position = 'topright',returnToPrevBounds = True).add_to(m)


    return m


def create_map(data:pd.DataFrame)->folium.Map :
    """
    This function creates a folium map based on the given data

    Parameters
    ----------
    data: Panda DataFrame
        The data which should be visualized.

    Returns
    -------
    folium_map:
        The created folium map.
    """

    # creating a new folum map with a start location(for the view) and the degree of the zoom
    m = folium.Map(location=[51.5, 10.0], zoom_start=6.47)

    #updating the map according to the data
    update(data,m)

    # adding the legend to the data describing
    add_legend(m)

    # saving the folium app localy
    m.save(os.path.join(get_root_dir(), os.path.join("App", "P&R_Karte.html")))

    return m
