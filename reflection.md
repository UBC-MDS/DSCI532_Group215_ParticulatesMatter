## App Reflection

Below is a critique of our own application, summarizing the strengths and limitations of the interface. Furthermore, we describe potential features that could be added to increase the effectiveness of the interface.

### Areas of Strength
- The app succeeds in giving users different perspectives for which they can analyze the data, through the variety of plots. The heatmap provides a good summary of pollution concentration across all locations in the dataset. Clients can use the heatmap to discover locations of interest and then investigate these locations further by looking at distributions and time-series plots.
- Using a color code, it is intuitive for the user to distinguish the global controls (affect every plot) from the local controls (affect a single plot).
- The controls give the users flexibility in how they want to observe the data, with regards to time, location, and pollutant type. This flexibility allows users optimize the plots in a way that is beneficial to answering their particular research questions.

### Limitations
- There is a large proportion of missing data which limits what conclusions can be made using the app. Additionally, 
- We have data from 55 unique locations in BC, which doesn't work optimally with the multi-option dropdown dash component. When multiple locations are selected the app's layout becomes distorted. We considered using checkboxes, but it didn't seem reasonable to have 55 different checkboxes as it would lead to a cluttered layout.
- Currently, we only use monthly pollutant averages in all our plots. As a result, the user cannot assess individual data points. We made this decision to reduce the size of the data and make the plots easier to grasp, which meant a trade off with some information loss.

### Future Improvements
- Adding a map of BC would be extremely beneficial because it would allow us to show pollutant hotspots from a geographical standpoint. This can be helpful to users who aren't as familiar with the cities of BC.
- Fix the multi-option dropdown menu functionality to eliminate the distortion that is observed. For example, instead of having a drop down menu with all the locations, we could have a dropdown menu with different regions in BC (East Coast, South, Northern BC, etc.). Below the dropdown menu, there could be checkboxes with all the locations contained within a selected region.
- Like discussed in the limitations section, our app only contains data for monthly averages. It would be worth exploring alternative statistics that could be added to application, such as quartile ranges, correlational analysis, and variance.
