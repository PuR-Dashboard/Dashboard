import pyautogui
import folium
from folium import plugins
from folium.plugins import MarkerCluster
from folium_jsbutton import JsButton
from pandas import read_csv
import ctypes
import branca


def add_markers(markers, folium_map):
    """
    Add markers to the map
    :param markers: The markers to add
    :param folium_map: The map to add the markers to
    """
    for i in range(len(markers)):  # Iterate over all markers
        marker = markers[i]  # Get the marker
        folium.Marker(  # Add the marker to the map
            location=[marker[0],  # Latitude
                      marker[1]],  # Longitude
            popup=marker[2],  # Popup for the marker
            icon=folium.Icon(color=marker[3])  # Icon for the marker
        ).add_to(folium_map)  # Add the marker to the map


def get_screensize():
    """
    Get the size of the primary monitor
    :return: width, height
    """
    return pyautogui.size()  # Returns a tuple of (width, height)


def create_popup_html(data, screensize):
    """
    Creates and returns the html for the popup
    :param data: The data that is displayed in the popup
    :param screensize: The size of the screen
    :return: The html for the popup
    """
    html_list = []  # Create a list to store the html in

    for i in range(len(data)):  # Iterate over all rows
        one = data.iloc[i] # Get the row with the data
        html = f"""  
            <h1> {one[0]}</h1>
            <img src= "https://th.bing.com/th/id/OIP.mbBEbzuRMttCVk4AyTzIxwHaD8?pid=ImgDet&rs=1" width="250" height="250" align="right">
            &thinsp;
            <p><B><u>Charakteristika:</u></B></p>
            <ul>
                <li><B>occupancy_tendency</B>: {one[3]}</li>
                &thinsp;
                &thinsp;
                <li><B>occupancy_traffic_light</B>: {one[5]}</li>
                &thinsp;
                <li><B>occupancy_label:</B> {one[6]}</li>&thinsp;
                <li><B><a href="https://www.python-graph-gallery.com">ÖPNV-Anbindung</a></B>: S3, S4, Bus</li>
            </ul>
            &thinsp;
            <p><B><u>Prognose:</u></B></p>
            <ul>
                <li> <B>Mo-Fr</B> Morgens <font color = red>&emsp; voll </font></li>&thinsp;
                <li> <B>Mo-Fr</B> Mittags <font color = green>&emsp; leer </font></li>&thinsp;
                <li> <B>Mo-Fr</B> Abends<font color = orange>&emsp; mittel </font></li>&thinsp;
                <li> <B>Sa-So</B> Morgens</li>&thinsp;
                <li> <B>Sa-So</B> Mittags</li>&thinsp;
                <li> <B>Sa-So</B> Abends</li>&thinsp;
            </ul>
            </p>
            <body><py-script output="plot">
        </py-script></body>
         """  # Create the html for the popup

        iframe = folium.IFrame(  # Create an iframe for the popup
            html=html,  # The html for the popup
            width=screensize[0]/2,  # The width of the popup
            height=screensize[1]*2/3  # The height of the popup
        )

        popup = folium.Popup(  # Create the popup
            iframe,  # The iframe for the popup
            max_width=7000  # The max width of the popup
        )

        html_list.append(popup)  # Add the popup to the list

    return html_list  # Return the list with the popups


def create_einzugsgebiete(areas, cluster):
    """
    Creates the "Einzugsgebiete"
    :param areas: The areas to add
    :param cluster: The cluster to add the areas to
    """
    for area in areas:  # Iterate over all areas
        circle = folium.vector_layers.Circle(  # Create a circle for the "Einzugsgebiet"
            location=(area[0],  # Latitude
                      area[1]),  # Longitude
            radius=area[2],  # Radius of the circle
            color="#3186cc",  # Color of the circle
            fill=True,  # Fill the circle
            fill_color="#3186cc"  # Color of the fill
        )
        circle.add_to(cluster)  # Add the circle to the cluster


def create_button(function):
    """
    Creates a button that executes the given function
    :param function: The function to execute
    :return: The button
    """
    return JsButton(title='<i class="fas fa-crosshairs"></i>', function=function)


def add_legend(folium_map):
    """
    Adds a legend to the map
    :param folium_map: The map to add the legend to
    :return: The map with the legend
    """
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
    '''  # The html for the legend

    legend = branca.element.MacroElement()  # Create a macro element for the legend

    legend._template = branca.element.Template(legend_html)  # Add the html to the macro element

    folium_map.get_root().add_child(legend)  # Add the legend to the map

    return folium_map  # Return the map with the legend


def update(m):
    """
    Updates the map
    :param m: The map to update
    :return: The updated map
    """

    # TODO: Fix path
    data = read_csv(
        "C:\\Users\\Marc\\Downloads\\Dashboard\\Dashboard\\Location_Data (1).csv",
        delimiter=','
    )

    screensize = get_screensize()  # Get the screensize

    html = create_popup_html(data, screensize)  # Create the html for the popups

    markers = []  # Create a list for the markers

    for i in range(len(data)):  # Iterate over all data
        markers.append(  # Add the marker to the list
            [
                data.iloc[i][2],  # Latitude
                data.iloc[i][1],  # Longitude
                html[i],  # The html for the popup
                "red"  # The color of the marker
            ]
        )

    add_markers(markers, m)  # Add the markers to the map

    einzugsgebiete = MarkerCluster(  # Create a cluster for the "Einzugsgebiete"
        name='Einzugsgebiete',  # Name of the cluster
        show=False  # Disable the cluster by default
    ).add_to(m)  # Add the cluster to the map

    areas = []  # Create a list for the areas

    for i in range(len(data)):  # Iterate over all data
        areas.append(  # Add the area to the list
            [
                data.iloc[i][2],  # Latitude
                data.iloc[i][1],  # Longitude
                10000  # Radius of the area
            ]
        )

    create_einzugsgebiete(areas, einzugsgebiete)  # Create the "Einzugsgebiete"

    folium.plugins.LocateControl().add_to(m)  # Add the locate-control to the list. Allows the user to locate himself

    folium.plugins.Search(  # Add the search bar to the map
        layer=einzugsgebiete,  # The layer to search in
        position='topright'  # Position of the search bar
    ).add_to(m)  # Add the search bar to the map

    folium.LayerControl().add_to(m)  # Add the layer control to the map

    return m  # Return the updated map


def create_map():
    """
    Creates the map
    :return: The map
    """
    m = folium.Map(  # Create the map
        location=[51.5, 10.0],  # The location of the map
        zoom_start=6.47  # The zoom level of the map
    )

    update(m)  # Update the map

    add_legend(m)  # Add the legend to the map

    m.save("P&R_Karte.html")  # Save the map to a html file

    return m  # Return the map
