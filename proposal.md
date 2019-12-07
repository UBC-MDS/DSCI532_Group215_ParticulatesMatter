# Dashboard Proposal

## Section 1:  Motivation and Purpose

It is a well-known fact that air quality affects human health. Lots of studies have been made and proved this statement. It is estimated that around seven million people die each year worldwide because of air pollution. Particulate matter or pollution particle is a mixture of solid and liquid particles, which cause health problems among people. PM2.5 and PM10 refer to atmospheric particulate matter (PM) that have a diameter of less than 2.5 and 10 micrometers, respectively. PM2.5, for example, is so small that it can bypass the nose and throat of humans and penetrate the deeper layers of the lungs. One of [the studies](https://www.ncbi.nlm.nih.gov/pubmed/11879110) estimated that for every $10(μg/m^3)$ increase of this matter in the air increases the risk of cardiopulmonary and lung cancer about 4%, 6% and 8%. PM2.5 and PM10 can also cause bronchitis, asthma, different forms of heart diseases, etc.

Another known fact is that the consumption of energy, transport, air conditioning, heating, and other things cause an increase in PMs. But how to know which areas have the highest concentration? Knowing the concentration of these matters in given areas can help to investigate the causes of air pollution, take actions against it and reduce the risk of health issues. Our dashboard provides an easy-to-use platform where a user can investigate the concentration of PM2.5 and PM10 particulate matters in available areas and dates. The user has a chance to change the location, choose timestamps in the interactive charts and compare two or more locations together.

## Section 2 Description of the data

Our app will visualize data sourced from the BC Ministry of Environment and Climate Change. The ministry publishes quality-assured hourly data on its [website](https://catalogue.data.gov.bc.ca/dataset/77eeadf4-0c19-48bf-a47a-fa9eef01f409) from air quality monitoring stations across BC. It is important to note that these stations are not present in every city in BC and are not equally distributed, in terms of distance. Therefore, conclusions should be made with caution that the data do represent BC in its entirety. The Ministry of Environment and Climate Change stores separate files for each of the nine pollutants they track. For the purposes of this study, we selected the PM2.5 and PM10 datasets and merged them together. 

Each observation of the dataset is indexed by a datetime measured in Pacific Standard Time and found in the `DATA_PST` variable. The location of each weather monitoring station is found in the `STATION_NAME` variable, which is paired with a unique `EMS_ID`. The name of the specific pollutant measured is stored in the `PARAMETER` field and name of the instrument used to record pollutant concentrations is stored in the `INSTRUMENT` variable. The concentrations of PM2.5 and PM10 are recorded in the identical `RAW_VALUE` and `ROUNDED_VALUE` fields. The units corresponding to these concentrations are micrograms per cubic metre (ug/m3) as shown in the `UNITS` variable.

An additional step of filtering will be performed to limit the number of stations to the unique BC cities in the dataset, reducing the size of the working dataset. We will select the top 10 BC cities, in terms of data availability. This decision was made to avoid overplotting and allows users to focus on cities with a reasonable amount of data. Lastly, the data will be aggregated as required to show monthly averages pollution levels.


## Section 3: Research questions and usage scenarios


- Do concentration levels of PM10 and PM2.5 follow a similar trend?
- What is the range of average PM10 and PM2.5 concentrations in a given year?
- What locations have the highest concentration of pollutants? 
- Which location has the highest rate of increase for pollutant concentration?
- Does Vancouver have higher pollution concentrations than Kelowna?



  Dave, BC’s  Commissioner for Sustainable Development and the Environment, is in charge of assessing the state of air quality in BC. Recently, he has been informed by the Ministry of Health that there have been increasing cases of respiratory health problems along coastal locations in Vancouver. They suspect air quality to be a potential factor in this rise, so they ask Dave, the Commissioner for Sustainable Development and the Environment, to investigate and compile a report. To better understand the air quality situation, Dave wants to track how pollutant concentration has changed over time, with a special focus on whether the rate of increase poses a significant concern. In particular, he is interested in which locations exhibit the most concerning levels of pollution so that he can plan and recommend future interventions to government-level decision makers.

  Our app, “Pollutants Matter BC”, is centered around providing Dave with informative methods of visualization that will help him extract important trends and patterns with regards to pollutant concentration in the Greater Vancouver area. Since he was informed that health problems have become an issue in coastal locations, he may hypothesize that coastal areas have seen a rise in air pollution in the past decade. Interactive features, like a toggle for different locations, as well the option to choose different time ranges, will give Dave flexibility in how he chooses explore measures of air pollution, like PM10 and PM2.5. After viewing the data from different perspectives, Dave discovers that levels of PM2.5 in coastal locations are rising by an average of 4% each year. He recommends immediate intervention in his report to the government.