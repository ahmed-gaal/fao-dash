"""The following scripts visualizes findings about bananas"""
import os
import pandas as pd
import cufflinks
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from crops import Dashboard as dd

px.set_mapbox_access_token(os.environ.get('TOKEN'))
dff = pd.read_excel('data/dff.xlsx')
dff.drop(columns=['Unnamed: 0', 'Area Code', 'Item Code', 'Element Code'],
         inplace=True)
dff.drop_duplicates(subset=['Y2014', 'Y2015', 'Y2016', 'Y2017', 'Y2018'],
                    inplace=True)
area = dff[dff['Element'] == 'Area harvested']
yield1 = dff[dff['Element'] == 'Yield']
prod = dff[dff['Element'] == 'Production']
world = pd.read_excel('data/world.xlsx')
drop = ['Unnamed: 0', 'Area Code', 'Area', 'Item Code', 'Element Code',
        'Y1961', 'Y1962', 'Y1963', 'Y1964', 'Y1965', 'Y1966', 'Y1967',
        'Y1968', 'Y1969', 'Y1970', 'Y1971', 'Y1972', 'Y1973', 'Y1974',
        'Y1975', 'Y1976', 'Y1977', 'Y1978', 'Y1979', 'Y1980', 'Y1981',
        'Y1982', 'Y1983', 'Y1984', 'Y1985', 'Y1986', 'Y1987', 'Y1988',
        'Y1989', 'Y1990', 'Y1991', 'Y1992', 'Y1993', 'Y1994', 'Y1995',
        'Y1996', 'Y1997', 'Y1998', 'Y1999', 'Y2000', 'Y2001', 'Y2002',
        'Y2003', 'Y2004', 'Y2005', 'Y2006', 'Y2007', 'Y2008', 'Y2009',
        'Y2010', 'Y2011', 'Y2012', 'Y2013']


ar = dd.world_clean('area', drop=drop)
pr = dd.world_clean('production', drop=drop)
yy = dd.world_clean('yield', drop=drop)

data = pd.read_csv('data/ndizi.csv')
colors = ['#273037', '#F68C3F', '#F16710', '#CB540B', '#AB2D28']
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode="number+delta",
    value=ar[ar['Item'] == 'Bananas'].Y2018.sum(),
    title={
        "text": "Area Harvested<br><span style='font-size:0.8em\
                ;color:gray'>in</span><br><span style='font-size:\
                0.8em;color:gray'>Hectares</span>"
    },
    delta={
        'reference': ar[ar['Item'] == 'Bananas'].Y2017.sum(), 'relative': True
    },
    domain={'x': [0, 0.5], 'y': [0.5, 0]}))

fig.add_trace(go.Indicator(
    mode="number+delta",
    value=pr[pr['Item'] == 'Bananas'].Y2018.sum(),
    title={
        "text": "Production<br><span style='font-size:0.8em;color:\
                gray'>in</span><br><span style='font-size:0.8em;\
                color:gray'>Tonnes</span>"
    },
    delta={
        'reference': pr[pr['Item'] == 'Bananas'].Y2017.sum(), 'relative': True
    },
    domain={'x': [0.5, 1], 'y': [0, 1]}))

fig.add_trace(go.Indicator(
    mode="number+delta",
    value=yy[yy['Item'] == 'Bananas'].Y2018.sum() / 10000,
    title={
        "text": "Yield<br><span style='font-size:0.8em;color\
                :gray'>in</span><br><span style='font-size:0.8em\
                ;color:gray'>Tonne per Hectare</span>"
    },
    delta={
        'reference': yy[yy['Item'] == 'Bananas'].Y2017.sum()/10000,
        'relative': True
    },
    domain={'x': [0.5, 0], 'y': [1, 0.5]}))


fig1 = dd.bar_graph(
    x='Years', y='Area harvested', xTitle='Area harvested',
    yTitle='Years', how='h', colors='#914F9A', item='Bananas',
    title='Area of Bananas Harvested (Hectares) in Somalia 2014-2018'
)

