
# external libraries
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import nltk
import json
import pandas as pd
import plotly.graph_objs as go
import plotly_express as px
import altair as alt


###########################################
# READ IN TEST DATA
###########################################

test_df = pd.read_csv('data/pm_kits.csv')
pollution_data = pd.read_csv('data/processed_data.csv')



###########################################
# PLOT FUNCTIONS
###########################################
def mds_special():
    font = "Arial"
    axisColor = "#000000"
    gridColor = "#DEDDDD"
    return {
        "config": {
            "title": {
                "fontSize": 24,
                "font": font,
                "anchor": "start", # equivalent of left-aligned.
                "fontColor": "#000000"
            },
            'view': {
                "height": 300, 
                "width": 400
            },
            "axisX": {
                "domain": True,
                "gridColor": gridColor,
                "domainWidth": 1,
                "grid": False,
                "labelFont": font,
                "labelFontSize": 12,
                "labelAngle": 0, 
                "tickColor": axisColor,
                "tickSize": 5, # default, including it just to show you can change it
                "titleFont": font,
                "titleFontSize": 16,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "X Axis Title (units)", 
            },
            "axisY": {
                "domain": False,
                "grid": True,
                "gridColor": gridColor,
                "gridWidth": 1,
                "labelFont": font,
                "labelFontSize": 14,
                "labelAngle": 0, 
                "titleFont": font,
                "titleFontSize": 16,
                "titlePadding": 10, # guessing, not specified in styleguide
                "title": "Y Axis Title (units)", 
            },
        }
    }


alt.data_transformers.enable('json')
#alt.themes.register('mds_special', mds_special)

def make_heatmap(data, pm = 2.5, width = 550):
    pm_filter = 'PM25' if pm == 2.5 else 'PM10'
    temp_data = data[data['PARAMETER'] == pm_filter]
    
    return alt.Chart(temp_data, title = f'Concentration of PM{pm} in BC').\
                mark_rect().\
                encode(
                    x=alt.X('index:O', title = 'date'),
                    y=alt.Y('STATION_NAME:O', title = ''),
                    color= alt.Color('RAW_VALUE:Q', legend=alt.Legend(title=f"Concentration of PM{pm}()")),
                    tooltip = [alt.Tooltip('index:O', title = 'Date:'),
                                alt.Tooltip('RAW_VALUE:N', title = 'Polution')]).\
                properties(
                    width=width,
                    height=250
                )

def make_lineplot(data, pm = 2.5, width = 550, init_locations=[]):
    pm_filter = 'PM25' if pm == 2.5 else 'PM10'
    temp_data = data[data['PARAMETER'] == pm_filter]
    
    initialize_selection = [{'STATION_NAME': location} for location in init_locations]
    
    brush = alt.selection_multi(init=initialize_selection)
    
    return alt.Chart(temp_data, title = f'Concentration of PM{pm} in given locations').\
                mark_line(width = 10).\
                encode(
                    x=alt.X('DATE_PST:O', title = 'date'),
                    y=alt.Y('RAW_VALUE', title = 'Concentration'),
                    color= alt.condition(brush, 'STATION_NAME', if_false=alt.value('lightgray')),
                    tooltip = [alt.Tooltip('index:O', title = 'Date:'),
                                alt.Tooltip('RAW_VALUE:N', title = 'Polution')]).\
                properties(
                    width=width,
                    height = 250
                ).add_selection(
                    brush
                )

def make_second_timeseries(data, location, pms = [2.5, 10], width = 550):
    temp_data = data[data['STATION_NAME'] == location]
    if len(pms) == 1:
        pm = pms[0]
        pm_filter = 'PM25' if pm == 2.5 else 'PM10'
        temp_data = temp_data[temp_data['PARAMETER'] == pm_filter]
    elif len(pms) == 0:
        temp_data = pd.DataFrame(columns = data.columns)
    
    return alt.Chart(temp_data, title = f'Concentration of selected PMs in {location}').\
                mark_line(width = 10).\
                encode(
                    x=alt.X('index:O', title = 'date'),
                    y=alt.Y('RAW_VALUE', title = 'Concentration()'),
                    color= alt.Color('PARAMETER'),
                    tooltip = [alt.Tooltip('index:O', title = 'Date:'),
                                alt.Tooltip('RAW_VALUE:N', title = 'Polution')]).\
                properties(
                    width=width,
                    height = 250
                )


