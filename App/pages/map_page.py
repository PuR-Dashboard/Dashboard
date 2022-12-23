from gc import callbacks
import dash
import dash_bootstrap_components as dbc
<<<<<<< Updated upstream
from dash import html, dcc, callback
=======
from dash import html, dcc, callback,ctx
>>>>>>> Stashed changes
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate
import os
from utility import map_functions
from utility.map_functions import *
from pandas import read_csv
<<<<<<< Updated upstream

=======
from pages import list_page
from utility.util_functions import *
from components.sidebar import get_sidebar
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream


html_list = []
=======
seitentag = "_map"

#html_list = []

global data, temp_data

global sid 
sid = get_sidebar(seitentag)

data = get_data()
temp_data = data.copy(deep=True)
>>>>>>> Stashed changes

#html_list.append(html.H3("Interaktive Karte Test"))

#button for refreshing the map
FA_icon = html.I(className="fa fa-refresh")
<<<<<<< Updated upstream
button = (html.Div(dbc.Button([FA_icon, " Refresh"], color="light", className="me-1",
style={
                        "marginLeft": "93%",
=======
button = (html.Div(dbc.Button([FA_icon, " Refresh"], color="light", className="me-1",id = "test_refresh", value = 0,
style={
                        "marginLeft": "6%",
>>>>>>> Stashed changes
                        "width": "7%",
                        "height": "60%",
                        "fontSize": "1em",
                       # "background-color": "grey",
                        "color": "black",
                       # "border-radius": "4px",
                       # "border": "2px solid black",
                    },
                    )))

<<<<<<< Updated upstream
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
=======


#method to create the html which represents the map_page
#returns the layout of the map_page as a HTML List
def create_html_map(data):
    global sid

    html_list = []

    map_functions.create_map(data) # create the map
    html_list.append(button) # adding the Refresh_Button to the map_page
    html_list.append(  # Append the map tp the map_page
                    html.Iframe( #Create an Iframe element to get an interactive map
                    id="page-layout", # Set the id of the Iframe element
                    srcDoc=open(os.path.join(os.path.dirname(__file__), '../P&R_Karte.html'), "r").read(),# Set the source of the Iframe element to be the previously created map
                     width="87%", height="800" # set the width and the height of the IFrame Element
                     ))

    html_list.append(sid)
    
    return html_list

layout = html.Div( #creating the layout
                children = create_html_map(data), # the elements of the layout
                 id = "layout_map" # the ID of the layout
                 )







# method to filter and update the map_page
# Callback inputs:
    # 1-4: Buttons of the filter
    # 5 : Refreshing Button
    # 6-8 : dash_components to handel the pop-up and the filtering
# Callback output:
    # 1: the updated/filtered layout
    # 2: whether the modal_window is presented
    # 3: the value of the life-filter in the sidebar
    # 4: the value which was written in the location_filter
    # 5: the value which was choosen for the occupancy
# Callback State: is the open/close state of the pop up/modal

@callback(
    [Output("layout_map", "children"),
    Output("modal_window" + seitentag, "is_open"),
    Output("sideboard_name_filter" + seitentag, "value"),
    Output("modal_name_filter" + seitentag, "value"),
    Output("modal_occupancy_filter" + seitentag, "value")],
    [Input("clear_filter_button" + seitentag, "n_clicks"),
    Input("advanced_filter_button" + seitentag, "n_clicks"),
    Input("modal_submit_button" + seitentag, "n_clicks"),
    Input("modal_cancel_button" + seitentag, "n_clicks"),
    Input(component_id="test_refresh", component_property='n_clicks'),
    Input("modal_name_filter" + seitentag, "value"),
    Input("modal_occupancy_filter" + seitentag, "value"),
    Input("sideboard_name_filter" + seitentag, "value")],
    [State("modal_window" + seitentag, "is_open")],
    prevent_initial_call=True
)

def filter_map(_n1, _n2, _n3, _n4,n_5, modal_name_text, modal_occupancy_radio, sideboard_name_text, modal_state): #cancel_c_clicks,
    triggered_id = ctx.triggered_id

    #depending on the button pressed, act accordingly and return according values

    if triggered_id == "clear_filter_button" + seitentag:
        return reverse_Map(), modal_state, "", "", "None" #

    elif triggered_id == "advanced_filter_button" + seitentag:# was genau soll hier passieren
        return keep_layout_Map(), (not modal_state), "", modal_name_text, modal_occupancy_radio

    elif triggered_id == "modal_submit_button" + seitentag:
        filter_dict = list_page.create_filter_dict(modal_name_text, modal_occupancy_radio) #creating a dictionary according to the filter
        return filter_buttons_Map(filter_dict), (not modal_state), "", modal_name_text, modal_occupancy_radio

    elif triggered_id == "modal_cancel_button" + seitentag:
        return keep_layout_Map(), (not modal_state), "", "", "None"

    elif triggered_id == "sideboard_name_filter" + seitentag:
        filter_dict = list_page.create_filter_dict(sideboard_name_text, modal_occupancy_radio)
        return filter_buttons_Map(filter_dict), False, sideboard_name_text, modal_name_text, modal_occupancy_radio

    elif triggered_id == "test_refresh":
        return update(n_5), False, sideboard_name_text, modal_name_text, modal_occupancy_radio

    # default
    else:
        raise PreventUpdate



#function to replace the filtered dataframe with the original
#returns layout of page
def reverse_Map():
    global data, temp_data

    temp_data = data.copy(deep=True)

    return create_html_map(temp_data)



#function to replace the filtered dataframe with itself, not changing anything
#returns layout of page
def keep_layout_Map():

    global data, temp_data

    return create_html_map(temp_data)




#function to replace the current dataframe with the filtered version of the original
#returns layout of page
def filter_buttons_Map(filter_dict):

    global data, temp_data
    temp_data = data.copy(deep=True)

    temp_data = list_page.filter_content(temp_data, filter_dict)

    return create_html_map(temp_data)


#function to update the dataframe according to the data (checking for potentiell changes in the data)
# returns the updated layou of the page
def update(nr_clicks):
    global data, temp_data

    if nr_clicks == None:
        raise PreventUpdate
    data = get_data()
    temp_data = data.copy(deep=True)
    #only for testing
    #temp_data.drop(temp_data.loc[temp_data['location'] == "Heidelberg"].index, inplace = True )

    return create_html_map(temp_data)
>>>>>>> Stashed changes