fig2 = dd.line_graph(
    x='Years', y='Production', xTitle='Years', mode='lines',
    colors='#CD4E43', how='spline', yTitle='Tonnes', item='Bananas',
    title='Banana Production in Somalia from 2014 - 2018'
)

fig3 = px.scatter_mapbox(
    dd.total_element('production', 'Bananas'), lat='Lat',
    lon='Lon', color='Total', hover_name='Area', size='Total',
    hover_data={'Lat': False, 'Lon': False}, labels={'Area': 'Element'},
    color_continuous_scale=colors, zoom=1.4, width=1900, height=700,
    template='presentation', center=None, mapbox_style='light',
    title='Global Banana Production in Tonnes(2014-2018)'
)

fig4 = data[data['Element'] == 'Production'].iplot(
    asFigure=True, kind='pie',
    labels='Area', values='Y2018',
    legend=False, textinfo='label+percent',
    theme='polar', hole=.6, linecolor='white',
    colors=colors, linewidth=.5,
    title='Banana Production in Africa as at 2018'
)

fig5 = dd.line_graph(
    x='Years', y='Yield', xTitle='Years', yTitle='Tonne per hectare',
    title='Banana Yield for Somalia (2014 - 2018)', mode='lines+markers',
    scale='puor', how='spline', item='Bananas'
)

