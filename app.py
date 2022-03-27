import json
import dash
from urllib.request import urlopen

import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from util import util as u

# TODO: Below is good reference
# Refer https://towardsdatascience.com/mapping-us-census-data-with-python-607df3de4b9c
# https://plotly.com/python/mapbox-county-choropleth/
# https://plotly.com/python/county-choropleth/ -> zill(5) as well

# Global variables
tabtitle = 'Virginia Counties'
sourceurl = 'https://www.kaggle.com/muonneutrino/us-census-demographic-data?select=acs2017_census_tract_data.csv'
githublink = 'https://github.com/cahn1/305-virginia-census-data/tree/update1'
url = 'https://raw.githubusercontent.com/plotly/datasets/master/' \
      'geojson-counties-fips.json'

with urlopen(url) as response:
    counties = json.load(response)

# https://www.geeksforgeeks.org/dataframe-read_pickle-method-in-pandas/
# add 'FIPS' column to df:
# http://students.washington.edu/ayandm/tutfiles/FIPSConversion.pdf
df = pd.read_csv('assets/census/acs2017_census_tract_data.csv')
df = df.drop(labels=range(300000, 74000), axis=0)
df['FIPS'] = df['County'].apply(u.pick_fip)
options = u.pick_options(df)

# app server config
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

# app component layout
app.layout = html.Div(children=[
    html.H1('US Census Demographic Data 2017'),
    html.Div(children=[
        # left side
        html.Div([
            html.H6('Select census variable:'),
            dcc.Dropdown(
                id='stats-drop',
                options=[{'label': i, 'value': i} for i in options],
                value='Carpool'
            ),
        ],
            className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='us-map')],
            className='nine columns'
        ),
    ],
        className='twelve columns'),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),]
)

# callback
@app.callback(
    Output('us-map', 'figure'),
    [Input('stats-drop', 'value')])
def display_results(option):
    min_value = df[option].min()
    max_value = df[option].max()
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=counties,
            locations=df['FIPS'],
            z=df[option],
            colorscale='teal',
            text=df['County'],
            zmin=min_value,
            zmax=max_value,
            showlegend=True,
            marker_line_width=0))
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3.0,
        # https://docs.mapbox.com/playground/geocoding/?search_text=-98
        # .62651607972974,40.33851776440284&types=place%2Cpostcode%2Caddress&limit=1
        mapbox_center={"lat": 37.0902, "lon": -95.7129})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # https://community.plot.ly/t/what-colorscales-are-available-in-plotly-and
    # -which-are-the-default/2079

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
