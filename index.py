import time
startTime = time.time()
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import server
from app import app
# import all pages in the app
from apps import banana,home,bean,grapefruit,cassava,lemon,maize,sesame,sorghum,sugarcane

##

##
# building the navigation bar
nav_item = dbc.NavItem(dbc.NavLink("Home", href='/home'))
navitem = dbc.NavItem(dbc.NavLink("BlueXpress Technologies", style = {'font-varianr':'small-caps','font-weight':'bold'},href='https://blueexpress.vercel.app/'))
# make a dropdown for the different pages
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Bananas", href="/banana"),
        dbc.DropdownMenuItem("Grapefruit", href="/grapefruit"),
        dbc.DropdownMenuItem("Sugar Cane", href="/sugarcane"),
        dbc.DropdownMenuItem("Lemons and Limes", href="/lemon"),
    ],
    nav=True,
    in_navbar=True,
    label="Fruits",
)
drop_down = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Beans", href="/bean"),
        dbc.DropdownMenuItem("Sesame Seed", href="/sesame"),
        dbc.DropdownMenuItem("Cassava", href="/cassava"),
        dbc.DropdownMenuItem("Maize", href="/maize"),
        dbc.DropdownMenuItem("Sorghum", href="/sorghum"),
    ],
    nav = True,
    in_navbar = True,
    label = "Dry Foods",
)
# Navbar Layout
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/log.png', height="50px",), width=4),
                        dbc.Col(dbc.NavbarBrand("Crop Production Analysis", className="ml-2"), width=8),
                    ],
                    align="center",
                    no_gutters=True,
                ),
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item,navitem,dropdown,drop_down], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="secondary",
    dark=False,
    className="mb-5",
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)
# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/banana':
        return banana.layout
    elif pathname == '/bean':
        return bean.layout
    elif pathname == '/cassava':
        return cassava.layout
    elif pathname == '/grapefruit':
        return grapefruit.layout
    elif pathname == '/lemon':
        return lemon.layout
    elif pathname == '/sugarcane':
        return sugarcane.layout
    elif pathname == '/sesame':
        return sesame.layout
    elif pathname == '/sorghum':
        return sorghum.layout 
    elif pathname == '/maize':
        return maize.layout
    else:
        return home.layout

execute = (time.time() - startTime)
print(execute)

if __name__ == '__main__':
    app.run_server(debug=True)
