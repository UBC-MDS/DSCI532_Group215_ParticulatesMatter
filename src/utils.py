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
    """

    def __init__(self, data, widths=500, heights=500):
        """__init__ takes necessary data and properties for later use

        Args:
            data (pandas.core.frame.DataFrame): pre-processed data
            widths (int): Width of each individual plot. This property can be
                    adjusted in each plot function.
            heights (int): Height of each individual plot. This property can be
                    adjusted in each plot function.

        Notes:
            - data should contain index column which has dtype string, with values
                year-month-date, where year, month and date are numbers

        """
        self.data = data
        self.width = widths
        self.height = heights

    def make_barchart(self, locations, pm = 2.5, width = None, height = None):
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


        Returns:
            (altair.Chart) Altair chart

        Examples:
            make_barchart(locations = ["Vancouver Kitsilano", "Abbotsford Central"])
            make_barchart(locations = ["Vancouver Kitsilano", "Abbotsford Central"],
                            pm = 10)

        """

        width = self.width if not width else width
        height = self.height if not height else height

        pm_filter = 'PM25' if pm == 2.5 else 'PM10'
        temp_data = self.data[self.data['STATION_NAME'].isin(locations)]
        temp_data = temp_data[temp_data['PARAMETER'] == pm_filter]


        return alt.Chart(temp_data, title = f'Distribution of concentration of PM{pm} in given locations').\
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

    def pm_linechart(self, location, pms = [2.5, 10], width = None, height = None):
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

        Returns:
            (altair.Chart) Altair chart

        Examples:
            pm_linechart(location = "Vancouver Kitsilano")
            pm_linechart(location = "Vancouver Kitsilano", pms = [2.5])

        """

        width = self.width if not width else width
        height = self.height if not height else height


        temp_data = self.data[self.data['STATION_NAME'] == location]
        if len(pms) == 1:
            pm = pms[0]
            pm_filter = 'PM25' if pm == 2.5 else 'PM10'
            temp_data = temp_data[temp_data['PARAMETER'] == pm_filter]
        elif len(pms) == 0:
            temp_data = pd.DataFrame(columns = data.columns)

        keyvals = pd.date_range(temp_data['index'].min(), temp_data['index'].max(), freq='MS').astype(int) // 1000000

        return alt.Chart(temp_data).mark_line(
            width = 10
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
            title=f'Concentration of selected PMs in {location}',
            width=width,
            height=600
        )



    def location_linechart(self, pm = 2.5, init_locations=[], width = None, height = None):
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

        Returns:
            (altair.Chart) Altair chart

        Examples:
            location_linechart(init_locations = "Vancouver Kitsilano")
            location_linechart(init_locations = ["Vancouver Kitsilano",
                                "Abbotsford Central"], pm = 10)

        """

        width = self.width if not width else width
        height = self.height if not height else height

        pm_filter = 'PM25' if pm == 2.5 else 'PM10'
        temp_data = self.data[self.data['PARAMETER'] == pm_filter]

        random_locations = random.choices(list(temp_data['STATION_NAME']), k=6)
        temp_data = temp_data[temp_data['STATION_NAME'].isin(set(init_locations + random_locations))]


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
        ).transform_filter(
            brush
        ).properties(
            width=width,
            height = height
        )

        return alt.Chart(temp_data, title = f'Concentration of PM{pm} in given locations').\
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
                        color= alt.condition(brush, 'STATION_NAME', if_false=alt.value('lightgray')),
                        tooltip = [alt.Tooltip('index:T', title = 'Date:'),
                                    alt.Tooltip('RAW_VALUE:N', title = 'Polution')]).\
                    properties(
                        width=width,
                        height = height
                    ).add_selection(
                        brush
                    ) + line_highlight


    def make_heatmap(self, pm = 2.5, width = None, height = None):
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

        Returns:
            (altair.Chart) Altair chart

        Examples:
            make_heatmap(pm = 10)

        """


        width = self.width if not width else width
        height = self.height if not height else height

        pm_filter = 'PM25' if pm == 2.5 else 'PM10'
        temp_data = self.data[self.data['PARAMETER'] == pm_filter]
        return alt.Chart(temp_data, title = f'Concentration of PM{pm} in BC').\
                    mark_rect().\
                    encode(
                        x=alt.X('index:O', title = 'date'),
                        y=alt.Y('STATION_NAME:O', title = '', impute=alt.ImputeParams(
                              value=None
                            )),
                        color= alt.Color('RAW_VALUE:Q', legend=alt.Legend(title=f"Concentration of PM{pm}()")),
                        tooltip = [alt.Tooltip('index:O', title = 'Date:'),
                                    alt.Tooltip('RAW_VALUE:N', title = 'Polution'),
                                    alt.Tooltip('STATION_NAME:O', title = 'Location')]).\
                    properties(
                        width = width,
                        height = height
                    )


