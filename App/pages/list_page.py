import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate
import csv
from pandas import read_csv
import os


#einlesen der csv-Datei
data = read_csv(os.path.join(os.path.dirname(__file__),'../../Location_Data (1).csv'),delimiter=',')
sentences_head = []
sentences_collapse = []
for i in range(len(data)):
    sentences_head.append(data.iloc[i][0])
    one = ["Daten des P&R-Standortes in "+ data.iloc[i][0]]
    sentences_collapse.append(one)



html_list = []

for i in range(len(sentences_head)):
    html_list.append(dbc.CardHeader(dbc.Button(
                sentences_head[i],
                color="outline",
                id="button-question-{}".format(i),
                value=i
            )))
    html_list.append(dbc.Collapse(
        dbc.CardBody(sentences_collapse[i]),
        id="collapse-question-{}".format(i), is_open=False
    ))


#
outputs = [Output("collapse-question-{}".format(i), "is_open") for i in range(len(sentences_head))]
inputs = [Input("button-question-{}".format(i), "n_clicks") for i in range(len(sentences_head))]
states = [State("collapse-question-{}".format(i), "is_open") for i in range(len(sentences_head))]

@callback(
    outputs, [inputs], [states]
)
def toggle_collapses(butts, stats):
    ctx = dash.callback_context

    if not ctx.triggered:
        print("Update prevented")
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        j = 0
        for b, s in zip(butts, stats):
            if button_id == "button-question-{}".format(j):
                if s:
                    stats[j] = False
                    return tuple(stats)
                else:
                    stats[j] = True
                    return tuple(stats)
            j += 1


        return tuple(stats)


layout = html.Div(html_list)
