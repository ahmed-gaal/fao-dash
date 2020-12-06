import dash_html_components as html 
import dash_bootstrap_components as dbc
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1('Crop Production Analysis', style={
                'font-family': 'Overpass, sans-serif', 'font-size':'250%', 'font-weight':'bold', 'font-variant':'small-caps'
            },className='text-center'), className='mb-5 mt-5')
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container([
                    html.H2(children='This dashboard has been created by the Data Science team at the BlueXpress Technologies'),
                    html.Hr(),
                    html.H2(children='The data used in the development of this application was obtained from the United Nations \
                    Food and Agriculture Organization\'s public Data portal')
                    ]))
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container([
                    html.P(children='This dashboard has been categorised in two groups:',
                    style={
                        'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                    }),
                    html.P(children='1. Fruits which comprise of (Bananas, Grapefruits and Lemons)',
                    style={
                        'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                    }),
                    html.P(children='2. Dry Foods which comprise of (Beans, Sesame seed and Maize)',
                    style={
                        'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                    })
                ])
            )
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container([
                    html.P(children='It seeks to reveal insights from the data obtained.\
                        The data has been cleaned process produced data which has been \
                        optimized for data mining and data manipulation.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        }),
                    html.Hr(),
                    html.P(children='This project seeks to reveal insights combined with historical data and delves\
                        deeper into analysis of trends.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        }),
                    html.Hr(),
                    html.P(children='Therefore, this dashboard can serve as a fundamental part\
                        for generating future decisons that are important for Crop Production.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        }),
                        html.Hr(),
                    html.P(children='The Model Prediction System is still underway. The unforeseen delay has been\
                        largely attributed to insufficient data for training sets.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ])
            )
        ])

    ])
])