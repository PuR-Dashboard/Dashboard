import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import numpy as np
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])  # https://bootswatch.com/default/

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
html_list.append(html.Iframe(id="karte", srcDoc=open(r"C:\Users\Marc\Documents\BPTesting\P&R_Karte.html", "r").read(), width="100%", height="600"))

app.layout = html.Div(html_list)


outputs = [Output("collapse-question-{}".format(i), "is_open") for i in range(len(sentences_head))]
inputs = [Input("button-question-{}".format(i), "n_clicks") for i in range(len(sentences_head))]
states = [State("collapse-question-{}".format(i), "is_open") for i in range(len(sentences_head))]

#@app.callback(
#    [
#      Output("collapse-question-0", "is_open"),
#      Output("collapse-question-1", "is_open"),
#    ],
#    [
#      Input("button-question-0", "value"),
#      Input("button-question-1", "value"),
#    ],
#    [State("collapse-question-0", "is_open"), 
#    State("collapse-question-1", "is_open")],
#)
@app.callback(
    outputs, [inputs], [states]
)
def toggle_collapses(butts, stats):
    ctx = dash.callback_context
    #print("ctx ", ctx.triggered)
    
    if not ctx.triggered:
        print("Update prevented")
        raise PreventUpdate
    else:
        #ret_bools = np.zeros(len(sentences_head), dtype="int")

        #stats = [params[i] for i in range(len(sentences_head), len(params))]
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        #print("Button ID: ", button_id)
        #print("States: ", ret_bools)
        j = 0
        for b, s in zip(butts, stats):
            #print("Value ", b)
            if button_id == "button-question-{}".format(j):
                if s:
                    stats[j] = False
                    return tuple(stats)
                else:
                    stats[j] = True
                    return tuple(stats)
            j += 1


        return tuple(stats)
#def toggle_collapses(*params):
#    ctx = dash.callback_context
#    print(ctx.triggered)
#    
#    if not ctx.triggered:
#        print("Update prevented")
#        raise PreventUpdate
#    else:
#        #ret_bools = np.zeros(len(sentences_head), dtype="int")
#
#        stats = [params[i] for i in range(len(sentences_head), len(params))]
#        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#        #print("Button ID: ", button_id)
#        #print("States: ", ret_bools)
#
#        for j in range(len(sentences_head)):
#            print(j)
#            print(stats[j])
#            if button_id == "button-question-{}".format(j):
#                if stats[j]:
#                    stats[j] = False
#                    return tuple(stats)
#                else:
#                    stats[j] = True
#                    return tuple(stats)
#
#
#        return tuple(stats)
    #else:
    #    print(button_id)
    #    raise ValueError('Unexpected ID: {}'.format(button_id))
"""
@app.callback(
    Output("collapse-question-1", "is_open"),
    [Input("button-question-1", "n_clicks")],
    [State("collapse-question-1", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-question-2", "is_open"),
    [Input("button-question-2", "n_clicks")],
    [State("collapse-question-2", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
"""

if __name__ == "__main__":
    app.run_server(port=8051) #debug=True,