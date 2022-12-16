import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State, MATCH, ALL
import numpy as np
from dash.exceptions import PreventUpdate
from utility.util_functions import *


#global inputs, outputs, states

data = get_data()

#for filtering content
temp_content = data.copy(deep=True)

def filter_content(df, filter):
    #ideen für filter: dictionary an attributen plus expected value?
    
    for f in filter:
        df.drop(df.loc[df[f] != filter[f]].index, inplace=True)

    
    return df

def create_content(df):
    cols = df.columns
    #print(cols)
    content = []
    names = []

    for i in range(len(df)):
        row = df.iloc[[i]]

        names.append(row["location"].values[0])

        inhalt = []
        for c in cols:
            mini = str(c) + ": " + str(row[c].values[0])
            inhalt.append(mini)
            inhalt.append(html.Br())

        content.append(inhalt)

    return names, content
    
def create_layout(names, content):

    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": "4rem",
        "right": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    sidebar = html.Div(
        [
            html.H2("Funcs", className="display-4"),
            html.Hr(),
            html.Button("Filter", id="filter_test", value="999"),
            html.Button("Revert", id="revert_filter_test", value="666"),
            dbc.Nav(
                [
                    dbc.Button("Add", id="filter_test2", value=999),
                    dbc.Button("Delete", id={"type":"test", "index":111}),
                    html.Div(id={"type":"output", "index":111}),
                    dbc.Button("Delete2", id={"type":"test", "index":222}),
                    html.Div(id={"type":"output", "index":222}),
                    dbc.Button("Test"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    html_list = []

    for i in range(len(names)):
        html_list.append(dbc.CardHeader(dbc.Button(
                    names[i],
                    color="outline",
                    id={"type":"header", "index":i},
                    value=i
                )))
        html_list.append(dbc.Collapse(
            dbc.CardBody(content[i]),
            id={"type":"content", "index":i}, 
            is_open=False
        ))

    html_list.append(sidebar)

    return html_list

def make_in_out_state(names):
    outs = [Output({"type":"content", "index":i}, "is_open") for i in range(len(names))]
    ins = [Input({"type":"header", "index":i}, "n_clicks") for i in range(len(names))]
    stas = [State({"type":"content", "index":i}, "is_open") for i in range(len(names))]

    return outs, ins, stas

names, content = create_content(data)

html_list_for_layout = create_layout(names, content)

layout = html.Div(children=html_list_for_layout, id="page-layout")

#outputs, inputs, states = make_in_out_state(names)



#@callback(
#    Output({"type":"content", "index":MATCH}, "is_open"),
#    [Input({"type":"header", "index":ALL}, "n_clicks")]
#)



#@callback(
#    Output({"type": "header", "index": MATCH}, "is_open"),
#    [Input({"type": "content", "index": MATCH}, "n_clicks")],
#    [State({"type": "header", "index": MATCH}, "is_open")]
#)
#@callback(
#    outputs, [inputs], [states]
#)
@callback(
    Output({"type": "content", "index": MATCH}, "is_open"),
    [Input({"type": "header", "index": MATCH}, "n_clicks")],
    [State({"type": "content", "index": MATCH}, "is_open")]
)
def toggle_collapses(butts, stats):
    print("printing", butts, stats)

    ctx = dash.callback_context
        
    if not ctx.triggered:
        print("Update prevented")
        raise PreventUpdate
    else:

        return not stats
        #print("It does smth")
            
        #button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        #print(button_id[9], type(button_id))
        #j = 0
        #for b, s in zip(butts, stats):
        #    if int(button_id[9]) == j:
        #        #print("happened")
        #        if s:
        #            stats[j] = False
        #            return tuple(stats)
        #        else:
        #            stats[j] = True
        #            return tuple(stats)
        #    j += 1

        #print(tuple(stats))
        #return tuple(stats)

#@callback(
#    Output("page-layout", "children"), [Input("revert_filter_test", "n_clicks")],
#    prevent_initial_call=True
#)
#def filter_buttons(n_clicks):
#    #temp_content = filter_content(data, {"location": "Heidelberg"})
#
#    names2, content2 = create_content(data)
#
#    layout = create_layout(names2, content2)
#    #print(layout)
#
#    return layout

@callback(
    Output("page-layout", "children"), [Input("filter_test", "n_clicks")],
    prevent_initial_call=True
)
def filter_buttons(n_clicks):
    #global inputs, outputs, states
    temp_content = filter_content(data, {"location": "Heidelberg"})

    names2, content2 = create_content(temp_content)

    #outputs, inputs, states = make_in_out_state(names2)
    #print(outputs, inputs, states)
    layout = create_layout(names2, content2)
    #print(layout)

    return layout
