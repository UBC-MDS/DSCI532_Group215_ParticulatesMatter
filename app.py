
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
app.config['suppress_callback_exceptions'] = True
server = app.server

colors = {"white": "#ffffff",
          "light_grey": "#d2d7df",
          "box1blue": "#8BBEE8FF ",
          "box2green": "#A8D5BAFF",
          "box3blue": "#8BBEE8FF",
          "box4purp": "#ccccff",
          "black": "#000000"
          }

# TODO - move to separate file
# BOXES 1 & 2 AND CHARTS 1 & 2
joint_view_div =[
html.Div(className="row", children=[

    # SIDEBAR
    html.Div(className="two columns", style={'backgroundColor': colors['light_grey'], 'padding': 0}, children=[

        #BOX1 BLUE
        html.Div(className="row",  style={'backgroundColor': colors['box1blue'],
            'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':200,'border': '1px solid'}, children=[
            html.P("Charts 1 & 2 controls:\nPollutant:\n"),

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
                height='290',
                width='550',
                style={'border-width': '0'},

                ################ The magic happens here
                srcDoc= Plotter.location_linechart(pm = 2.5, init_locations=["Vancouver"],width=400, height = 220, daterange=[2005,2010]).to_html()
                ################ The magic happens here
                ),
        ])
    ]),

    ###########################################
    # CHART 2
    ###########################################
    html.Div(className='five columns', style={"backgroundColor": colors['white'], 'text-align': 'center', 'margin-left':10, 'margin-right':0, "padding": 0}, children=[

        html.Div(className="row",  children=[
            
            html.H6("Chart 3: Distribution of PM2.5 Concentrations for BC Cities", id = 'plot3_title', style={"backgroundColor": colors['box3blue'], 'border': '1px solid', 'text-align': 'center',"padding-left": 5}),

            html.Iframe(
                sandbox='allow-scripts',
                id='plot3',
                height='300',
                width='550',
                style={'border-width': '0'},

                ################ The magic happens here
                srcDoc= Plotter.make_barchart(["Abbotsford"], pm = 2.5, width = 400, height = 220, daterange=[2000,2017]).to_html()
                # srcDoc= Plotter.make_barchart(["Abbotsford"], pm = 2.5, width = None, height = 250, daterange=[2000,2017]).to_html()
                ################ The magic happens here
                )
            ])

    ])
  ]),

# BOXES 3 & 4 AND CHARTS 3 & 4
html.Div(className="row", children=[

    # SIDEBAR
    html.Div(className="two columns", style={'backgroundColor': colors['light_grey'], 'padding': 0}, children=[

       #BOX2 GREEN
        html.Div(className="row",  style={'backgroundColor': colors['box2green'],
            'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':80, 'border': '1px solid'}, children=[
        html.P("Chart 3 controls:"),

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
                value="Vancouver",
                clearable = False
            )]),


        #BOX4 PURPLE
        html.Div(className="row",  style={'backgroundColor': colors['box4purp'],
            'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':120, 'border': '1px solid'}, children=[
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
            html.H6("Chart 3: Pollutant Concentration in Vancouver", id = "plot2_title", style={"backgroundColor": colors['box2green'], 'border': '1px solid','padding-left':5}),

            html.Iframe(
                sandbox='allow-scripts',
                id='plot2',
                height='290',
                width='550',
                style={'border-width': '0'},

                ################ The magic happens here
                srcDoc= Plotter.pm_linechart("Vancouver", pms = [2.5, 10], height = 250, width = 300, daterange=[2000,2017]).to_html()
    
                ################ The magic happens here

                )
            ])
        
        

    ]),

    ###########################################
    # CHART 4
    ###########################################
    html.Div(className='five columns', style={"backgroundColor": colors['white'], 'text-align': 'center', 'margin-left':10, 'margin-right':0,"padding": 0}, children=[

        html.Div(className="row",  children=[
            html.H6("Chart 4: PM2.5 Concentration Heatmap", id = "plot4_title", style={"backgroundColor": colors['box4purp'], 'border': '1px solid', "padding-left": 5}),

            html.Iframe(
                sandbox='allow-scripts',
                id='plot4',
                height='300',
                width='550',
                style={'border-width': '0'},

                ################ The magic happens here
                srcDoc = Plotter.make_heatmap(pm = 2.5, width = 340, height = 250, daterange=[2000,2017]).to_html()
                ################ The magic happens here
                ),
                html.P("Hover over heatmap for location and date information"),
                html.P("Red lines show the time period subset presented in other charts")
            ])

    ])
]),



