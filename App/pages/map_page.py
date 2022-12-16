import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate
from pages import map_functions
import os


html_list = []
html_list.append(html.H3("Interaktive Karte Test"))
m = map_functions.create_map()

#----------!!!!!!!!!
# pfad zur karte manchmal weird muss vorm testen angepasst werden(also wenn was falsch läuft kann gut hier dran liegen)
html_list.append(html.Iframe(id="karte", srcDoc=open(os.path.join(os.path.dirname(__file__), '../P&R_Karte.html'), "r").read(), width="100%", height="800"))

layout = html.Div(html_list)
