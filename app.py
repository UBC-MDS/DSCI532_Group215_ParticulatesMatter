
# external libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import nltk
import json
import pandas as pd
import plotly.graph_objs as go
import plotly_express as px




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
    html.Div(className="row", style={'backgroundColor': colors['banner_blue'], "padding": 5}, children=[
        html.H2('Pollutants Matter BC – visualization of particulate matter concentrations',
                style={'color':colors['black']})
    ]),
    
    
    # SIDEBAR
    html.Div(className="two columns", style={'backgroundColor': colors['light_grey'], 'padding': 0}, children=[

        #BOX1 BLUE
        html.Div(className="row",  style={'backgroundColor': colors['box1blue'], 'padding': 20}, children=[
        html.P("Chart 1 controls:\nPollutant:\nLocation:\n ")]),

        #BOX2 GREEN
        html.Div(className="row",  style={'backgroundColor': colors['box2green'], 'padding': 20}, children=[
        html.P("Chart 2 controls:\nPollutant:\nLocation:\n ")]),

        #BOX3 YELLOW
        html.Div(className="row",  style={'backgroundColor': colors['box3yellow'], 'padding': 20}, children=[
        html.P("Chart 3 controls:\nPollutant:\nLocation:\n ")]),

        #BOX4 PURPLE
        html.Div(className="row",  style={'backgroundColor': colors['box4purple'], 'padding': 20}, children=[
        html.P("Chart 4 controls:\nPollutant:\nLocation:\n ")]),

        #BOX5 LIGHT_GREY
        html.Div(className="row",  style={'backgroundColor': colors['light_grey'], 'padding': 20}, children=[
        html.P("Date axis controller")]),
        
    ]),


    
  

    # MAIN CHART AREA
    html.Div(className='ten columns', style={"backgroundColor": colors['white'], "padding": 20}, children=[
        
        html.Div(className="row",  children=[
            html.H4("Distribution and heatmap charts go here")
        ])
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)