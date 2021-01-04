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
pdd =dd.world_clean('production', drop=drop)
yy = dd.world_clean('yield', drop=drop)

data = pd.read_csv('data/mahindi.csv')
colors = ['#957CC3','#ACD37B','#60A3F2','#8A74C4','#3A6EB8']
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = ar[ar['Item'] == 'Maize'].Y2018.sum(),
    title = {
        "text": "Area Harvested<br><span style='font-size\
                :0.8em;color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Hectares</span>"
    },
    delta = {
        'reference': ar[ar['Item'] == 'Maize'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0, 0.5], 'y': [0.5, 0]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = pdd[pdd['Item'] == 'Maize'].Y2018.sum(),
    title = {
        "text": "Production<br><span style='font-size:0.8em;\
                color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Tonnes</span>"
    },
    delta = {
        'reference': pdd[pdd['Item'] == 'Maize'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0.5, 1], 'y': [0, 1]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = yy[yy['Item'] == 'Maize'].Y2018.sum() / 10000,
    title = {
        "text": "Yield<br><span style='font-size:0.8em\
                ;color:gray'>in</span><br><span style='font-size:0.8em\
                ;color:gray'>Tonne per Hectare</span>"
    },
    delta = {
        'reference': yy[yy['Item'] == 'Maize'].Y2017.sum()/10000,\
            'relative': True
    },
    domain = {'x': [0.5, 0], 'y': [1, 0.5]}))


fig1 = dd.bar_graph(x='Years', y='Area harvested', xTitle='Area harvested', yTitle='Years',
                 title='Area Harvested (Hectares)', how='h', colors='#3A6EB8', item='Maize')

fig2 = dd.line_graph(x='Years', y='Production', xTitle='Years', yTitle='Tonnes',
                  colors='red',how='spline', mode='lines', item='Maize',
                  title='Maize Production in Somalia from 2014 - 2018')

fig3 = px.scatter_mapbox(dd.total_element('production', 'Maize'), lat='Lat',
                         lon='Lon', color='Total', hover_name='Area', size = 'Total',
                         hover_data={'Lat':False, 'Lon':False}, labels = {'Area':'Element'},
                         color_continuous_scale=colors, zoom=1.4, width=1900, height=700,
                         template='presentation', center=None, mapbox_style='light',
                         title='Global Maize Production in Tonnes(2014-2018)')

fig4 = data[data['Element'] == 'Production'].iplot(asFigure=True, kind='pie',
                                                   labels='Area', values='Y2018',
                                                   legend=False,textinfo='label+percent',
                                                   theme='polar', hole=.6, linecolor='white',
                                                   colors=colors, linewidth=.5,
                                                   title='Maize Production in Africa as at 2018')

fig5 = dd.line_graph(x='Years', y='Yield', xTitle='Years', yTitle='Tonne per hectare',
                  title='Maize Yield for Somalia (2014 - 2018)', mode='lines+markers',
                  scale='puor', how='spline', item='Maize')

layout = html.Div([
    dbc.Container([
        dbc.Row([
                dbc.Col(html.H1('World Maize Statistics as at 2018', className='text-center'), className='mb-4 mt-5')
            ]),
        dbc.Row(
            dbc.Col(html.Div([
                    dcc.Graph(id = 'Chart36',
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
                    dcc.Graph(id = 'Chart37',
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
                html.H2(children='Maize Production in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart38',
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
                    html.P(children='The analysis performed on the Production of Maize in Somalia shows that from 2014 to 2018, a total of\
                        484,159 metric tonnes was observed. The best year for Maize producers in Somalia was 2018 with a Production just \
                        shy of 140,000 metric tonnes.\
                        The worst year for Maize Producers in Somalia was 2016 with an output of 63,251 metric tonnes. This suggests that the\
                        drought and famine season in 2016 hit the Maize producers very hard.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='Maize Production in Africa.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container(
                    html.P(children='The analysis performed on Maize Production in Africa puts Eastern Africa at the forefront of Maize production in Africa.\
                        With a total of 28.9 million metric tonnes as at 2018, East Africa claims 36.7% of total Maize produced during 2018.\
                        Western Africa performed fairly well with a production of 28.4% of total Maize produced in Africa as at 2018.\
                        Northern and Central Africa performed very poorly with no more than an output of 15 million metric tonnes combined.\
                        This suggets that Maize is a staple food in Eastern Africa.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            ),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart39',
                                figure = fig4,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips': True,
                                    'displaylogo': False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6, align = 'center'),
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='Maize Area Harvested in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart40',
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
                    html.P(children='The analysis performed shows a total of 654,000 hectares was prepared, tilled, cultivated and harvested with\
                        Maize from 2014 to 2018. The year with the most land cultivated with Maize was 2015 just shy of 200,000 hectares.\
                        From 2015 to 2018 we observed a 49% drop in Area harvested for Maize in Somalia.\
                        Further analysis is required to understand the drop in Area harvested and the increase of the Production and Yield of Maize in Somalia.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='Maize Yield in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container(
                    html.P(children='The analysis shows that the Yield of Maize in Somalia. From 2014 to 2015 we observe a 17% drop\
                        in the Yield of Maize. Consequently, we observe a 4.16% increase in yield during 2015 to 2016.\
                        During 2016 to 2017 we observe an 11.1% increase in the yield.\
                        From 2017 to 2018 we observe a 129.6% spike in the yield of Maize in Somalia which amounts to 1.5 tonnes per hectare.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            ),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart41',
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