## App Reflection

### Areas of Strength
- The app gives users different perspectives for which they can analyze the data, through a variety of plots. Clients can use the heatmap to discover locations of interest and then investigate these locations further by looking at distributions and time-series plots.
- Using a color code, it is intuitive for the user to distinguish the global controls (affect every plot) from the local controls (affect a single plot).
- The controls give the users flexibility in how they want to observe the data, with regards to time, location, and pollutant type. This allows users optimize the plots to better approach their research questions.

### Limitations
- There is a large proportion of missing data which limits what conclusions can be made using the app.
- We have data from 55 unique locations in BC, which doesn't work optimally with the multi-option dropdown dash component. When multiple locations are selected the app's layout becomes distorted.
- Currently, we only use monthly pollutant averages in all our plots. As a result, the user cannot assess individual data points. We made this decision to reduce the size of the data and make the plots easier to grasp.

### Future Improvements
- Adding a map of BC would be beneficial because it would geographically show pollutant hotspots. This can help users who aren't familiar with BC.
- Fix the multi-option dropdown to eliminate the observed distortions. For example, instead of having a drop-down menu with all the locations, we could have a dropdown menu with different regions in BC (West Coast, Northern BC, etc.). Below the dropdown menu, there could be checkboxes with all the locations contained within a selected region.
- It would be worth exploring alternative statistics that could be added to application, such as quartile ranges, correlational analysis, and variance.

### Addressing TA Feedback

1. You could add a couple of sentences with information about your dashboard in the menu panel, including your data source

    Action Taken: In the menu panel, we added source information and clearly stated that we are using weighted monthly averages.

2. Make sure it is clear to the user which controls affect which plots. If possible make this distinction even clearer than what your sketch is showing

    Action Taken: In addition to color coding the charts and control panels, we also gave explicit labels like "Chart 1", Chart 2", etc.

3. State this data is not for the entire province

    Action Taken: Added a footnote to clarify that the data is not for the entire province.

4. I am not sure right now what your y-axis represents in the heat map

    Action Taken: We ended up having to remove x-axis and y-axis ticks because of spacing issues. Instead we point the user to using the tooltip for information on time, location, and pollutant concentration. We acknowledge that this is not optimal and we will look to find an alternative in the next two weeks of the course.