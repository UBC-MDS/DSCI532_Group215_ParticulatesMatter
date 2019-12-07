# Tab 1 src code
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


def get_heatmap_view(Plotter, colors, pm_df):
    return [html.Div(style={"backgroundColor": colors['white'], 'text-align': 'center', 'display': 'inline-block', 'margin-left':10, 'margin-right':0,"padding": 0}, children=[

            html.H6("PM2.5 Concentration Heatmap", id = "heatmap_title", style={"backgroundColor": colors['box4green'], 'align': 'center', 'border': '1px solid', "padding-left": 5}),

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
                html.P("Hover over heatmap for location and date information")

    ])]

def get_joint_view(Plotter, colors, pm_df, avg_df):

    return [
        html.Div(className="row", children=[

            # SIDEBAR
            html.Div(className="two columns", style={'backgroundColor': colors['light_grey'], 'padding': 0}, children=[

                #BOX1 BLUE
                html.Div(className="row",  style={'backgroundColor': colors['box1blue'],
                    'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':195,'border': '1px solid'}, children=[
                    html.P("Chart 1 & 2 controls:\n\n\n"),
                    html.P("Pollutant:"),

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
                        srcDoc= Plotter.location_linechart(pm = 2.5, init_locations=["Vancouver"],width=400, height = 250, daterange=[2005,2010]).to_html()
                        ################ The magic happens here
                        ),
                        html.P("The grey lines represent the provincial averages of the selected pollutant")
                ])
            ]),

            ###########################################
            # CHART 2
            ###########################################
            html.Div(className='five columns', style={"backgroundColor": colors['white'], 'margin-left':10, 'margin-right':10, "padding": 0}, children=[

                html.Div(className="row",  children=[
                    html.H6("Chart 2: Distribution of PM2.5 Concentrations for BC Cities", id = 'plot2_title', style={"backgroundColor": colors['box3blue'], 'border': '1px solid', 'text-align': 'center',"padding-left": 5}),

                    html.Iframe(
                        sandbox='allow-scripts',
                        id='plot2',
                        height='300',
                        width='550',
                        style={'border-width': '0'},

                        ################ The magic happens here
                        srcDoc= Plotter.make_barchart(["Vancouver"], pm = 2.5, width = None, height = 250, daterange=[2000,2017]).to_html()
                        ################ The magic happens here
                        )
                    ])

            ]),

        ]),

        # BOXES 3 & 4 AND CHARTS 3 & 4
        html.Div(className="row", children=[

            # SIDEBAR
            html.Div(className="two columns", style={'backgroundColor': colors['light_grey'], 'padding': 0}, children=[

                #BOX3 YELLOW
                html.Div(className="row",  style={'backgroundColor': colors['box2green'],
                    'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':70, 'border': '1px solid'}, children=[
                html.P("Chart 3 controls:"),
                html.P("Location:\n", style={'padding-top':5}),

                dcc.Dropdown(
                    id = 'location3',
                    options=[
                        {'label':k , 'value': k } for k in pm_df['STATION_NAME'].unique()
                    ],
                    value="Vancouver",
                    clearable = False
                )
                ]),

                #BOX4 PURPLE
                html.Div(className="row",  style={'backgroundColor': colors['light_purple'],
                    'padding-left': 10, 'padding-right':10, 'padding-top':2, 'padding-bottom':90, 'border': '1px solid'}, children=[
                    html.P("Chart 4 controls:"),
                    html.P("Pollutant:"),

                    dcc.Dropdown(
                        id = 'pollutant4',
                            options=[
                                {'label': 'PM2.5', 'value': 2.5},
                                {'label': 'PM10', 'value': 10}
                            ],
                            value = 2.5,
                            clearable = False
                        ),

                    ])
            ]),

            ###########################################
            # CHART 2
            ###########################################
            html.Div(className='five columns', style={"backgroundColor": colors['white'], 'text-align': 'center', 'margin-left':10, 'margin-right':0, "padding": 0}, children=[

                html.Div(className="row",  children=[
                    html.H6("Chart 3: Pollutant Concentration in Vancouver", id = "plot3_title", style={"backgroundColor": colors['box2green'], 'border': '1px solid','padding-left':5}),

                    html.Iframe(
                        sandbox='allow-scripts',
                        id='plot3',
                        height='290',
                        width='550',
                        style={'border-width': '0'},

                        ################ The magic happens here
                        srcDoc= Plotter.pm_linechart("Vancouver", pms = [2.5, 10], height = 250, width = 300, daterange=[2000,2017]).to_html()
                        ################ The magic happens here
                        ),
                        html.P("The grey lines represent the provincial averages for each pollutant")
                    ])

            ]),


            ###########################################
            # CHART 4
            ###########################################
            html.Div(className='five columns', style={"backgroundColor": colors['white'], 'text-align': 'center', 'margin-left':10, 'margin-right':0,"padding": 0}, children=[

                html.Div(className="row",  children=[
                    html.H6("Chart 4: PM2.5 Concentration Heatmap", id = "plot4_title", style={"backgroundColor": colors['light_purple'], 'border': '1px solid', "padding-left": 5}),

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
                        html.P("Red lines show the date period selected in the other charts")
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