layout = html.Div([
    dbc.Container([
        dbc.Row([
                dbc.Col(
                    html.H1(
                        'World Bananas Statistics as at 2018',
                        className='text-center'
                    ), className='mb-4 mt-5')
        ]),
        dbc.Row(
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='Chart',
                        figure=fig,
                        animate=True,
                        responsive=True,
                        config={
                            'showTips': True,
                            'displaylogo': False
                        }
                    )
                ], style={
                    'font-variant': 'small-caps', 'font-weight': 'bold'
                }), width=12, align='center'
            )
        )
    ], fluid=True),

    dbc.Row(
        dbc.Col(
            html.Div([
                dcc.Graph(
                    id='Chart1',
                    figure=fig3,
                    responsive='auto',
                    animate=True,
                    config={
                        'showTips': True,
                        'displaylogo': False,
                        'scrollZoom': False
                    })], style={
                        'font-variant': 'small-caps', 'font-weight': 'bold'
                    }
                ), width=12
        ), style={'font-variant': 'small-caps', 'font-weight': 'bold'}
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H2(
                children='Banana Production in Somalia.', style={
                    'font-family': 'Overpass, sans-serif',
                    'font-size': '200%', 'font-weight': 'bold'
                }
            ),
            width={'size': 6, 'offset': 4}
        )
    ], className='row'
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.Div([
                    dcc.Graph(
                        id='Chart2',
                        figure=fig2,
                        responsive=True,
                        animate=True,
                        config={
                            'showTips': True,
                            'displaylogo': False
                        }
                    )
            ], style={
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=6, align='center'
            ),
        dbc.Col(
            dbc.Container(
                html.P(
                    children='The analysis performed on the production of\
                        Bananas in Somalia has\
                        been on steep decrease from 2014\
                        until 2016 when it reached an all-time low of 19,897\
                        metric tonnes.\
                        This is true in that there was a period of famine\
                        in Somalia between\
                        2015-2016 and as a result a drop in production.\
                        As at 2017 we observed\
                        a 7.75% increase in Production.\
                        Production is set to increase exponentially due to\
                        torrential rains expected until 2021.', style={
                            'font-family': 'Overpass, sans-serif',
                            'font-size': '210%', 'font-weight': 'normal'
                        }
                )
            ), width=6
        )
    ], className='row'
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H2(children='Banana Production in Africa.', style={
                'font-family': 'Overpass, sans-serif', 'font-size': '200%',
                'font-weight': 'bold'
            }),
            width={'size': 6, 'offset': 4}
        )
    ], className='row'
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            dbc.Container(
                html.P(
                    children='The analysis performed on the Banana Production\
                        in Africa indicates\
                        East Africa having the highest Production as at 2018\
                        with a 53.5% followed\
                        by Central Africa with a 25.6% Production.\
                        This is accurate in that East Africa is in possession\
                        of optimal land for\
                        cultivating Bananas and followed by Central Africa.\
                        Southern Africa produced 2.21% of Bananas produced in\
                        2018 which\
                        establishes that Southern Africa is not suitable for\
                        Banana Production.', style={
                            'font-family': 'Overpass, sans-serif',
                            'font-size': '210%', 'font-weight': 'normal'
                        }
                )
            ), width=6
        ),

        dbc.Col(
            html.Div([
                    dcc.Graph(
                        id='Chart3',
                        figure=fig4,
                        responsive=True,
                        animate=True,
                        config={
                            'showTips': True,
                            'displaylogo': False
                        }
                    )
            ], style={
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=6, align='center'
        ),
    ], className='row'
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H2(children='Banana Area harvested in Somalia.', style={
                'font-family': 'Overpass, sans-serif', 'font-size': '200%',
                'font-weight': 'bold'
            }), width={'size': 6, 'offset': 4}
        )
    ], className='row'
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Graph(
                    id='Chart4',
                    figure=fig1,
                    responsive=True,
                    animate=True,
                    config={
                        'showTips': False,
                        'displaylogo': False
                    }
                )
            ], style={
                'font-variant': 'small-caps', 'font-weight': 'bold'
            }), width=6
        ),
        dbc.Col(
            dbc.Container(
                html.P(
                    children='The analysis performed on the Area harvested\
                        for Banana in Somalia indicates that 2014 was the year\
                        that largest parcel\
                        of land had been cultivated and harvested Bananas just\
                        shy of 1,400 hectares.\
                        This shows that 2014 was the year Somalia experienced\
                        an influx of farmers\
                        producing Bananas.\
                        Throughout 2015-2016 was a challenging year for\
                        Somali Farmers due to the\
                        drought and famine experienced during this time.\
                        As a result Area harvested\
                        decreased at a rate of 17.08%. 2017 showed a little\
                        bit of hope of 7% \
                        increase in area harvested.', style={
                            'font-family': 'Overpass, sans-serif',
                            'font-size': '210%', 'font-weight': 'normal'
                        }
                )
            ), width=6
            )
    ], className='row'
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            html.H2(
                children='Banana Yield in Somalia.',
                style={
                    'font-family': 'Overpass, sans-serif', 'font-size': '200%',
                    'font-weight': 'bold'
                }
            ),
            width={'size': 6, 'offset': 4}
        )
    ], className='row'
    ),
    html.Hr(),
    dbc.Row([
        dbc.Col(
            dbc.Container(
                html.P(
                    children='The analysis performed on the Yield of Bananas\
                        in Somalia.\
                        As we can see, 2014 shows a Yield of 17.03 Tonnes per\
                        hectare and\
                        throughout to 2018 shows a steady increase in Yield\
                        even though there\
                        were mitigating factors during the year 2015 upto\
                        2016.\
                        The conclusion of this analysis seems to indicate\
                        the Banana is a viable\
                        agricultural product in Somalia and possesses a\
                        higher market value both for local and International\
                        markets.', style={
                            'font-family': 'Overpass, sans-serif',
                            'font-size': '210%', 'font-weight': 'normal'
                        }
                )
            ), width=6
        ),
        dbc.Col(
            html.Div([
                dcc.Graph(
                    id='Chart5',
                    figure=fig5,
                    responsive=True,
                    animate=True,
                    config={
                        'showTips': True,
                        'displaylogo': False
                    }
                )],
                style={'font-variant': 'small-caps', 'font-weight': 'bold'}
            ), width=6
        ),
    ], className='row'
    )
])
