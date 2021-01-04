"""The following is a base class for all methods used in this application."""
import pandas as pd
import numpy as np
import cufflinks

dff = pd.read_excel('data/dff.xlsx')
world = pd.read_excel('data/world.xlsx')

class Dashboard:

    """Create a class for all functions used in the project."""

    
    def __init__(self):
        """Initialzing the class."""

    
    def confirm_option_value(value, dataframe):
        """Method for extracting element from the dataframe"""
        if value == 'area':
            ar = dataframe[dataframe['Element'] == 'Area harvested']
            return ar
        elif value == 'yield':
            y = dataframe[dataframe['Element'] == 'Yield']
            y['Total'] = y['Total'] / 10000
            return y
        elif value == 'production':
            return dataframe[dataframe['Element'] == 'Production']


    def world_clean(value, drop):
        """Cleaning the dataset"""
        world1 = world.drop(drop, axis=1)
        total = world1.sum(axis=1)
        world1['Total'] = total
        final = Dashboard.confirm_option_value(value, world1)
        return final

    
    def country_info(country, item=None):
        """Function for producing country information"""
        
        # Selecting specific country
        som = dff[dff['Area'] == country]
        lat = som['Lat']
        lon = som["Lon"]
        somm = som.drop(['Lat', 'Lon'], axis=1)
        # Summing up the totals
        total = somm.sum(axis=1)
        somm['Total'] = total
        somm['Lat'] = lat
        somm['Lon'] = lon
        # ruling out specific item
        itm = somm[somm['Item'] == item]
        years = ['Y2014', 'Y2015', 'Y2016', 'Y2017', 'Y2018']
        new_df = itm.groupby('Element')[years].sum().transpose()
        new_df['Years'] = years
        new_df['Yield'] = new_df['Yield'] / 10000
        return new_df


    def total_element(value=None, item=None):
        """Function for producing crop information"""
        
        # Selecting specific item
        lot = dff[dff['Item'] == item]
        lat = lot['Lat']
        lon = lot["Lon"]
        ittem = lot.drop(['Lat', 'Lon'], axis=1)
        # Summing up the totals
        total = ittem.sum(axis=1)
        ittem['Total'] = total
        ittem['Lat'] = lat
        ittem['Lon'] = lon
        # Filtering elements
        return Dashboard.confirm_option_value(value, ittem)


    def bar_graph(x, y, xTitle, yTitle, title, how, colors, item=None):
        df = Dashboard.country_info('Somalia', item=item)
        fig = df.iplot(asFigure=True, kind='bar', x=x, y=y, yTitle=yTitle,
                    xTitle=xTitle, theme='polar', subplots=True,
                    subplot_titles=True, title=title, colors=colors,
                    orientation=how)
        return fig

    
    def line_graph(x, y, xTitle, yTitle, title, mode, how, item=None, colors=None, scale=None):
        df = Dashboard.country_info('Somalia', item=item)
        fig = df.iplot(asFigure=True, kind='scatter', mode=mode,
                    x=x, y=y, xTitle=xTitle, yTitle=yTitle,
                    subplots=True, subplot_titles=True, theme='polar',
                    interpolation=how, title=title, colorscale=scale)
        return fig