def make_barchart(data, locations, pm = 2.5, width = 550):
    pm_filter = 'PM25' if pm == 2.5 else 'PM10'
    temp_data = data[data['STATION_NAME'].isin(locations)]
    temp_data = temp_data[temp_data['PARAMETER'] == pm_filter]
    
    
    return alt.Chart(temp_data, title = f'Distribution of concentration of PM{pm} in given locations').\
                mark_bar(fillOpacity = 0.5).\
                encode(
                    x=alt.X('RAW_VALUE', bin=alt.Bin(step=0.25), title = 'Concentration()'),
                    y = alt.Y('count()',
                              stack = None,
                              title = 'Frequency'),
                    color = alt.Color('STATION_NAME', title='Locations')
                    ).\
                properties(
                    width=width,
                    height = 250
                )

# USAGE EXAMPLES
# df = pd.read_csv('temp_data/processed_data.csv')
# df_temp = df[df['STATION_NAME'].str.startswith('Vancouver')]
# 
# make_heatmap(df_temp, 10)
# 
# locations = ["Vancouver International Airport #2"]
# make_lineplot(df_temp, init_locations=locations)
# 
# make_second_timeseries(df_temp, location = "Vancouver Kitsilano")
# 
# make_barchart(df_temp, ["Vancouver Kitsilano", "Vancouver International Airport #2"])

###########################################
# STATIC PLOTS FOR DASHBOARD DRAFT
###########################################

# srcDoc = make_plot().to_hmtl()




###########################################
# APP LAYOUT
###########################################

# COLOUR AND STYLE
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {"white": "#ffffff",
          "light_grey": "#d2d7df",
          "banner_blue": "#00ccff",
          "box1blue": "#e6f5ff",
          "box2green": "#e6ffe6",
          "box3yellow": "#ffffcc",
          "box4purple": "#eeccff",
          "black": "#000000"
          }


