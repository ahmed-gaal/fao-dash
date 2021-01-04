import os
import pandas as pd
import cufflinks as cf
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
pdd = dd.world_clean('production', drop=drop)
yy = dd.world_clean('yield', drop=drop)

data = pd.read_csv('data/sim.csv')
colors = ['#BD3F68','#121C1A','#23E1F0','#F14B5B','#E52C25']
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = ar[ar['Item'] == 'Sesame seed'].Y2018.sum(),
    title = {
        "text": "Area Harvested<br><span style='font-size\
                :0.8em;color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Hectares</span>"
    },
    delta = {
        'reference': ar[ar['Item'] == 'Sesame seed'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0, 0.5], 'y': [0.5, 0]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = pdd[pdd['Item'] == 'Sesame seed'].Y2018.sum(),
    title = {
        "text": "Production<br><span style='font-size:0.8em;\
                color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Tonnes</span>"
    },
    delta = {
        'reference': pdd[pdd['Item'] == 'Sesame seed'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0.5, 1], 'y': [0, 1]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = yy[yy['Item'] == 'Sesame seed'].Y2018.sum() / 10000,
    title = {
        "text": "Yield<br><span style='font-size:0.8em\
                ;color:gray'>in</span><br><span style='font-size:0.8em\
                ;color:gray'>Tonne per Hectare</span>"
    },
    delta = {
        'reference': yy[yy['Item'] == 'Sesame seed'].Y2017.sum()/10000,\
            'relative': True
    },
    domain = {'x': [0.5, 0], 'y': [1, 0.5]}))


fig1 = dd.bar_graph(x='Years', y='Area harvested', xTitle='Area harvested', yTitle='Years',
                 title='Area Harvested (Hectares)', how='h', colors='#AD1A31', item='Sesame seed')

fig2 = dd.line_graph(x='Years', y='Production', xTitle='Years', yTitle='Tonnes',
                  colors='#AD1A31',how='spline', mode='lines', item='Sesame seed',
                  title='Sesame seed Production in Somalia from 2014 - 2018')

fig3 = px.scatter_mapbox(dd.total_element('production', 'Sesame seed'), lat='Lat',
                         lon='Lon', color='Total', hover_name='Area', size = 'Total',
                         hover_data={'Lat':False, 'Lon':False}, labels = {'Area':'Element'},
                         color_continuous_scale=colors, zoom=1.4, width=1900, height=700,
                         template='presentation', center=None, mapbox_style='light',
                         title='Global Sesame seed Production in Tonnes(2014-2018)')

fig4 = data[data['Element'] == 'Production'].iplot(asFigure=True, kind='pie',
                                                   labels='Area', values='Y2018',
                                                   legend=False,textinfo='label+percent',
                                                   theme='polar', hole=.6, linecolor='white',
                                                   colors=colors, linewidth=.5,
                                                   title='Sesame seed Production in Africa as at 2018')

fig5 = dd.line_graph(x='Years', y='Yield', xTitle='Years', yTitle='Tonne per hectare',
                  title='Sesame seed Yield for Somalia (2014 - 2018)', mode='lines+markers',
                  scale='puor', how='spline', item='Sesame seed')

layout = html.Div([
    dbc.Container([
        dbc.Row([
                dbc.Col(html.H1('World Sesame seed Statistics as at 2018', className='text-center'), className='mb-4 mt-5')
            ]),
        dbc.Row(
            dbc.Col(html.Div([
                    dcc.Graph(id = 'Chart42',
                            figure = fig,
                            animate = True,
                            responsive = True,
                            config = {
                                'showTips': True,
                                'displaylogo': False
                            })], style = {'font-variant':'small-caps','font-weight':'bold'}), width = 12, align='center')
        )
    ], fluid=True),
        dbc.Row(
            dbc.Col(html.Div([
                    dcc.Graph(id = 'Chart43',
                            figure = fig3,
                            responsive = 'auto',
                            animate = True,
                            config = {
                                'showTips':True,
                                'displaylogo':False,
                                'scrollZoom':False
                            })], style = {'font-variant':'small-caps','font-weight':'bold'}),width=12), style={'font-variant':'small-caps','font-weight':'bold'}),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='Sesame Seed Production in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        
        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart44',
                                figure = fig2,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips':True,
                                    'displaylogo':False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6, align='center'),
            dbc.Col(
                dbc.Container(
                    html.P(children='The analysis performed on the Production of Sesame Seed in Somalia from 2014 to 2018\
                        shows that a total of 129,616 metric tonnes was produced over the course of 5 years. The year with \
                        the highest production was 2014 with a total output of 26,275 metric tonnes. By 2015, this value decreased\
                        with a 1.1% and went on a further 0.8% decrease by 2016.\
                        The year 2017 we observed an increase in production by 0.01% and a further 0.02% increase in production by 2018.\
                        The poor production may have been caused by environmental factors.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='Sesame Seed Production in Africa.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container(
                    html.P(children='The analysis performed shows that between 2014 to 2018 Eastern Africa has been the largest producer of Sesame seeds in\
                        Africa. Over the course of 5 years, East Africa has produced a whopping 7.8 million metric tonnes with the United Republic\
                        of Tanzania producing more than half of it making it the largest producer of Sesame seeds worldwide.\
                        Northern and Western Africa performed fairly well with a 28.7% and 27.7% production as at 2018 respectively.\
                        Central Africa performed poorly with a production rate of 6.7% as at 2018 and little over 1 million metric tonnes\
                        over the course of 5 years.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            ),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart45',
                                figure = fig4,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips': True,
                                    'displaylogo': False
                                })
            ], style={'font-variant':'small-caps','font-weight':'bold'}), width=6, align = 'center'),
        ], className='row'),

        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='Sesame Seed Area Harvested in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart46',
                                figure = fig1,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips':False,
                                    'displaylogo':False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6),
            dbc.Col(
                dbc.Container(
                    html.P('The analysis performed on the Sesame seed Area harvested shows that over the course of 5 years,\
                        the Area harvested slowly but steadily decreased. This may be due to environmental fators such as soil\
                        fertlity, topography, water quality or climate change.\
                        Further observations is required, hence we will continue to monitor the situation closely.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='Sesame Seed Yield in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container(
                    html.P(children='The analysis performed on the data provided shows that the Yield of Sesame seed in Somalia\
                        has been on constant increase. From 2014 to 2015 we observed an increase in yield by 0.6%. From 2015 to 2016,\
                        even though we experienced environmental factors such as drought and famine, a 0.4% increase in the yield was observed.\
                        From 2017 to 2018 we observed a 0.7% increase in yield which amounts to 0.55 tonnes per hectare.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            ),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart47',
                                figure = fig5,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips':True,
                                    'displaylogo': False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6),
        ], className='row')


])