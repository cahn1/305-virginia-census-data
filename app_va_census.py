import json
import dash
from urllib.request import urlopen

import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from util import util as u

# Global variables
tabtitle = 'Virginia Counties'
sourceurl = 'https://www.kaggle.com/muonneutrino/us-census-demographic-data'
githublink = 'https://github.com/cahn1/305-virginia-census-data/tree/update1'
# options = [
#     'TotalPop', 'Men', 'Women', 'Hispanic', 'White', 'Black', 'Native',
#     'Asian', 'Pacific', 'VotingAgeCitizen', 'Income', 'IncomeErr',
#     'IncomePerCap', 'IncomePerCapErr', 'Poverty', 'ChildPoverty',
#     'Professional', 'Service', 'Office', 'Construction', 'Production',
#     'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp', 'WorkAtHome',
#     'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork', 'SelfEmployed',
#     'FamilyWork', 'Unemployment', 'RUCC_2013']

url = 'https://raw.githubusercontent.com/plotly/datasets/master/' \
      'geojson-counties-fips.json'

with urlopen(url) as response:
    counties = json.load(response)

# https://www.geeksforgeeks.org/dataframe-read_pickle-method-in-pandas/
df = pd.read_pickle('resources/va-stats.pkl')

print(f'cahn0={df}')
s1 = df['FIPS'].sample(5)
print(f'df["FIPS"].sample(5)={s1}')
print(f'df.columns={df.columns}')

options = u.pick_options(df)
print(f'cahn4={options}')

# app server config
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

# app component layout
app.layout = html.Div(children=[
    html.H1('Virginia Census Data 2017'),
    html.Div(children=[
        # left side
        html.Div([
            html.H6('Select census variable:'),
            dcc.Dropdown(
                id='stats-drop',
                options=[{'label': i, 'value': i} for i in options],
                value='MeanCommute'
            ),
        ],
        className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='va-map')],
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
    Output('va-map', 'figure'),
    [Input('stats-drop', 'value')])
def display_results(option):
    valmin = df[option].min()
    valmax = df[option].max()
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=counties,
            locations=df['FIPS'],
            z=df[option],
            colorscale='oxy',
            text=df['County'],
            zmin=valmin,
            zmax=valmax,
            marker_line_width=0))
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5.8,
        mapbox_center = {"lat": 38.0293, "lon": -79.4428})
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # https://community.plot.ly/t/what-colorscales-are-available-in-plotly-and
    # -which-are-the-default/2079
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