# APP LAYOUT
app.layout = html.Div(style={'backgroundColor': colors['white']}, children=[
    # HEADER
    html.Div(className="row", style={'backgroundColor': colors['banner_blue'], 'border': '1px solid', "padding-left": 5}, children=[
        html.H3('Pollutants Matter BC – visualization of particulate matter concentrations',
                style={'color':colors['black'], 'margin-top':2, 'margin-bottom':2})
    ]),
    
    
    # BOXES 1 & 2 AND CHARTS 1 & 2
    html.Div(className="row", children=[
    
        # SIDEBAR
        html.Div(className="two columns", style={'backgroundColor': colors['light_grey'], 'padding': 0}, children=[

            #BOX1 BLUE
            html.Div(className="row",  style={'backgroundColor': colors['box1blue'], 
                'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':10,'border': '1px solid'}, children=[
                html.P("Chart 1 controls:\nPollutant:\n"),
                
                dcc.Dropdown(
                    options=[
                        {'label': 'PM2.5', 'value': 'PM2.5'},
                        {'label': 'PM10', 'value': 'PM10'}
                    ],
                    
                    value='MTL'
                ),

                html.P("Location:\n", style={'padding-top':10}),
                
                dcc.Dropdown(
                    options=[
                        {'label':k , 'value': k } for k in pollution_data['STATION_NAME'].unique()
                    ],
                    multi = True,
                    value='MTL'
                )    
                
                ]),

            #BOX2 GREEN
            html.Div(className="row",  style={'backgroundColor': colors['box2green'], 
                'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':10, 'border': '1px solid'}, children=[
            html.P("Chart 2 controls:\nPollutant:\n"),
            
            dcc.Dropdown(
                    options=[
                        {'label': 'PM2.5', 'value': 'PM2.5'},
                        {'label': 'PM10', 'value': 'PM10'}
                    ],
                    value='MTL'
                ),

                html.P("Location:\n", style={'padding-top':5}),
                
                dcc.Dropdown(
                    options=[
                        {'label': 'Vancouver', 'value': 'Vancouver'},
                        {'label': 'Surrey', 'value': 'Surrey'},
                        {'label': 'Burnaby', 'value': 'Burnaby'}
                    ],
                    value='MTL'
                )   ])
        ]),


        ###########################################
        # CHART 1
        ###########################################



        html.Div(className='five columns', style={"backgroundColor": colors['white'], 'margin-left':10, 'margin-right':10, "padding": 0}, children=[
            
            html.Div(className="row", children=[
                html.H6("Chart 1: Multi-location, pollutant map", style={"backgroundColor": colors['box1blue'], 'border': '1px solid', 'text-align': 'center', 'padding-left':5}),
                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot1',
                    height='300',
                    width='550',
                    style={'border-width': '0'},

                    ################ The magic happens here
                    srcDoc= make_lineplot(test_df, pm = 2.5, width = 370,init_locations=['Vancouver Kitsilano']).to_html()
                    ################ The magic happens here
                    ),
            ])
        ]),

        ###########################################
        # CHART 2
        ###########################################
        html.Div(className='five columns', style={"backgroundColor": colors['white'], 'text-align': 'center', 'margin-left':10, 'margin-right':0, "padding": 0}, children=[
            
            html.Div(className="row",  children=[
                html.H6("Chart 2: Multi-pollutant, location map", style={"backgroundColor": colors['box2green'], 'border': '1px solid','padding-left':5}),

                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot2',
                    height='300',
                    width='550',
                    style={'border-width': '0'},

                    ################ The magic happens here
                    srcDoc= make_second_timeseries(test_df, 'Vancouver Kitsilano', pms = [2.5, 10], width = 380).to_html()
                    ################ The magic happens here
                    )
                ])
            
        ])
    ]),

    # BOXES 3 & 4 AND CHARTS 3 & 4
    html.Div(className="row", children=[
    
        # SIDEBAR
        html.Div(className="two columns", style={'backgroundColor': colors['light_grey'], 'padding': 0}, children=[

            #BOX3 YELLOW
            html.Div(className="row",  style={'backgroundColor': colors['box3yellow'], 
                'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':10, 'border': '1px solid'}, children=[
            html.P("Chart 3 controls:\nPollutant:\nLocation:\n "),
            
            
            dcc.Dropdown(
                    options=[
                        {'label': 'PM2.5', 'value': 'PM2.5'},
                        {'label': 'PM10', 'value': 'PM10'}
                    ],
                    value='MTL'
                ),

                html.P("Location:\n", style={'padding-top':5}),
                
                dcc.Dropdown(
                    options=[
                        {'label': 'Vancouver', 'value': 'Vancouver'},
                        {'label': 'Surrey', 'value': 'Surrey'},
                        {'label': 'Burnaby', 'value': 'Burnaby'}
                    ],
                    multi=True,
                    value='MTL'
                )   ]),

            #BOX4 PURPLE
            html.Div(className="row",  style={'backgroundColor': colors['box4purple'], 
                'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':90, 'border': '1px solid'}, children=[
                html.P("Chart 4 controls:\nPollutant:\n "),
                
                dcc.Dropdown(
                        options=[
                            {'label': 'PM2.5', 'value': 'PM2.5'},
                            {'label': 'PM10', 'value': 'PM10'}
                        ],
                        value='MTL'
                    )])
        ]),


        ###########################################
        # CHART 3
        ###########################################
        html.Div(className='five columns', style={"backgroundColor": colors['white'], 'margin-left':10, 'margin-right':10, "padding": 0}, children=[
            
            html.Div(className="row",  children=[
                html.H6("Chart 3: Histograms chart", style={"backgroundColor": colors['box3yellow'], 'border': '1px solid', 'text-align': 'center',"padding-left": 5}),

                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot3',
                    height='300',
                    width='550',
                    style={'border-width': '0'},

                    ################ The magic happens here
                    srcDoc= make_barchart(test_df, ['Vancouver Kitsilano'], pm = 2.5, width = 400).to_html()
                    ################ The magic happens here
                    )
                ])
            
        ]),

        ###########################################
        # CHART 4
        ###########################################
        html.Div(className='five columns', style={"backgroundColor": colors['white'], 'text-align': 'center', 'margin-left':10, 'margin-right':0,"padding": 0}, children=[
            
            html.Div(className="row",  children=[
                html.H6("Chart 4: Heatmap chart", style={"backgroundColor": colors['box4purple'], 'border': '1px solid', "padding-left": 5}),

                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot4',
                    height='300',
                    width='550',
                    style={'border-width': '0'},

                    ################ The magic happens here
                    srcDoc= make_heatmap(test_df, pm = 2.5, width = 340).to_html()
                    ################ The magic happens here
                    )
                ])
            
        ])
    ]),
    
    

    # BOX 5
    html.Div(className="row", children=[

        #BOX5 DATE CONTROLLER
        html.Div(className="row",  style={'backgroundColor': colors['light_grey'], 'padding-bottom':30, 'padding-left':10,  'border': '1px solid'}, children=[
            html.P("Date control slider", style={'padding-top':0}),
            dcc.RangeSlider(
                marks={i: '{}'.format(i) for i in range(2000, 2017)},
                min=2000,
                max=2017,
                value=[2000, 2017]
            )   ])

    ])
    
  

    
])


if __name__ == '__main__':
    app.run_server(debug=True)