import dash_html_components as html 
import dash_bootstrap_components as dbc
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Crop Production Analysis', className='text-center'), className='mb-5 mt-5')
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.H4(children='This dashboard has been created by the Data Science team at the BlueXpress Technologies'))
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.H6('The data used in the development of this application was obtained from the United Nations Food and Agriculture Organization\'s public Data portal'))
        ]),
        html.Hr(),

    ])
])