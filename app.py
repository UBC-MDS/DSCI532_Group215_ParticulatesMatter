 
# external libraries
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly_express as px
import altair as alt
from src import utils

alt.data_transformers.disable_max_rows()

###########################################
# READ IN DATASET
###########################################


pm_df = pd.read_csv('data/processed_data.csv')
avg_df = pd.read_csv('data/processed_baseline_data.csv')

Plotter = utils.PlotsCreator(pm_df, avg_df)

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


# def chart1_wrapper(pollutant1,location1, daterange):
#     return Plotter.location_linechart(pm = pollutant1, init_locations= location1,height = 220, width = 320, 
#                                                 start_date = str(daterange[0])+'-01-01', end_date= str(daterange[1])+'-01-01').to_html()

# APP LAYOUT
app.layout = html.Div(style={'backgroundColor': colors['white']}, children=[
    # HEADER
    html.Div(className="row", style={'backgroundColor': colors['banner_blue'], 'border': '1px solid', "padding-left": 5}, children=[
        html.H3('Pollutants Matter BC – visualization of particulate matter concentrations (weighted monthly averages)',
                style={'color':colors['black'], 'margin-top':2, 'margin-bottom':2}),
        html.H6('Data is attributed to the BC Ministry of Environment and Climate Change Strategy',
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
                    id = 'pollutant1',
                    options=[
                        {'label': 'PM2.5', 'value': 2.5},
                        {'label': 'PM10', 'value': 10}
                    ],
                    
                    value=2.5,
                    clearable = False
                ),

                html.P("Location:\n", style={'padding-top':10}),
                
                dcc.Dropdown(
                    id = 'location1',
                    options=[
                        {'label':k , 'value': k } for k in pm_df['STATION_NAME'].unique()
                    ],
                    multi = True,
                    value='Vancouver'
                )    
                
                ]),

            #BOX2 GREEN
            html.Div(className="row",  style={'backgroundColor': colors['box2green'], 
                'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':100, 'border': '1px solid'}, children=[
            # html.P("Chart 2 controls:\nPollutant:\n"),
            
            # dcc.Dropdown(
            #         options=[
            #             {'label': 'PM2.5', 'value': 'PM2.5'},
            #             {'label': 'PM10', 'value': 'PM10'}
            #         ],
            #         value='MTL'
            #     ),

                html.P("Location:\n", style={'padding-top':5}),
                
                dcc.Dropdown(
                    id = 'location2',
                    options=[
                        {'label':k , 'value': k } for k in pm_df['STATION_NAME'].unique()
                    ],
                    value=pm_df['STATION_NAME'].unique()[0],
                    clearable = False
                )

                
                
                   ])
        ]),


        ###########################################
        # CHART 1
        ###########################################



        html.Div(className='five columns', style={"backgroundColor": colors['white'], 'margin-left':10, 'margin-right':10, "padding": 0}, children=[
            
            html.Div(className="row", children=[
                html.H6("Chart 1: Concentration of PM2.5 for given locations"  , id = 'plot1_title', style={"backgroundColor": colors['box1blue'], 'border': '1px solid', 'text-align': 'center', 'padding-left':5}),
                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot1',
                    height='300',
                    width='550',
                    style={'border-width': '0'},

                    ################ The magic happens here
                    srcDoc= Plotter.location_linechart(pm = 2.5, init_locations=["Vancouver"],width=400, height = 250, daterange=[2005,2010]).to_html()
                    ################ The magic happens here
                    ),
            ])
        ]),

        ###########################################
        # CHART 2
        ###########################################
        html.Div(className='five columns', style={"backgroundColor": colors['white'], 'text-align': 'center', 'margin-left':10, 'margin-right':0, "padding": 0}, children=[
            
            html.Div(className="row",  children=[
                html.H6("Chart 2: Pollutant Concentration in Abbotsford", id = "plot2_title", style={"backgroundColor": colors['box2green'], 'border': '1px solid','padding-left':5}),

                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot2',
                    height='300',
                    width='550',
                    style={'border-width': '0'},

                    ################ The magic happens here
                    srcDoc= Plotter.pm_linechart("Vancouver", pms = [2.5, 10], height = 250, width = 300, daterange=[2000,2017]).to_html()
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
            html.P("Chart 3 controls:\nPollutant:\n"),
            
            
            dcc.Dropdown(
                    id = 'pollutant3',
                    options=[
                        {'label': 'PM2.5', 'value': 2.5},
                        {'label': 'PM10', 'value': 10}
                    ],
                    value = 2.5,
                    clearable = False
                ),

                html.P("Location:\n", style={'padding-top':5}),
                
                dcc.Dropdown(
                    id = 'location3',
                    options=[
                        {'label':k , 'value': k } for k in pm_df['STATION_NAME'].unique()
                    ],
                    multi=True,
                    value = list(pm_df['STATION_NAME'].unique()[0:2])
                )   ]),

            #BOX4 PURPLE
            html.Div(className="row",  style={'backgroundColor': colors['box4purple'], 
                'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':90, 'border': '1px solid'}, children=[
                html.P("Chart 4 controls:\nPollutant:\n "),
                
                dcc.Dropdown(
                    id = 'pollutant4',
                        options=[
                            {'label': 'PM2.5', 'value': 2.5},
                            {'label': 'PM10', 'value': 10}
                        ],
                        value = 2.5,
                        clearable = False
                    )])
        ]),


        ###########################################
        # CHART 3
        ###########################################
        html.Div(className='five columns', style={"backgroundColor": colors['white'], 'margin-left':10, 'margin-right':10, "padding": 0}, children=[
            
            html.Div(className="row",  children=[
                html.H6("Chart 3: Distribution of PM2.5 Concentrations for BC Cities", id = 'plot3_title', style={"backgroundColor": colors['box3yellow'], 'border': '1px solid', 'text-align': 'center',"padding-left": 5}),

                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot3',
                    height='300',
                    width='550',
                    style={'border-width': '0'},

                    ################ The magic happens here
                    srcDoc= Plotter.make_barchart(["Abbotsford"], pm = 2.5, width = None, height = 250).to_html()
                    ################ The magic happens here
                    )
                ])
            
        ]),

        ###########################################
        # CHART 4
        ###########################################
        html.Div(className='five columns', style={"backgroundColor": colors['white'], 'text-align': 'center', 'margin-left':10, 'margin-right':0,"padding": 0}, children=[
            
            html.Div(className="row",  children=[
                html.H6("Chart 4: PM2.5 Concentration Heatmap", id = "plot4_title", style={"backgroundColor": colors['box4purple'], 'border': '1px solid', "padding-left": 5}),

                html.Iframe(
                    sandbox='allow-scripts',
                    id='plot4',
                    height='300',
                    width='550',
                    style={'border-width': '0'},

                    ################ The magic happens here
                    srcDoc = Plotter.make_heatmap(pm = 2.5, width = 340, height = 250, daterange=[2000,2017]).to_html()
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
                id = 'daterange',
                marks={i: '{}'.format(i) for i in range(2000, 2017)},
                step = None,
                min=2000,
                max=2017,
                value=[2008, 2010]
            )   ])

    ])
])


