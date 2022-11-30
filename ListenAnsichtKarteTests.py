import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

sentences_head = ["Dies ist Standord Nummer Eins", "Dies ist Standord Nummer Zwei", "Dies ist Standord Nummer Drei"]
sentences_collapse = ["Hier kommt der Content von Standord Nummer Eins hin", "Hier kommt der Content von Standord Nummer Zwei hin", "Hier kommt der Content von Standord Nummer Drei hin"]

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
html_list.insert(0, html.Div(html.H6("Park and Ride Visualisierungskonzept"), style={"text-align":"center"}))
html_list.insert(1, html.Hr())

html_list.append(html.H1("Interaktive Karte Test"))
#----------!!!!!!!!!
# pfad zur karte manchmal weird muss vorm testen angepasst werden(also wenn was falsch läuft kann gut hier dran liegen)
html_list.append(html.Iframe(id="karte", srcDoc=open(r"C:\Users\Marc\Documents\BPTesting\P&R_Karte.html", "r").read(), width="100%", height="600"))

app.layout = html.Div(html_list)


outputs = [Output("collapse-question-{}".format(i), "is_open") for i in range(len(sentences_head))]
inputs = [Input("button-question-{}".format(i), "n_clicks") for i in range(len(sentences_head))]
states = [State("collapse-question-{}".format(i), "is_open") for i in range(len(sentences_head))]


@app.callback(
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


if __name__ == "__main__":
    app.run_server(port=8051) #debug=True,