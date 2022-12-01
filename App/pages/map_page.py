import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate


html_list = []
html_list.append(html.H3("Interaktive Karte Test"))
#----------!!!!!!!!!
# pfad zur karte manchmal weird muss vorm testen angepasst werden(also wenn was falsch läuft kann gut hier dran liegen)
html_list.append(html.Iframe(id="karte", srcDoc=open(r"C:\Anni\TU Darmstadt\5. Semester\Bachelorpraktikum\Dashboard\P&R_Karte.html", "r").read(), width="100%", height="600"))

layout = html.Div(html_list)


