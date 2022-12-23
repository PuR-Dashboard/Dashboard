# Import necessary libraries
from dash import html, dcc
from dash.dependencies import Input, Output

<<<<<<< Updated upstream
=======
from components import sidebar
>>>>>>> Stashed changes
# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import map_page, list_page

# Connect the components to the index
from components import navbar
from components import sidebar

# Define the navbar
nav = navbar.Navbar()

#Define sidebar
sid = sidebar.Sidebar()

<<<<<<< Updated upstream
# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
    sid,
=======

nav = navbar.get_navbar()  # Create the navbar

#sid = sidebar.get_sidebar()  # Create the sidebar

app.layout = html.Div([  # Create a Div containing the navbar and the content
    dcc.Location(id='url', refresh=False),  # Track current URL of the page
    nav,  # Add the navbar
    html.Div(id='page-content', children=[]),  # Add the page content
    #sid  # Add the sidebar
>>>>>>> Stashed changes
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/map_page':
        return map_page.layout
    if pathname == '/list_page':
        return list_page.layout
    else: # if redirected to unknown link
        return map_page.layout

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
