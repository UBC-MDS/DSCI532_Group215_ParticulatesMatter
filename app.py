
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
from src import utils, tabs

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
          "box4green": "#A8D5BAFF",
          "black": "#000000",
          "light_purple": "#E3D1FB"
          }

# TODO - move to separate file
# BOXES 1 & 2 AND CHARTS 1 & 2
joint_view_div = tabs.get_joint_view(Plotter, colors, pm_df, avg_df)

heatmap_view_div = tabs.get_heatmap_view(Plotter, colors, pm_df)

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
    [dash.dependencies.Input('location1', 'value'),
     dash.dependencies.Input('pollutant1', 'value'),
     dash.dependencies.Input('daterange', 'value')])

def update_plot2(location1, pollutant1, daterange):
    if type(location1) is not list:
        location1 = [location1]

    updated_plot2 = Plotter.make_barchart(location1, pm = pollutant1, width = 350, height = 220, daterange=daterange).to_html()

    updated_title2 = "Chart 2: Distribution of PM" + str(pollutant1) + " Concentration for BC Cities"

    return updated_plot2, updated_title2


@app.callback(
    [dash.dependencies.Output('plot3', 'srcDoc'),
    dash.dependencies.Output('plot3_title', 'children')],
    [dash.dependencies.Input('location3', 'value'),
     dash.dependencies.Input('daterange', 'value')])
def update_plot3(location2, daterange):

    updated_plot3 = Plotter.pm_linechart(location =location2, pms = [2.5, 10], height = 220, width = 400, daterange=daterange).to_html()
    updated_title3 = "Chart 3: Pollutant Concentration in " + str(location2)

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
