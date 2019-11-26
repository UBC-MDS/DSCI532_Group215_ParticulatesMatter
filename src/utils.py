import altair as alt
import pandas as pd


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
alt.themes.register('mds_special', mds_special)

def make_heatmap(data, pm = 2.5, width = 800):
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
                    width=width
                )

def make_lineplot(data, pm = 2.5, width = 800, init_locations=[]):
    pm_filter = 'PM25' if pm == 2.5 else 'PM10'
    temp_data = data[data['PARAMETER'] == pm_filter]
    
    initialize_selection = [{'STATION_NAME': location} for location in init_locations]
    
    brush = alt.selection_multi(init=initialize_selection)
    
    return alt.Chart(temp_data, title = f'Concentration of PM{pm} in given locations').\
                mark_line(width = 10).\
                encode(
                    x=alt.X('index:O', title = 'date'),
                    y=alt.Y('RAW_VALUE', title = 'Concentration'),
                    color= alt.condition(brush, 'STATION_NAME', if_false=alt.value('lightgray')),
                    tooltip = [alt.Tooltip('index:O', title = 'Date:'),
                                alt.Tooltip('RAW_VALUE:N', title = 'Polution')]).\
                properties(
                    width=width,
                    height = 600
                ).add_selection(
                    brush
                )

def make_second_timeseries(data, location, pms = [2.5, 10], width = 800):
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
                    height = 600
                )


def make_barchart(data, locations, pm = 2.5, width = 800):
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
                    height = 600
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
