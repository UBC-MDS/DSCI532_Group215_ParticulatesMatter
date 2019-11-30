import altair as alt
import pandas as pd
import random

class PlotsCreator:
    """
    Class implements possibility to create several plots with given PM data.

    There are 4 different plots currently available in the class: barchart
    of one specified PM and different locations, heatmap with all the data,
    linechart with up to two PMs and one location, and linechart with one
    PM and multiple locations.

    Note: If data_avg is provided, average PM values will be depicted in
        both lineplots.
    """

    def __init__(self, data, data_avg=None, widths=500, heights=500):
        """__init__ takes necessary data and properties for later use

        Args:
            data (pandas.core.frame.DataFrame): pre-processed data
            data_avg (pandas.core.frame.DataFrame): pre-pricessed data that
                    contains averages of PMs for each date.
            widths (int): Width of each individual plot. This property can be
                    adjusted in each plot function.
            heights (int): Height of each individual plot. This property can be
                    adjusted in each plot function.

        Notes:
            - data should contain index column which has dtype string, with values
                year-month-date, where year, month and date are numbers

        """
        self.data = data
        self.data_avg = data_avg
        self.width = widths
        self.height = heights

    def make_barchart(self, locations, pm = 2.5, width = None, height = None, daterange=[2000,2017]):
        """
        Plots Barchart with given locations and pm

        Args:
            locations (iterable): Iterable object, like list, containing names
                    of the locations that want to be analyzed
            pm (float): PM type number. Ex. if we want to analyze PM10 we need
                    to pass pm=10. Default = 2.5
            width (int): Width of the plot. If provided, it will be preferred
                    over the global class value. Default = None
            height (int): Height of the plot. If provided, it will be preferred
                    over the global class value. Default = None
            start_date : The start date to highlight in red when plotting
            end_date : The end date to highlight in red when plotting

        Note: The type of the start_date and end_date should be the same as the
                'index' column of the data provided

        Returns:
            (altair.Chart) Altair chart

        Examples:
            make_barchart(locations = ["Vancouver", "Abbotsford"])
            make_barchart(locations = ["Vancouver", "Abbotsford"],
                            pm = 10)

        """
        start_date = str(daterange[0])+'-01-01' 
        end_date = str(daterange[1])+'-01-01'
        
        width = self.width if not width else width
        height = self.height if not height else height

        pm_filter = 'PM25' if pm == 2.5 else 'PM10'
        temp_data = self.data[self.data['STATION_NAME'].isin(locations)]
        temp_data = temp_data[temp_data['PARAMETER'] == pm_filter]


        if start_date:
            temp_data = temp_data[temp_data['index'] > start_date]
        if end_date:
            temp_data = temp_data[temp_data['index'] < end_date]



        return alt.Chart(temp_data).\
                    mark_bar(fillOpacity = 0.5).\
                    encode(
                        x=alt.X('RAW_VALUE', bin=alt.Bin(step=0.5), title = 'Concentration()'),
                        y = alt.Y('count()',
                                  stack = None,
                                  title = 'Frequency'),
                        color = alt.Color('STATION_NAME', title='Locations')
                        ).\
                    properties(
                        width=width,
                        height = height
                    )

    def pm_linechart(self, location, pms = [2.5, 10], width = None, height = None, daterange=[2000,2017]):
        """
        Plots linechart with up to two PMs and one location.

        Args:
            location (str): The name of the location that should be plotted
            pms (iterable): Iterable, like list, containing PM type number(s).
                        Default = [2.5, 10]
            width (int): Width of the plot. If provided, it will be preferred
                    over the global class value. Default = None
            height (int): Height of the plot. If provided, it will be preferred
                    over the global class value. Default = None
            start_date : The start date to highlight in red when plotting
            end_date : The end date to highlight in red when plotting

        Note: The type of the start_date and end_date should be the same as the
                'index' column of the data provided

        Returns:
            (altair.Chart) Altair chart

        Examples:
            pm_linechart(location = "Vancouver")
            pm_linechart(location = "Vancouver", pms = [2.5],
                                start_date = '2005-01-01',
                                end_date = '2008-01-01')

        """

        start_date = str(daterange[0])+'-01-01' 
        end_date = str(daterange[1])+'-01-01'

        width = self.width if not width else width
        height = self.height if not height else height


        temp_data = self.data[self.data['STATION_NAME'] == location]

        if start_date:
            temp_data = temp_data[temp_data['index'] > start_date]
        if end_date:
            temp_data = temp_data[temp_data['index'] < end_date]


        if len(pms) == 1:
            pm = pms[0]
            pm_filter = 'PM25' if pm == 2.5 else 'PM10'
            temp_data = temp_data[temp_data['PARAMETER'] == pm_filter]
        elif len(pms) == 0:
            temp_data = pd.DataFrame(columns = data.columns)


        keyvals = pd.date_range(temp_data['index'].min(), temp_data['index'].max(), freq='MS').astype(int) // 1000000

        base_plot = alt.Chart(temp_data).mark_line(
                            width = 10,
                            point = True
                        ).transform_window(
                            rolling_mean='mean(RAW_VALUE)',
                            frame=[-2, 2],
                            groupby = ['PARAMETER']
                        ).encode(
                            x=alt.X('index:T', title = 'date'),
                            y=alt.Y('rolling_mean:Q',
                                title = 'Concentration()',
                                impute=alt.ImputeParams(value=None, keyvals=list(keyvals))
                            ),
                            color= alt.Color('PARAMETER'),
                            tooltip = [alt.Tooltip('index:T', title = 'Date:'),
                                       alt.Tooltip('RAW_VALUE:N', title = 'Pollution')]
                        ).properties(
                            width=width,
                            height=height
                        )

        if self.data_avg is not None:

            avg_d = self.data_avg[self.data_avg['PARAMETER'] == pm_filter] if len(pms) == 1 else self.data_avg

            if start_date:
                avg_d = avg_d[avg_d['index'] > start_date]
            if end_date:
                avg_d = avg_d[avg_d['index'] < end_date]


            return alt.Chart(avg_d).mark_line(
                            width = 10,
                            point = True
                        ).transform_window(
                            rolling_mean='mean(RAW_VALUE)',
                            frame=[-2, 2],
                            groupby = ['PARAMETER']
                        ).encode(
                            x=alt.X('index:T', title = 'date'),
                            y=alt.Y('rolling_mean:Q',
                                title = 'Concentration()',
                                impute=alt.ImputeParams(value=None, keyvals=list(keyvals))
                            ),
                            detail = alt.Color('PARAMETER'),
                            color = alt.value('lightgray'),
                            tooltip = [alt.Tooltip('index:T', title = 'Date:'),
                                       alt.Tooltip('RAW_VALUE:N', title = 'Pollution')]
                        ).properties(
                            width=width,
                            height=height
                        ) + base_plot

        return base_plot



    def location_linechart(self, pm = 2.5, init_locations=[], width = None, height = None, daterange =[2000,2017]):
        """
        Plots linechart with one PM and multiple locations.

        Plots all locations, but highlights only selected lines

        Args:
            pm (float): PM type number. Ex. if we want to analyze PM10 we need
                    to pass pm=10. Default = 2.5
            init_locations (iterable): Iterable, like list, containing locations
                        that will be highlighted at first. Default = []
            width (int): Width of the plot. If provided, it will be preferred
                    over the global class value. Default = None
            height (int): Height of the plot. If provided, it will be preferred
                    over the global class value. Default = None
            start_date : The start date to highlight in red when plotting
            end_date : The end date to highlight in red when plotting

        Note: The type of the start_date and end_date should be the same as the
                'index' column of the data provided

        Returns:
            (altair.Chart) Altair chart

        Examples:
            location_linechart(init_locations = "Vancouver")
            location_linechart(init_locations = ["Vancouver",
                                "Abbotsford"], pm = 10,
                                start_date = '2005-01-01',
                                end_date = '2008-01-01')

        """
        start_date = str(daterange[0])+'-01-01' 
        end_date = str(daterange[1])+'-01-01'

        width = self.width if not width else width
        height = self.height if not height else height

        pm_filter = 'PM25' if pm == 2.5 else 'PM10'
        temp_data = self.data[self.data['PARAMETER'] == pm_filter]

        temp_data = temp_data[temp_data['STATION_NAME'].isin(set(init_locations))]
        if self.data_avg is not None:
            avg_data = self.data_avg[self.data_avg['PARAMETER'] == pm_filter]
            avg_data['STATION_NAME'] = ['average']*len(avg_data)

            temp_data = pd.concat((temp_data, avg_data)).reset_index()

        if start_date:
            temp_data = temp_data[temp_data['index'] > start_date]
        if end_date:
            temp_data = temp_data[temp_data['index'] < end_date]



        initialize_selection = [{'STATION_NAME': location} for location in init_locations]

        brush = alt.selection(type = 'multi', init=initialize_selection, nearest=True)

        keyvals = pd.date_range(temp_data['index'].min(), temp_data['index'].max(), freq='MS').astype(int) // 1000000

        line_highlight = alt.Chart(temp_data).mark_line(width = 10, point=True).\
                        transform_window(
                            rolling_mean='mean(RAW_VALUE)',
                            frame=[-2, 2],
                            groupby = ['PARAMETER']
                        ).encode(
                            x=alt.X('index:T', title = 'date'),
                            y=alt.Y('rolling_mean:Q', title = 'Concentration',
                                   impute=alt.ImputeParams(value=None, keyvals=list(keyvals))),
                            color = alt.condition(brush, 'STATION_NAME', if_false=alt.value('lightgray')),
                            tooltip = [alt.Tooltip('index:T', title = 'Date:'),
                                alt.Tooltip('RAW_VALUE:N', title = 'Polution'),
                                alt.Tooltip('STATION_NAME:N', title = 'Location')]
                        ).transform_filter(
                            brush
                        ).properties(
                            width=width,
                            height = height
                        ).add_selection(
                            brush
                        )

        if self.data_avg is not None:
            if start_date:
                avg_data = avg_data[avg_data['index'] > start_date]
            if end_date:
                avg_data = avg_data[avg_data['index'] < end_date]



            return alt.Chart(avg_data).\
                    mark_line(width = 10, point=True).\
                    transform_window(
                        rolling_mean='mean(RAW_VALUE)',
                        frame=[-2, 2],
                        groupby = ['PARAMETER']
                    ).\
                    encode(
                        x=alt.X('index:T', title = 'date'),
                        y=alt.Y('rolling_mean:Q', title = 'Concentration',
                               impute=alt.ImputeParams(value=None, keyvals=list(keyvals))),
                        color= alt.value('lightgray'),
                        tooltip = [alt.Tooltip('index:T', title = 'Date:'),
                                    alt.Tooltip('RAW_VALUE:N', title = 'Polution'),
                                    alt.Tooltip('STATION_NAME:N', title = 'Location')]).\
                    properties(
                        width=width,
                        height = height
                    ) + line_highlight

        return line_highlight


    def make_heatmap(self, pm = 2.5, width = None, height = None, daterange=[2000,2017]):
        """
        Plots heatmap with all locations and given pm

        Plots all locations, but highlights only selected lines

        Args:
            pm (float): PM type number. Ex. if we want to analyze PM10 we need
                    to pass pm=10. Default = 2.5
            width (int): Width of the plot. If provided, it will be preferred
                    over the global class value. Default = None
            height (int): Height of the plot. If provided, it will be preferred
                    over the global class value. Default = None
            start_date : The start date to highlight in red when plotting
            end_date : The end date to highlight in red when plotting

        Note: The type of the start_date and end_date should be the same as the
                'index' column of the data provided

        Returns:
            (altair.Chart) Altair chart

        Examples:
            make_heatmap(pm = 10,
                    start_date = '2005-01-01',
                    end_date = '2008-01-01')

        """

        start_date = str(daterange[0])+'-01-01' 
        end_date = str(daterange[1])+'-01-01'

        width = self.width if not width else width
        height = self.height if not height else height

        pm_filter = 'PM25' if pm == 2.5 else 'PM10'
        temp_data = self.data[self.data['PARAMETER'] == pm_filter]
        temp_data['RAW_VALUE'] = temp_data['RAW_VALUE'].clip(
                                        upper = temp_data['RAW_VALUE'].quantile(0.99))

        temp_data['index'] = pd.to_datetime(temp_data['index'])

        base_chart = alt.Chart(temp_data, title = f'Concentration of PM{pm} in BC').\
                    mark_rect().\
                    encode(
                        x=alt.X('index:O', title = 'date', axis = alt.Axis(labels=False, ticks=False)),
                        y=alt.Y('STATION_NAME:N', title = 'Location',  axis=alt.Axis(labels=False, ticks=False)),
                        color= alt.Color('RAW_VALUE:Q', legend=alt.Legend(title=f"")),
                        tooltip = [alt.Tooltip('index:O', title = 'Date:'),
                                    alt.Tooltip('RAW_VALUE:N', title = 'Pollution'),
                                    alt.Tooltip('STATION_NAME:O', title = 'Location')]).\
                    properties(
                        width = width,
                        height = height
                    )

        if start_date is not None or end_date is not None:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            lines = pd.DataFrame({'val': [v for v in (start_date, end_date) if v is not None]})

            rule = alt.Chart(lines).mark_rule(color='red').encode(
                x =alt.X('val:O', title = 'filter', axis = None)
            )

            return (base_chart + rule)

        return base_chart


