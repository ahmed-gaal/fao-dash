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
    
data = pd.read_csv('data/bambelmo.csv')
colors = ['#4E5C8C','#D6AB2C','#79B2D6','#879E9C','#E52C25']
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = ar[ar['Item'] == 'Grapefruit (inc. pomelos)'].Y2018.sum(),
    title = {
        "text": "Area Harvested<br><span style='font-size\
                :0.8em;color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Hectares</span>"
    },
    delta = {
        'reference': ar[ar['Item'] == 'Grapefruit (inc. pomelos)'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0, 0.5], 'y': [0.5, 0]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = pdd[pdd['Item'] == 'Grapefruit (inc. pomelos)'].Y2018.sum(),
    title = {
        "text": "Production<br><span style='font-size:0.8em;\
                color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Tonnes</span>"
    },
    delta = {
        'reference': pdd[pdd['Item'] == 'Grapefruit (inc. pomelos)'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0.5, 1], 'y': [0, 1]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = yy[yy['Item'] == 'Grapefruit (inc. pomelos)'].Y2018.sum() / 10000,
    title = {
        "text": "Yield<br><span style='font-size:0.8em\
                ;color:gray'>in</span><br><span style='font-size:0.8em\
                ;color:gray'>Tonne per Hectare</span>"
    },
    delta = {
        'reference': yy[yy['Item'] == 'Grapefruit (inc. pomelos)'].Y2017.sum()/10000,\
            'relative': True
    },
    domain = {'x': [0.5, 0], 'y': [1, 0.5]}))

fig1 = dd.bar_graph(x='Years', y='Area harvested', xTitle='Area harvested', yTitle='Years',
                    title='Area Harvested (Hectares)', how='h', colors='#4E5C8C', item='Grapefruit (inc. pomelos)')

fig2 = dd.line_graph(x='Years', y='Production', xTitle='Years', yTitle='Tonnes',
                    colors='#E52C25',how='spline', mode='lines', item='Grapefruit (inc. pomelos)',
                    title='Grapefruit (inc. pomelos) Production in Somalia from 2014 - 2018')

fig3 = px.scatter_mapbox(dd.total_element('production', 'Grapefruit (inc. pomelos)'), lat='Lat',
                         lon='Lon', color='Total', hover_name='Area', size = 'Total',
                         hover_data={'Lat':False, 'Lon':False}, labels = {'Area':'Element'},
                         color_continuous_scale=colors, zoom=1.4, width=1900, height=700,
                         template='presentation', center=None, mapbox_style='light',
                         title='Global Grapefruit (inc. pomelos) Production in Tonnes(2014-2018)')

fig4 = data[data['Element'] == 'Production'].iplot(asFigure=True, kind='pie',
                                                   labels='Area', values='Y2018',
                                                   legend=False,textinfo='label+percent',
                                                   theme='polar', hole=.6, linecolor='white',
                                                   colors=colors, linewidth=.5,
                                                   title='Grapefruit (inc. pomelos) Production in Africa as at 2018')

fig5 = dd.line_graph(x='Years', y='Yield', xTitle='Years', yTitle='Tonne per hectare',
                  title='Grapefruit (inc. pomelos) Yield for Somalia (2014 - 2018)', mode='lines+markers',
                  scale='puor', how='spline', item='Grapefruit (inc. pomelos)')

layout = html.Div([
    dbc.Container([
        dbc.Row([
                dbc.Col(html.H1('World Grapefruit Statistics as at 2018', className='text-center'), className='mb-4 mt-5')
            ]),
        dbc.Row(
            dbc.Col(html.Div([
                    dcc.Graph(id = 'Chart18',
                            figure = fig,
                            animate = True,
                            responsive = True,
                            config = {
                                'showTips': True,
                                'displaylogo': False
                            })], style = {'font-variant':'small-caps','font-weight':'bold'}), width = 12, align='center')
        )
    ], fluid=True),
        dbc.Row([
            dbc.Col(html.Div([
                    dcc.Graph(id = 'Chart19',
                            figure = fig3,
                            responsive = 'auto',
                            animate = True,
                            config = {
                                'showTips':True,
                                'displaylogo':False,
                                'scrollZoom':False
                            })], style = {'font-variant':'small-caps','font-weight':'bold'}),width=12),
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='GrapeFruit Production in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart20',
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
                    html.P(children='The analysis performed shows that production of Grapefruits including pomelos was at\
                        an all-time high in 2014 with an output of 6,165 metric tonnes. By 2015, the production of Grapefruits\
                        experienced a drastic decrease of about 8.5%. The year 2016 observed a negligible increase of production\
                        which shows that 2015-2016 was not the best year yet. From 2016-2018, Grapefruit farmers faced a decrease \
                        in production which suggests local markets were not satisfied.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='GrapeFruit Production in Africa.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container(
                    html.P(children='The total Grapefruits Production in Africa as at 2018 was 924,959 Metric Tonnes.\
                        Southern Africa experienced an influx of Grapefruit Production claiming about 53.4% of total Grapefruits\
                        produced in Africa. Northern Africa also experienced a decent production of about 344,000 metric tonnes.\
                        The worst performed region was Central Africa which contributed to about 2.25% of production that year.\
                        East Africa produced 40,000 metric tonnes which resulted in 4.3% of total Grapefruit Production in Africa.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            ),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart21',
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
                html.H2(children='GrapeFruit Area Harvested in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart22',
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
                    html.P(children='The analysis performed on the available data showed that Area that Grapefruit was \
                        harvested to be on a constant decrease from 2014 until 2018. From 2014 to 2015 experienced a drastic\
                        fall of area harvested with a 8.4 % decrease. Further investigation needs to be undertaken to fully\
                        understand the underlying reasons for the decline of the Area harvested in Somalia.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            )   
        ], className='row'),

        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H2(children='GrapeFruit Yield in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Container(
                    html.P(children='The analysis performed on the Yield of Grapefruits in Somalia showed a 1.2 % decrease\
                        from 2014 to 2015. From 2015 to 2018 there was a constant increase in the Yield.\
                        From 2015-2016 there was a 3.9% increase in the Yield of Grapefruits in Somalia and from 2016 to 2018\
                        Somalia experienced a 1% increase in the Yield of Grapefruits.',
                        style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            ),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart23',
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