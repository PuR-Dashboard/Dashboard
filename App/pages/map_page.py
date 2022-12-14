import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate
import os

html_list = []

#html_list.append(html.H3("Interaktive Karte Test"))

#button for refreshing the map
FA_icon = html.I(className="fa fa-refresh")
button = (html.Div(dbc.Button(FA_icon, color="light", className="me-1",
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
html_list.append(html.Iframe(id="karte", srcDoc=open(os.path.join(os.path.dirname(__file__), '../../P&R_Karte.html'), "r").read(), width="100%", height="600"))


layout = html.Div(html_list)


