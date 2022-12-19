# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

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


def Sidebar():
    sidebar = html.Div(
        [
            html.H2("Funcs", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    html.H4("Name"),
                    dbc.Input(id="sideboard_name_filter", type="text", debounce=False, value="", placeholder="Location Name", autofocus=True),
                    dbc.Button("Advanced", id="advanced_filter_button", value=999, style=BUTTON_STYLE),
                    html.Br(),
                    dbc.Button("Clear Filter", id="clear_filter_button",style=BUTTON_STYLE),
                    html.Br(),
                ],
                vertical=True,
                pills=True,
            ),
            dbc.Modal(
            [
                dbc.ModalHeader("Nach Kategorie filtern"),
                dbc.ModalBody(
                    [
                        dbc.Label("Name:"),
                        dbc.Input(id="modal_name_filter", type="text", debounce=True, value=""),
                        dbc.Label("Auslastung:"),
                        dbc.RadioItems(
                            options=[
                            {'label': 'Hoch', 'value': 'red'}, 
                            {'label': 'Mittel', 'value': 'yellow'}, 
                            {'label': 'Niedrig', 'value': 'green'}, 
                            {'label': 'Keine Angabe', 'value': 'None'}
                            ],
                            value='None',
                            inline=False,
                            id="modal_occupancy_filter"
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Apply", color="primary", id="modal_submit_button"),
                        dbc.Button("Discard", id="modal_cancel_button"),
                    ]
                ),
            ],
            id="modal_window",
            centered=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    return html.Div([sidebar])