# BOX 5
html.Div(className="row", children=[

    #BOX5 DATE CONTROLLER
    html.Div(className="row",  style={'backgroundColor': colors['light_grey'], 'padding-bottom':30, 'padding-left':20,'padding-right':20,  'border': '1px solid'}, children=[
        html.P("Date control slider", style={'padding-top':0}),
        dcc.RangeSlider(
            id = 'daterange',
            marks={i: '{}'.format(i) for i in range(2000, 2018)},
            step = None,
            min=2000,
            max=2017,
            value=[2000, 2017]
        )
        ]),
    html.A("BC Ministry of Environment and Climate Change Strategy", href = "https://catalogue.data.gov.bc.ca/dataset/77eeadf4-0c19-48bf-a47a-fa9eef01f409", target = "_blank"),
    html.P("Data is limited to the stations where measurements were taken and therefore does not account for the entirety of BC")


])
]

heatmap_view_div = [html.Div(style={"backgroundColor": colors['white'], 'text-align': 'center', 'display': 'inline-block', 'margin-left':10, 'margin-right':0,"padding": 0}, children=[

        html.H6("PM2.5 Concentration Heatmap", id = "heatmap_title", style={"backgroundColor": colors['box4purp'], 'align': 'center', 'border': '1px solid', "padding-left": 5}),

        dcc.Dropdown(
            id = 'heatmap_pollutant',
            options=[
                {'label': 'Pollutant: PM2.5', 'value': 2.5},
                {'label': 'Pollutant: PM10', 'value': 10}
            ],

            value=2.5,
            clearable = False
        ),

        html.Iframe(
            sandbox='allow-scripts',
            id='heatmap_plot',
            height='750',
            width='1700',
            style={'border-width': '0'},

            ################ The magic happens here
            srcDoc = Plotter.make_heatmap(pm = 2.5, width = 1480, height = 680,
                                        include_red_lines=False, include_y_labels = True).to_html()
            ################ The magic happens here
            ),
            html.P("Hover over heatmap for location and date information"),
            html.A("BC Ministry of Environment and Climate Change Strategy", href = "https://catalogue.data.gov.bc.ca/dataset/77eeadf4-0c19-48bf-a47a-fa9eef01f409", target = "_blank"),
            html.P("Data is limited to the stations where measurements were taken and therefore does not account for the entirety of BC")

])]

# def chart1_wrapper(pollutant1,location1, daterange):
#     return Plotter.location_linechart(pm = pollutant1, init_locations= location1,height = 220, width = 320,
#                                                 start_date = str(daterange[0])+'-01-01', end_date= str(daterange[1])+'-01-01').to_html()
# app.layout = html.Div(style={'backgroundColor': colors['white']}, children=[
#     # HEADER
#     html.Div(className="row", style={'backgroundColor': colors['black'], 'border': '1px solid', "padding-left": 5}, children=[
#         html.H3('Pollutants Matter BC – Visualization of Particulate Matter Concentrations',
#                 style={'color':colors['white'], 'margin-top':2, 'margin-bottom':2}),
#         html.P('This application tracks weighted monthly averages for pollution data collected from different stations across British Columbia. The measured pollutants, PM2.5 and PM10, refer to atmospheric particulate matter (PM) that have a diameter of less than 2.5 and 10 micrometers, respectively.',
#                 style={'color':colors['white'], 'margin-top':2, 'margin-bottom':2})
# APP LAYOUT
app.layout = html.Div(style={'backgroundColor': colors['white']}, children=[
    # HEADER
    html.Div(className="row", style={'backgroundColor': colors['black'], 'border': '1px solid', "padding-left": 5}, children=[
        html.H3('Pollutants Matter BC – Visualization of Particulate Matter Concentrations',
                style={'color':colors['white'], 'margin-top':2, 'margin-bottom':2}),
        html.P('This application tracks weighted monthly averages for pollution data collected from different stations across British Columbia. The measured pollutants, PM2.5 and PM10, refer to atmospheric particulate matter (PM) that have a diameter of less than 2.5 and 10 micrometers, respectively.',
                style={'color':colors['white'], 'margin-top':2, 'margin-bottom':2})
    ]),

    # TAB
    dcc.Tabs(id="tabss", value='general_tab', children=[
        dcc.Tab(label='Joint View', value='general_tab'),
        dcc.Tab(label='Enlarged Heatmap', value='heatmap_tab'),
    ]),

    html.Div(id='tabs-content')



])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabss', 'value')])
def render_content(tab):
    if tab == 'general_tab':

        return joint_view_div

    elif tab == 'heatmap_tab':

        return heatmap_view_div


