import dash
import dash_bootstrap_components as dbc

external_stylesheets_list = [dbc.themes.BOOTSTRAP,
                        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
                        ]
app = dash.Dash(__name__, 
                external_stylesheets=external_stylesheets_list, 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)