@app.callback(
    [dash.dependencies.Output('plot1', 'srcDoc'),
    dash.dependencies.Output('plot1_title', 'children')],
    [dash.dependencies.Input('pollutant1', 'value'),
     dash.dependencies.Input('location1', 'value'),
     dash.dependencies.Input('daterange', 'value')])
def update_plot1(pollutant1, location1, daterange):

    if type(location1) == str:
        location1 = [location1]

    #pdated_plot = make_plot(xaxxis_column_name, yaxis_column_name)).to_html()
    updated_plot1 = Plotter.location_linechart(pm = pollutant1, init_locations= location1, height = 220, width = 320).to_html()
    updated_title1 = "Chart 1: PM" + str(pollutant1) +" concentration for BC Cities"
    return updated_plot1, updated_title1


@app.callback(
    [dash.dependencies.Output('plot2', 'srcDoc'),
    dash.dependencies.Output('plot2_title', 'children')],
    [dash.dependencies.Input('location2', 'value')])

def update_plot2(location2, daterange):


    updated_plot2 = Plotter.pm_linechart(location =location2, pms = [2.5, 10], height = 220, width = 400, daterange=daterange).to_html()
    updated_title2 = "Chart 2: Pollutant Concentration in " + str(location2) 
    
    return updated_plot2, updated_title2



@app.callback(
    [dash.dependencies.Output('plot3', 'srcDoc'),
    dash.dependencies.Output('plot3_title', 'children')],
    [dash.dependencies.Input('location3', 'value'),
     dash.dependencies.Input('pollutant3', 'value'),
     dash.dependencies.Input('daterange', 'value')])

def update_plot3(location3, pollutant3, daterange):

    updated_plot3 = Plotter.make_barchart(location3, pm = pollutant3, width = 350, height = 220, daterange=daterange).to_html()
    updated_title3 = "Chart 3: Distribution of PM" + str(pollutant3) + " Concentration for BC Cities"
    return updated_plot3, updated_title3

@app.callback(
    [dash.dependencies.Output('plot4', 'srcDoc'),
    dash.dependencies.Output('plot4_title', 'children')],
    [dash.dependencies.Input('pollutant4', 'value')])

def update_plot4(pollutant4, daterange):


    updated_plot4 = Plotter.make_heatmap(pm = pollutant4, width = 280, height = 220, daterange=daterange).to_html()
    updated_title4 = "Chart 4: PM" + str(pollutant4) + " Concentration Heatmap"
    return updated_plot4, updated_title4



if __name__ == '__main__':
    app.run_server(debug=True)