@app.callback(
    [dash.dependencies.Output('plot1', 'srcDoc'),
    dash.dependencies.Output('plot1_title', 'children')],
    [dash.dependencies.Input('pollutant1', 'value'),
     dash.dependencies.Input('location1', 'value'),
     dash.dependencies.Input('daterange', 'value')])
def update_plot1(pollutant1, location1, daterange):

    if type(location1) == str:
        location1 = [location1]

    updated_plot1 =  Plotter.location_linechart(pm = pollutant1, init_locations= location1, width=400, height = 220, daterange = daterange).to_html()
    updated_title1 = "Chart 1: PM" + str(pollutant1) + " Concentration for given locations"

    return updated_plot1, updated_title1





@app.callback(
    [dash.dependencies.Output('plot2', 'srcDoc'),
    dash.dependencies.Output('plot2_title', 'children')],
    [dash.dependencies.Input('location2', 'value'),
     dash.dependencies.Input('daterange', 'value')])
def update_plot2(location2, daterange):

    updated_plot2 = Plotter.pm_linechart(location =location2, pms = [2.5, 10], height = 220, width = 400, daterange=daterange).to_html()
    updated_title2 = "Chart 3: Pollutant Concentration in " + str(location2)

    return updated_plot2, updated_title2



@app.callback(
    [dash.dependencies.Output('plot3', 'srcDoc'),
    dash.dependencies.Output('plot3_title', 'children')],
    [dash.dependencies.Input('location1', 'value'),
     dash.dependencies.Input('pollutant1', 'value'),
     dash.dependencies.Input('daterange', 'value')])

def update_plot3(location1, pollutant1, daterange):
    if type(location1) == str:
        location1 = [location1]
    updated_plot3 = Plotter.make_barchart(location1, pm = pollutant1, width = 350, height = 220, daterange=daterange).to_html()

    updated_title3 = "Chart 2: Distribution of PM" + str(pollutant1) + " Concentration for BC Cities"

    return updated_plot3, updated_title3

@app.callback(
    [dash.dependencies.Output('plot4', 'srcDoc'),
    dash.dependencies.Output('plot4_title', 'children')],
    [dash.dependencies.Input('pollutant4', 'value'),
     dash.dependencies.Input('daterange', 'value')])


def update_plot4(pollutant4, daterange):

    updated_plot4 = Plotter.make_heatmap(pm = pollutant4, width = 450, height = 250, daterange=daterange).to_html()
    updated_title4 = "Chart 4: PM" + str(pollutant4) + " Concentration Heatmap"

    return updated_plot4, updated_title4



@app.callback(
    [dash.dependencies.Output('heatmap_plot', 'srcDoc'),
    dash.dependencies.Output('heatmap_title', 'children')],
    [dash.dependencies.Input('heatmap_pollutant', 'value')])
def update_heatmap(heatmap_pollutant):

    updated_heatmap = Plotter.make_heatmap(pm = heatmap_pollutant, width = 1480, height = 680,
                                        include_red_lines=False, include_y_labels = True).to_html()
    updated_title = "PM" + str(heatmap_pollutant) + " Concentration Heatmap"

    return updated_heatmap, updated_title

if __name__ == '__main__':
    app.run_server(debug=True)
