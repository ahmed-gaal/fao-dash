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
    
data = pd.read_csv('data/beans.csv')
colors = ['#133F54','#29AEB4','#B3CBB9','#F14B5B','#CA2E44']
fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = ar[ar['Item'] == 'Beans, dry'].Y2018.sum(),
    title = {
        "text": "Area Harvested<br><span style='font-size\
                :0.8em;color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Hectares</span>"
    },
    delta = {
        'reference': ar[ar['Item'] == 'Beans, dry'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0, 0.5], 'y': [0.5, 0]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = pdd[pdd['Item'] == 'Beans, dry'].Y2018.sum(),
    title = {
        "text": "Production<br><span style='font-size:0.8em;\
                color:gray'>in</span><br><span style='font-size\
                :0.8em;color:gray'>Tonnes</span>"
    },
    delta = {
        'reference': pdd[pdd['Item'] == 'Beans, dry'].Y2017.sum(),\
            'relative': True
    },
    domain = {'x': [0.5, 1], 'y': [0, 1]}))

fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = yy[yy['Item'] == 'Beans, dry'].Y2018.sum() / 10000,
    title = {
        "text": "Yield<br><span style='font-size:0.8em\
                ;color:gray'>in</span><br><span style='font-size:0.8em\
                ;color:gray'>Tonne per Hectare</span>"
    },
    delta = {
        'reference': yy[yy['Item'] == 'Beans, dry'].Y2017.sum()/10000,\
            'relative': True
    },
    domain = {'x': [0.5, 0], 'y': [1, 0.5]}))

fig1 = dd.bar_graph(x='Years', y='Area harvested', xTitle='Area harvested', yTitle='Years',
                 title='Area Harvested (Hectares)', how='h', colors='#914F9A', item='Beans, dry')

fig2 = dd.line_graph(x='Years', y='Production', xTitle='Years', yTitle='Tonnes',
                  colors='#AD1A31',how='spline', mode='lines', item='Beans, dry',
                  title='Beans Production in Somalia from 2014 - 2018')

fig3 = px.scatter_mapbox(dd.total_element('production', 'Beans, dry'), lat='Lat',
                         lon='Lon', color='Total', hover_name='Area', size = 'Total',
                         hover_data={'Lat':False, 'Lon':False}, labels = {'Area':'Element'},
                         color_continuous_scale=colors, zoom=1.4, width=1900, height=700,
                         template='presentation', center=None, mapbox_style='light',
                         title='Global Banana Production in Tonnes(2014-2018)')

fig4 = data[data['Element'] == 'Production'].iplot(asFigure = True, kind = 'pie',
                                                   labels = 'Area', values = 'Y2018',
                                                   legend = False,textinfo = 'label+percent',
                                                   theme = 'polar', hole = .6, linecolor = 'white',
                                                   colors = colors, linewidth = .5,
                                                   title = 'Beans Production in Africa as at 2018')

fig5 = dd.line_graph(x='Years', y='Yield', xTitle='Years', yTitle='Tonne per hectare',
                  title='Beans Yield for Somalia (2014 - 2018)', mode='lines+markers',
                  scale='piyg', how='spline', item='Beans, dry')

layout = html.Div([
    dbc.Container([
        dbc.Row([
                dbc.Col(html.H1('World Beans Statistics as at 2018', className='text-center'), className='mb-4 mt-5')
            ]),
        dbc.Row(
            dbc.Col(html.Div([
                    dcc.Graph(id = 'Chart6',
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
                    dcc.Graph(id = 'Chart7',
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
                html.H2(children='Beans Production in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),

        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart8',
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
                    html.P(children='The analysis performed on the data shows a steady and constant increase\
                        in the Production of Dry Beans. From 2014 to 2015 we observe a 3.1% increase in Production.\
                        Keeping in mind the unforgiving drought and famine of 2015 to 2016, there was a 0.1% increase\
                        in Production which is a positive result.\
                        From 2017 throughout was smooth sailing for Beans producers as there was 2.9% increase in production.\
                        The conclusion derived was that 2018 was the best year yet for Beans Producers.', style={
                            'font-family': 'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            )
        ], className='row'),
        html.Hr(),

        dbc.Row([
            dbc.Col(
                html.H2(children='Beans Production in Africa.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),

        dbc.Row([
            dbc.Col(
                dbc.Container(
                    html.P(children='This analysis performed shows the Beans Production to be prevalent in Africa.\
                        East Africa is observed to be the highest producers of beans. With a total of 4.8 million \
                        metric tonnes produced as at 2018, East Africa claimed almost 70% of the Beans Production in Africa.\
                        West, North and Southern Africa together produced almost 15% of Beans in Africa.\
                        This shows that East Africa has a conducive environment for Beans Production.',
                        style={
                            'font-family':'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            ),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart9',
                                figure = fig4,
                                responsive = True,
                                animate = True,
                                config = {
                                    'showTips': True,
                                    'displaylogo': False
                                })
            ], style = {'font-variant':'small-caps','font-weight':'bold'}), width=6, align = 'center'),
        ]),
        html.Hr(),
        
        dbc.Row([
            dbc.Col(
                html.H2(children='Beans Area Harvested in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),

        dbc.Row([
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart10',
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
                    html.P(children='The analysis performed shows that from 2014 to 2018 the Area from which beans \
                        was harvested at a total of 431,719 hectares. Between 2015 to 2016 there was drought and famine\
                        experienced in Somalia which resulted in a 0.1% decrease of Area harvested. From there onwards\
                        the analysis performed observed a 1.5% increase in Area harvested.', style={
                            'font-family':'Overpass, sans-serif', 'font-size':'210%', 'font-weight':'normal'
                        })
                ), width=6
            )
        ], className='row'),
        html.Hr(),

        dbc.Row([
            dbc.Col(
                html.H2(children='Beans Yield in Somalia.', style={
                'font-family':'Overpass, sans-serif', 'font-size':'200%', 'font-weight':'bold'
            }),
                width={'size':6, 'offset':4}
            )
        ], className='row'),
        html.Hr(),

        dbc.Row([
            dbc.Col(
                dbc.Container(
                    html.P(children='The analysis performed on the data shows that as at 2014, the Yield of Beans was at an all\
                        time high of 0.305 tonnes per hectare. By 2015, the Yield dropped exponentially by 3.7%. This was due to\
                        mitigating factors such as famine and the already crippled security situation in Somalia. From 2016, the Yield\
                        of beans was on an averag increase of 0.7%.\
                        The conclusion arrived at during the course of this analysis was the beans is a cash crop and has a high market value locally.',
                        style={
                            'font-family':'Overpass, sans-serif', 'font-weight':'normal', 'font-size':'210%'
                        })
                ), width=6
            ),
            dbc.Col(html.Div([
                        dcc.Graph(id = 'Chart11',
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