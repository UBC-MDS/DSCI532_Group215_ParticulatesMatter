## App Relection

Positives:
- the app succeeds in giving users a good summary of pollution concentration over time, with the use of the heatmap
- Separating the global controls from the local controls of each plot using color makes it intuitive for users
- the controls give the users flexibility in how they want to observe the data, with regards to time, location, and pollutant type, without giving the users too much control 

Limitations:
- a good proportion of missing data limits what conclusions can be made using the app
- We have data from 55 unique locations in BC, which doesn't work optimally with the multi-option dropdown dash component. When mulitple locations are selected the apps layout becomes distorted. We considered using checkboxes but it didn't seem reasonable to have 55 different checkboxes.
- 

Future Improvements:
- could add a map of BC and show pollutant hotspots from a geographical standpoint. This will be extremely helpful to users who aren't as familiar with the cities of BC, especially those in rural areas.
- Fix the multi-option dropdown menu functionality to eliminate the distortion that is observed. For example, instead of having a drop down menu with all the locations, we could have a dropdown menu with different regions in BC (East Coast, South, Northern BC,...etc). Below the dropdown menu, there could be checkboxes with all the locations contained within a selected region.
