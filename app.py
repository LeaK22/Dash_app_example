
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

data = pd.read_csv('nama_10_gdp_1_Data.csv', error_bad_lines = False, engine = 'python', na_values = [':', 'NaN'])

eu_values = [
    'European Union (current composition)',
    'European Union (without United Kingdom)',
    'European Union (15 countries)',
    'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
    'Euro area (19 countries)',
    'Euro area (12 countries)'
            ]

eu_filter = data['GEO'].isin(eu_values)

data = data.loc[~eu_filter.values].reset_index(drop = True)
data['NA_ITEM_UNIT'] = data['NA_ITEM'] + ' (' + data['UNIT'] + ')'

available_indicators = data['NA_ITEM_UNIT'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )],
        style={'width': '48%', 'display': 'inline-block'}), 
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            )],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'), 
    dcc.Slider(
        id='year--slider',
        min=data['TIME'].min(),
        max=data['TIME'].max(),
        value=data['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in data['TIME'].unique()}
    )
])

@app.callback( 
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    
    dff = data[data['TIME'] == year_value] #firstfiltering here by year
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM_UNIT'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM_UNIT'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM_UNIT'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
    
    
    
    
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

data = pd.read_csv('nama_10_gdp_1_Data.csv', error_bad_lines = False, engine = 'python', na_values = [':', 'NaN'])

eu_values = [
    'European Union (current composition)',
    'European Union (without United Kingdom)',
    'European Union (15 countries)',
    'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
    'Euro area (19 countries)',
    'Euro area (12 countries)'
            ]

eu_filter = data['GEO'].isin(eu_values)

data = data.loc[~eu_filter.values].reset_index(drop = True)
data['NA_ITEM_UNIT'] = data['NA_ITEM'] + ' (' + data['UNIT'] + ')'

available_indicators = data['NA_ITEM_UNIT'].unique()
available_countries= data['GEO'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            html.P(
                children = 'Select a country:',
                style = {'font-size': 15}
            ),
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Spain'
            )],
        style={'width': '48%', 'display': 'inline-block'}), 
        
        html.Div([
            html.P(
                children = 'Select an indicator:',
                style = {'font-size': 15}
            ),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            )],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
            ), 
    
    dcc.Graph(id='indicator-graphic'), 
    dcc.Slider(
        id='year--slider',
        min=data['TIME'].min(),
        max=data['TIME'].max(),
        value=data['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in data['TIME'].unique()}
    )  
    
    ]) ])

@app.callback( 
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('country', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(country_name, yaxis_column_name,
                 year_value):
    
    dff = data[data['TIME'] == year_value] #firstfiltering here by year
    
    
    return {
        'data': [go.Scatter(
            x=dff[dff['GEO'] == country_name]['Value'],
            y=dff[dff['NA_ITEM_UNIT'] == yaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': country_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

